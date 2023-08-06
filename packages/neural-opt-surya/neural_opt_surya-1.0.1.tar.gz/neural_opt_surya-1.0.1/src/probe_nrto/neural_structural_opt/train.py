"""
Contains training routines for different optimizers.

Classes
-------
TrainModels
    Base class for training tensorflow (TF) models using optimizers.
TrainLBFGS
    Trains models using L-BFGS-B optimizer.
TrainTFOptimizer
    Trains models using TF optimizers.
TrainMMA
    Trains models using GCMMA from NLOPT.

Functions
---------
tb_save_grads_and_weights
    Utility function that writes details for TensorBoard.
project_density
    Applies a heavyside (volume preserving) projection on the densities.
mean_density
    Calculates the mean density.
optimizer_result_dataset
    Function that converts data to an xarray dataset.
_set_variables
    Assigns the values to tensorflow variables.
_get_variables
    Concatenates a list of tensors to a numpy array.
generate_indices
    Helper to generate the indices to save the parameters.
weights_to_file
    Saves the model's parameters to a local directory.
"""
#                                                                       Modules
# =============================================================================
# Standard
import logging
from typing import List, Union, Tuple
import pickle
from dataclasses import dataclass
from copy import deepcopy

# Third-party
import autograd
import autograd.numpy as np
import tensorflow as tf
import xarray
import scipy.optimize
import nlopt

# Local
from . import models
from . import topo_physics
from . import autograd_lib
#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


def tb_save_grads_and_weights(train_summary_writer, grads: List[tf.Tensor],
                              tvars: List[tf.Tensor],
                              i: int, model: tf.keras.Model) -> None:
    """For logging training details onto tensorboard.
    The following details are logged:
    a. Gradient as a histogram
    b. Weights as a histrogram (on the log-scale as well)
    c. Norm of the gradients
    d. Norm of the weights
    e. Compliance value
    f. Preactivations of each layer as histograms
    https://stackoverflow.com/questions/41711190/keras-how-to-get-the-output-of-each-layer # noqa
    NOTE: Storing the preactivations assumes that the input of the model is stored
        in "model.z".

    Parameters
    ----------
    train_summary_writer
        A summary writer object from Tensorflow
        train_summary_writer = tf.summary.create_file_writer(file)
    grads
        The gradients
    tvars
        Model's trainable variables
    i
        Iteration number
    model
        One of the Keras models

    Returns
    -------
        None
    """
    with train_summary_writer.as_default():
        for g, v in zip(grads, tvars):
            if g is not None:
                tf.summary.histogram("{}/grad_histogram".format(
                    v.name), g, step=i)
                tf.summary.histogram("{}/weight_histogram".format(
                    v.name), v, step=i)
                tf.summary.histogram("{}/log_grad_histogram".format(
                    v.name), np.log(np.abs(g)+1e-12), step=i)
                tf.summary.scalar('{}/weight_norm'.format(
                    v.name), np.linalg.norm(v), step=i)
                tf.summary.scalar('{}/grad_norm'.format(
                    v.name), np.linalg.norm(g), step=i)
        # for preactivations of each layer
        inp = model.core_model.input
        inp_val = model.z
        for layer in model.core_model.layers[1:]:
            tf.keras.backend.clear_session()
            # Make a temporary model
            temp_mdl = tf.keras.Model(inputs=inp, outputs=layer.output)
            inter_val = temp_mdl(inp_val)
            tf.summary.histogram("{}/intermediate_histogram".format(
                layer.name), inter_val, step=i)
            del temp_mdl


def project_density(x: np.ndarray, beta: float) -> np.ndarray:
    """Projects the densities using a heavyside function.
    With increasing values of beta, the heavyside filtering causes
    sharp black and white features. The projection will make sure that the
    volume fraction is not violated using a bi-section algorithm.
    See DOI 10.1007/s00158-009-0452-7 for the theory behind this.
    However, Equation (9) of DOI 10.1007/s00158-010-0602-y is used here.

    Parameters
    ----------
    x
        The density values stored as a matrix (like an image).
    beta
        Parameter that controls the severity of the heavyside function.

    Returns
    -------
    x
        Projected densities
    """
    f = lambda eta : topo_physics.f_eta(x, beta, eta)
    eta = topo_physics.my_bisection(f, 0, 1, 1e-2)
    x = (np.tanh(beta*eta) + np.tanh(beta*(x-eta))) / \
        (np.tanh(beta*eta) + np.tanh(beta*(1-eta)))
    return x


def mean_density(logits, args, cone_filter: bool = False,
                 den_proj: bool = False,
                 beta: float = 1) -> tf.Tensor:
    """Calculates the mean density.
    Allows this function to be differentiable when using tensorflow models.

    Parameters
    ----------
    logits
        The output from the model. This function can apply cone-filtering
        as well as heavyside projection before calculating the mean value.
    cone_filter
        Whether to apply a cone density filter
    den_proj
        Whether to apply a heavyside density projection
    beta
        The value of parameter for the heavyside projection.
        This has no effect of "den_proj" is not True.

    Returns
        cur_density
            The mean value of the density matrix.
    """
    shape = (args['nely'], args['nelx'])
    x = tf.reshape(0.0 + tf.cast(logits, tf.float64), shape)
    x = x * args['mask']

    if cone_filter:
        assert args['width']/args['nelx'] == args['height'] / args['nely']
        elem_size = args['width']/args['nelx']
        f = lambda x : autograd_lib.cone_filter(
                x, args['filter_width'] / elem_size, args['mask'])
        x = models.convert_autograd_to_tensorflow(f)(x)

    if den_proj:
        # Heavyside projector
        f2 = lambda x : project_density(x, beta)
        x = models.convert_autograd_to_tensorflow(f2)(x)
    # Some problems have masks which should not be included
    cur_density = tf.reduce_mean(x) / np.mean(args['mask'])
    return cur_density


def optimizer_result_dataset(
        optimization_details : dict,
        designs : List[np.ndarray],
        save_intermediate_designs : bool = True) -> xarray.Dataset:
    """Function that converts data to an xarray dataset.

    Parameters
    ----------
    optmization_details
        Dictionary of the various loss components and training
        hyper-parameters at each iteration
    designs
        The designs at each iteration
    save_intermediate_designs
        Whether to save all the designs or just the best one.
        The notion of best is a bit difficult for certain scenarios.
        WARNING---Best design here corresponds to the lowest total loss.

    Returns
    -------
        ds
            An xarray dataset with the required variables as
            data arrays.
    """
    opt_dict_to_xarray = {k : (('step'), v)
                          for k, v in optimization_details.items()
                          if k != 'logits'}
    if save_intermediate_designs:
        # add all designs to the dictionary
        opt_dict_to_xarray['designs'] = (('step', 'y', 'x'), designs)
        ds = xarray.Dataset(opt_dict_to_xarray,
                            coords={'step' : np.arange(len(
                                optimization_details['total_loss'])
                            )})
    else:
        # The best design will often but not always be the final one.
        best_design = np.nanargmin(optimization_details['total_loss'])
        opt_dict_to_xarray['design'] = (('y', 'x'), designs[best_design])
        ds = xarray.Dataset(opt_dict_to_xarray,
                            coords={'step' : np.arange(len(
                                optimization_details['total_loss'])
                            )})
        print("WARNING-Best design here corresponds to the lowest total loss")
    return ds


def _set_variables(variables : List[tf.Tensor], x : np.array) -> None:
    """Assigns the values to tensorflow variables.
    This function is used to set the values of model parameters
    to given values.

    Parameters
    ----------
    variables
        Model's parameter as obtained with model.trainable_variables
        for a keras model.
    x
        A numpy array with the same size as the number of model parameters.

    Returns
    -------
        None
    """
    shapes = [v.shape.as_list() for v in variables]
    values = tf.split(x, [np.prod(s) for s in shapes])
    for var, value in zip(variables, values):
        var.assign(tf.reshape(tf.cast(value, var.dtype), var.shape))


def _get_variables(variables : List[tf.Tensor]) -> np.array:
    """Concatenates a list of tensors to a numpy array.
    This function is used to get the values of model parameters
    as a 1D numpy array.

    Parameters
    ----------
    variables
        Model's parameter as obtained with model.trainable_variables
        for a keras model.

    Returns
    -------
        1D numpy array of the model's parameters
    """
    return np.concatenate([
      v.numpy().ravel() if not isinstance(v, np.ndarray)
      else v.ravel()
      for v in variables])


def generate_indices(tot_iterations : int, n_saves : int,
                     filename : str = 'weights_') -> Tuple[str, List]:
    """Helper to generate the indices to save the parameters.

    Parameters
    ----------
    tot_iterations
        The total number of iterations to un the optimization
    n_saves
        Frequency of saving the weights. If n_saves = 10, every 10th
        model parameters will be saved.
    filename
        The name for the parameter files.

    Returns
    -------
    filename
        Name for the parameter files
    indices
        The indices where the parameters should be saved.
    """
    filename = filename
    indices = []
    i = 0
    while i < tot_iterations:
        indices.append(i)
        i += n_saves
    indices.append(tot_iterations)
    return filename, indices


def weights_to_file(model : tf.keras.Model,
                    directory : str, filename : str) -> None:
    """Saves the model's parameters to a local directory.
    Note that we save the state of the model including the
    non-trainable parameters. The saved file is a dictionary with the
    keys as the variable names and values as the numpy arrays.
    Parameters
    ----------
    model
        The model whose parameters are to be saved.
        The current state is pickled.
    directory
        The path to the location where the files are to be saved.
    filename
        The name for the parameter files.

    Returns
    -------
    None
    """

    new_param = dict()
    list_of_vars = model.variables
    for i, var in enumerate(list_of_vars):
        key = model.variables[i].name
        new_param[key] = var.numpy()

    file_path = directory + '/' + filename + '.p'
    pickle.dump(new_param, open(file_path, 'wb'))
#                                                             Training routines
# =============================================================================


@dataclass
class TrainModels:
    """Base class for training TF models using optimizers.
    Uses the optimizer from Scipy.optimize.

    Attributes
    ----------
    model
        A keras model
    max_iterations
        The maximum number of iterations
    save_weights_path
        The location to save the model parameters
    n_saves
        The frequency of saving model parameters
    save_intermediate_designs
        Whether to save all the designs or only the best one.
    conv_criteria
        Whether to apply a converge criteria to decide whether to stop
        saving parameters.
        The current criteria is to check for the percentage difference
        in the loss across 10 iterations and if they are all below a certain
        limit, weights are no longer saved.
    convergence_limit
        The limit used to determine teh convergence of the optimizer.
    t_args
        The training arguments as a dictionary.
        vol_const_hard (bool) : Apply hard volume constraint
        cone_filter (bool) : Apply cone filter to densities [as in hoyer]
        cont_scheme (bool) : Apply continuation scheme for SIMP penalty (p)
        p_start (float) : Starting penalty - SIMP penalization
        p_end (float) : Final penalty value
        del_p (float) :  increment in the p value
        scale_loss (bool) : Whether to scale the loss by initial loss
        alpha_start (float) : Starting penalty value for soft volume constraint
        alpha_end (float) : maximum penalty value for soft volume constraint
        del_alpha (float) : Step size for penalty value for
                            soft volume constraint
        den_proj (bool) : Whether to apply density projection
        beta (float) : Projection parameter
    stats_file
        Location for saving tensorboard statistics
    optimizer
        Either 'lbfgs' or a tf.keras optimizer

    Methods
    -------
    __post_init__
        Function to initialize and setup the optimization.
    _setup_details_for_optimization
        Setting alpha, beta and p values as well as initial loss.
    _setup_saving_details
        Saves initial weight and sets up framework for saving details
        and weights.
    calculate_loss_and_grad
        Calculate the loss using the current model and its gradient using Tape.
    callback_after_itr
        The callback function that is to be called after one iteration of
        the optimizer is done.
    _transfer_func_to_itr_data
        Helper function to transfer data from each function call to main
        data (per iteration basis).
    save_current_model
        Saves the parameters of the current model.
    update_beta
        Updates the beta parameter, if needed.
    update_alpha_and_penalty
        Updates the alpha and penalty parameter if needed.
    """
    model: tf.keras.Model
    max_iterations: int
    training_args: dict = None
    save_weights_path: str = None
    n_saves : int = 1
    save_intermediate_designs : bool = True
    convergence_criteria : bool = True
    convergence_limit : float = 0.1
    stats_file : str = None
    optimizer: Union[str, tf.keras.optimizers.Optimizer] = 'lbfgs'

    def __post_init__(self):
        """Function to initialize and setup the optimization problem.
        """
        self.tvars = self.model.trainable_variables
        # Store the initial parameters
        self.tvars0 = deepcopy(self.tvars)
        self._setup_details_for_optimization()
        self._setup_saving_details()
        # Log the calculated gradient values
        if self.stats_file is not None:
            self.grad0 = 0.0
            self.grad = 0.0
        # To save details after every iteration
        self.opt_details = {'total_loss' : [], 'vf': [], 'vf_loss': [],
                            'cur_alpha': [], 'cur_penalty': [], 'logits' : []}
        self.itr_count = 0
        # To check whether the optimizer has converged
        self.has_converged = False
        # Logs the details of each function call
        self.func_call_details = deepcopy(self.opt_details)

    def _setup_details_for_optimization(self):
        """Initializes the values for alpha, beta and SIMP penalty.
        Also creates an initial compliance to be used for scaling
        purposes.
        """
        # Extract training_args
        t_args = self.training_args
        if t_args is None:
            t_args = self.training_args = {
                        'vol_const_hard': True,
                        'cont_scheme': False,
                        'cone_filter': True,
                        'scale_loss': False,
                        'den_proj': False
                            }
        self.continuation = t_args['cont_scheme']
        self.hard_vol_constraint = t_args['vol_const_hard']
        self.scale_compliance = t_args['scale_loss']
        # setup alpha_0, penalty_0 and beta_0
        # apply continuation scheme
        if self.continuation:
            self.penalty = t_args['p_start']
            self.penalty_values = np.arange(self.penalty, t_args['p_end'],
                                            t_args['del_p'])
        else:
            self.penalty = self.model.env.args['penal']
            self.penalty_values = [self.penalty]
        # Apply hard volume constraint
        if self.hard_vol_constraint:
            self.alpha = 'NA'
            self.alpha_values = [self.alpha]
        else:
            self.alpha = t_args['alpha_start']
            self.alpha_values = np.arange(self.alpha, t_args['alpha_end'],
                                          t_args['del_alpha'])
        # Apply density projection
        if self.training_args['den_proj']:
            self.betas = [0.1]
        else:
            self.betas = [1]
        # Initial value for scaling compliance- as per Tounn paper
        # Uniform grey compliance value
        if self.scale_compliance:
            pix_mdl = models.PixelModel(seed=0, args=self.model.env.args)
            pix_logits = pix_mdl(None)
            J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
            self.model.J0 = J0.numpy().item()
            del pix_mdl
        return None

    def _setup_saving_details(self):
        """Saves initial model parameters.
        Calculates the indices of the iterations at whcih
        the parameters are to be saved.
        Creates a summary writer for tensorboard as well.
        """
        # total number of iterations
        # L-BFGS needs to run without changing the penalty/alpha
        # every iteration.
        if self.optimizer == 'lbfgs':
            if self.continuation:
                # For L-BFGS, max_iterations correspond to per penalty value
                tot_itrs = self.max_iterations * len(self.penalty_values)
            else:
                tot_itrs = self.max_iterations * len(self.alpha_values)
        else:
            tot_itrs = self.max_iterations
        # save the parameters
        filename = None
        if self.save_weights_path is not None:
            filename, indices = generate_indices(tot_itrs,
                                                 self.n_saves,
                                                 self.save_weights_path)
            weights_to_file(self.model, self.save_weights_path,
                            filename+str(0))
        else:
            indices = []
        # for tensorboard statistics
        if self.stats_file is not None:
            self.train_summary_writer = tf.summary.create_file_writer(
                                        self.stats_file)
        self.indices = indices
        self.filename = filename
        return None

    def calculate_loss_and_grad(self):
        """Calculates the loss value and associated gradient.
        Utilizes the current values of alpha, beta, penalty and the model.
        """
        # uses current model and hyper-parameters
        args = self.model.env.args
        t_args = self.training_args
        beta = max(self.betas)
        # Calculate the loss and the gradients
        vf_loss = 0
        cur_density = args['volfrac']
        with tf.GradientTape() as t:
            t.watch(self.tvars)
            logits = self.model(None)
            compliance = self.model.loss(logits, self.hard_vol_constraint,
                                         t_args['cone_filter'],
                                         self.penalty,
                                         t_args['den_proj'], beta)
            # Choose the loss function
            final_loss = compliance

            if self.scale_compliance or not self.hard_vol_constraint:
                scaled_compliance = compliance / self.model.J0
                final_loss = scaled_compliance
            # for soft volume constraint, need to add the violation to the loss
            if not self.hard_vol_constraint:
                cur_density = mean_density(logits, args,
                                           self.training_args['cone_filter'])
                vf_loss = self.alpha * ((cur_density/args['volfrac']) - 1)**2
                total_loss = tf.cast(vf_loss,
                                     dtype=tf.float64) + scaled_compliance
                final_loss = total_loss
        grads = t.gradient(final_loss, self.tvars)

        # Log details of this function call
        if self.stats_file is not None:
            self.grad = grads
            if self.itr_count == 0 and \
               len(self.opt_details['total_loss']) == 0:
                self.grad0 = grads

        self.func_call_details['total_loss'].append(final_loss.numpy().item())
        self.func_call_details['logits'].append(logits.numpy())
        self.func_call_details['cur_penalty'].append(self.penalty)
        self.func_call_details['cur_alpha'].append(self.alpha)
        if type(cur_density) is float:
            self.func_call_details['vf'].append(
                        cur_density)
            self.func_call_details['vf_loss'].append(
                        vf_loss)
        else:
            self.func_call_details['vf'].append(
                        cur_density.numpy().item())
            self.func_call_details['vf_loss'].append(
                        vf_loss.numpy().item())
        return final_loss, grads

    def callback_after_itr(self):
        """The callback function that logs details after every iteration."""
        # Save details to main iteration dictionary
        if self.itr_count == 0:
            # For first run, save initial details as well
            self._transfer_func_to_itr_data(save_init=True)
            if self.stats_file is not None:
                tb_save_grads_and_weights(self.train_summary_writer,
                                          self.grad0 , self.tvars,
                                          self.itr_count, self.model)
        else:
            self._transfer_func_to_itr_data()
        self.itr_count += 1
        # Update  beta, if needed
        # todo: update alpha and penalty here as well ?
        self.update_beta()
        # Convergence criteria
        if self.itr_count in self.indices and \
                self.save_weights_path is not None:
            self.save_current_model()
        # save initial optimization details into Tensorboard
        if self.stats_file is not None:
            tb_save_grads_and_weights(self.train_summary_writer,
                                      self.grad , self.tvars,
                                      self.itr_count, self.model)
        return None

    def _transfer_func_to_itr_data(self, save_init=False):
        """Copies the details from the function call level dictionary.

        Parameters
        ----------
        save_init
            If true, saves the first entry as well. Otherwise, only the
            last entry is copied to the main dictionary.
        """
        f_dets = self.func_call_details
        o_dets = self.opt_details
        for key, val in o_dets.items():
            if save_init:
                val.append(f_dets[key][0])
            val.append(f_dets[key][-1])
        return None

    def save_current_model(self):
        """Saves the current model parameters.
        Applies convergence criteria if requested by the user.
        The convergence criteria adopted is to check teh percentage
        difference between the last 10 losses and if each
        is less than the limit specified, it is assumed to have converged.
        Once converged, weights will no longer be saved.
        """
        losses = self.opt_details['total_loss']
        # Needs at least 10 loss values
        if len(losses) < 10:
            weights_to_file(self.model,
                            self.save_weights_path,
                            self.filename+str(self.itr_count))
            return None

        if self.convergence_criteria:
            if not self.has_converged:
                last_losses = np.array(losses[-10:])
                per_change = -1*np.diff(last_losses) / last_losses[:-1]*100
                if np.all(per_change <= self.convergence_limit):
                    self.has_converged = True
                    # extract the converged indices only
                    self.indices = self.indices[
                                    :int(self.itr_count/self.n_saves) + 1]
                weights_to_file(self.model,
                                self.save_weights_path,
                                self.filename+str(self.itr_count))
        # Without convergence criteria, save all weights
        else:
            weights_to_file(self.model,
                            self.save_weights_path,
                            self.filename+str(self.itr_count))
        return None

    def update_beta(self):
        """Updates the heaviside projection parameter.
        The maximum beta is kept as 100 and beta is doubled if the maximum
        change in the logits is less than 0.01. It is also doubled once every
        few iterations (specified by self.training_args['beta_change']).
        """
        logits = self.opt_details['logits']
        if self.training_args['den_proj']:
            change_freq = self.training_args['beta_change']
            change = np.max(
                np.abs(logits[-2].ravel() - logits[-1].ravel())
                            )
            prev_beta = max(self.betas)
            if prev_beta < 100 and \
                    (self.itr_count % change_freq == 0 or change <= 0.01):
                cur_beta = 2 * prev_beta
                print("Beta has been changed to ", cur_beta)
            else:
                cur_beta = prev_beta
            self.betas.append(cur_beta)
        else:
            cur_beta = 1
            self.betas.append(cur_beta)
        return None

    def update_alpha_and_penalty(self):
        """Updates the SIMP and volume constraint violation penalties."""
        if self.continuation:
            self.penalty = max(self.training_args['p_end'],
                               self.penalty + self.training_args['del_p'])
        if not self.hard_vol_constraint:
            self.alpha = max(self.training_args['alpha_end'],
                             self.alpha + self.training_args['del_alpha'])


class TrainLBFGS(TrainModels):
    """Trains models using L-BFGS-B optimizer.
    Uses the optimizer from Scipy.optimize and has the same
    attributes as it's superclass (TrainModels).

    Methods
    -------
    objective_and_grad
        Calculating loss and the gradient in the format required by
        Scipy.optimize.
    run_lbfgs
        Trains the model.
    """
    def __init__(self, model: tf.keras.Model, max_iterations: int,
                 t_args: dict = None,
                 save_weights_path: str = None, n_saves : int = 1,
                 save_intermediate_designs : bool = True,
                 convergence_criteria : bool = True,
                 convergence_limit : float = 0.1,
                 stats_file : str = None,
                 ):
        super().__init__(model, max_iterations, t_args,
                         save_weights_path=save_weights_path,
                         n_saves=n_saves,
                         save_intermediate_designs=save_intermediate_designs,
                         convergence_criteria=convergence_criteria,
                         convergence_limit=convergence_limit,
                         stats_file=stats_file)

    def objective_and_grad(self, x: np.array) -> Tuple[float, np.array]:
        """Calculates the loss and corresponding gradient.
        Accepts an incoming 1D numpy array and sets it as the value of
        model's parameters. Then calculates the loss and gradients.

        Parameters
        ----------
        x
            A numpy array with the same size as the model parameters.

        Returns
        -------
            The loss value and the flattened gradient. The gradient has the
            same shape as 'x'.
        """
        _set_variables(self.tvars, x)
        final_loss, grads = self.calculate_loss_and_grad()
        return float(final_loss.numpy()), _get_variables(
                             grads).astype(np.float64)

    def run_lbfgs(self, **scipy_kwargs: dict) -> Tuple[xarray.Dataset, List]:
        """Uses L-BFGS-B to train the model.

        Parameters
        ----------
        scipy_kwargs
            The arguments for the scipy.optimize module

        Returns
        -------
            An xarray dataset that contains the details of the optimization as
            well as the indices where the weights were saved.
        """
        t_args = self.training_args
        # Choose the deciding variable for iteration
        # L-BFGS does not run well if values change per iteration.
        # Thus, we adopt a restarting procedure whenever we change them.
        if self.continuation and self.hard_vol_constraint:
            decider = self.penalty_values
        elif self.continuation and not self.hard_vol_constraint:
            decider = self.penalty_values
        elif not self.continuation and self.hard_vol_constraint:
            decider = [1]
        else:
            decider = self.alpha_values

        callback = lambda x : self.callback_after_itr()
        for outer_itr_count, _ in enumerate(decider):
            x0 = _get_variables(self.tvars).astype(np.float64)
            # rely upon the step limit instead of
            # error tolerance for finishing.
            _, _, info = scipy.optimize.fmin_l_bfgs_b(
                                self.objective_and_grad, x0,
                                maxfun=self.max_iterations,
                                maxiter=self.max_iterations,
                                callback=callback, factr=1,
                                pgtol=1e-14, **scipy_kwargs)
            # Update alpha and penalty, if needed
            self.update_alpha_and_penalty()
        # Convert logits to designs and save all details using xarray
        designs = [self.model.env.render(
                        x,
                        volume_contraint=self.hard_vol_constraint,
                        cone_filter=self.training_args['cone_filter'],
                        den_proj=self.training_args['den_proj'],
                        beta=self.betas[b])
                   for b, x in enumerate(self.opt_details['logits'])]

        # Add other details as well
        ds = optimizer_result_dataset(self.opt_details, designs,
                                      self.save_intermediate_designs)
        return ds, self.indices


class TrainTFOptimizer(TrainModels):
    """Trains models using optimizers from tensorflow keras.
    This has the same attributes as it's superclass (TrainModels).
    By default, the adam optimizer with the following default parameters
    is set:
    'learning_rate' : 0.01
    'global_clipnorm' : 0.01
    'epsilon' : 1e-8
    'ams_grad' : True

    Methods
    -------
    run_optimizer
        Trains the model.
    """
    def __init__(self, model: tf.keras.Model, max_iterations: int,
                 t_args: dict = None,
                 save_weights_path: str = None, n_saves : int = 1,
                 save_intermediate_designs : bool = True,
                 convergence_criteria : bool = True,
                 convergence_limit : float = 0.1,
                 stats_file : str = None,
                 ):
        super().__init__(model, max_iterations, t_args,
                         save_weights_path=save_weights_path,
                         n_saves=n_saves,
                         save_intermediate_designs=save_intermediate_designs,
                         convergence_criteria=convergence_criteria,
                         convergence_limit=convergence_limit,
                         stats_file=stats_file)
        self.itr_count = 0
        self.has_converged = False
        self.optimizer = tf.keras.optimizers.Adam(0.01, amsgrad=True,
                                                  epsilon=1e-8,
                                                  global_clipnorm=0.01)

    def run_optimizer(self) -> Tuple[xarray.Dataset, List]:
        """Uses tensorflow keras optimizer to train the model.

        Returns
        -------
            An xarray dataset that contains the details of the optimization as
            well as the indices where the weights were saved.
        """
        t_args = self.training_args
        for itr in range(self.max_iterations + 1):
            # Obtain grad and loss
            _, grads = self.calculate_loss_and_grad()
            # Apply gradient
            self.optimizer.apply_gradients(zip(grads, self.tvars))
            # Callback
            self.callback_after_itr()
            # Update alpha and penalty, if needed
            self.update_alpha_and_penalty()
        # Convert logits to designs and save all details using xarray
        designs = [self.model.env.render(
                        x,
                        volume_contraint=self.hard_vol_constraint,
                        cone_filter=self.training_args['cone_filter'],
                        den_proj=self.training_args['den_proj'],
                        beta=self.betas[b])
                   for b, x in enumerate(self.opt_details['logits'])]

        # Add other details as well
        ds = optimizer_result_dataset(self.opt_details, designs,
                                      self.save_intermediate_designs)
        return ds, self.indices


class TrainMMA(TrainModels):
    """Trains models MMA optimizer.
    This has the same attributes as it's superclass (TrainModels).
    GCMMA from nlopt library is used. Since MMA can take care of
    constraints, hard volume constraint is not needed. Also, continuation
    scheme has not yet been implemented for MMA.
    Note:
        Neural network models should have a sigmoid at the end to force
        the densities to be between 0 and 1. For PixelModels, this is taken
        care of by using bounds on the design variables.

    Methods
    -------
    objective_and_grad
        Calculates the loss and the gradient.
    constraint
        Calculates the constraint and it's gradient.
    run_mma
        Trains the model.
    """
    def __init__(self, model: tf.keras.Model, max_iterations: int,
                 t_args: dict = None,
                 save_weights_path: str = None, n_saves : int = 1,
                 save_intermediate_designs : bool = True,
                 convergence_criteria : bool = True,
                 convergence_limit : float = 0.1,
                 stats_file : str = None,
                 ):
        super().__init__(model, max_iterations, t_args,
                         save_weights_path=save_weights_path,
                         n_saves=n_saves,
                         save_intermediate_designs=save_intermediate_designs,
                         convergence_criteria=convergence_criteria,
                         convergence_limit=convergence_limit,
                         stats_file=stats_file)
        self.itr_count = 0
        self.has_converged = False
        self.optimizer = 'mma'
        # MMA can take care of inequalities
        assert self.hard_vol_constraint is False
        # MMA with continuation is not yet implemented
        assert self.continuation is False
        # Todo: NeuralModels has to have a sigmoid at the end

    def objective_and_grad(self, x: np.array) -> Tuple[float, np.array]:
        """Calculates the loss and corresponding gradient.
        Accepts an incoming 1D numpy array and sets it as the value of
        model's parameters. Then calculates the loss and gradients.

        Parameters
        ----------
        x
            A numpy array with the same size as the model parameters.

        Returns
        -------
            The loss value and the flattened gradient. The gradient has the
            same shape as 'x'.
        """
        _set_variables(self.tvars, x)
        final_loss, grads = self.calculate_loss_and_grad()
        # todo : update values and store them
        self.callback_after_itr()
        return float(final_loss.numpy()), _get_variables(
                             grads).astype(np.float64)

    def constraint(self, x: np.array) -> Tuple[float, np.array]:
        """Calculates the constraint and it's gradient.
        Accepts an incoming 1D numpy array and sets it as the value of
        model's parameters. Then calculates the constraint (volume constraint)
        and the corresponding gradient.

        Parameters
        ----------
        x
            A numpy array with the same size as the model parameters.

        Returns
        -------
            The loss value and the flattened gradient. The gradient has the
            same shape as 'x'.
        """
        _set_variables(self.tvars, x)
        constraint_fn_np = self.model.env.constraint
        constraint_fn_tf = models.convert_autograd_to_tensorflow(
                                    constraint_fn_np)
        # calculate the constraint and its gradient
        with tf.GradientTape() as t:
            t.watch(self.tvars)
            logits = self.model(None)
            constraint_value = constraint_fn_tf(logits,
                                                self.training_args['den_proj'],
                                                beta=max(self.betas))
        grads = t.gradient(constraint_value, self.tvars)
        return float(constraint_value.numpy()), _get_variables(
                             grads).astype(np.float64)

    def run_mma(self) -> Tuple[xarray.Dataset, List]:
        """Uses GCMMA to train the model.

        Returns
        -------
            An xarray dataset that contains the details of the optimization as
            well as the indices where the weights were saved.
        """
        theta0 = _get_variables(self.tvars).astype(np.float64)

        def wrap_obj_and_constraint_funcs(func):
            """Wraps constraint and objective functions in line with
            the requirements of NLOPT.
            """
            def nlopt_func(x, grad):
                v, g = func(x)
                if grad.size > 0:
                    value, grad[:] = v, g
                else:
                    value = v
                return value
            return nlopt_func

        opt = nlopt.opt(nlopt.LD_MMA, theta0.size)
        # Use explicit bounds for PixelModel variables
        if isinstance(self.model, models.PixelModel):
            opt.set_lower_bounds(0.0)
            opt.set_upper_bounds(1.0)
        else:
            opt.set_lower_bounds(-np.inf)
            opt.set_upper_bounds(np.inf)

        opt.set_min_objective(wrap_obj_and_constraint_funcs(
                              self.objective_and_grad))
        opt.add_inequality_constraint(wrap_obj_and_constraint_funcs(
                              self.constraint, 1e-8))
        opt.set_maxeval(self.max_iterations + 1)
        opt.set_xtol_rel(1e-5)
        opt.optimize(theta0)
        # Convert logits to designs and save all details using xarray
        designs = [self.model.env.render(
                        x,
                        volume_contraint=self.hard_vol_constraint,
                        cone_filter=self.training_args['cone_filter'],
                        den_proj=self.training_args['den_proj'],
                        beta=self.betas[b])
                   for b, x in enumerate(self.opt_details['logits'])]

        # Add other details as well
        ds = optimizer_result_dataset(self.opt_details, designs,
                                      self.save_intermediate_designs)
        return ds, self.indices
