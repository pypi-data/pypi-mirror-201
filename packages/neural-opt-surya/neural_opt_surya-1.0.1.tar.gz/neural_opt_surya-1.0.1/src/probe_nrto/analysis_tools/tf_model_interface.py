"""
Contains an interface class for TF keras models.
This is needed for all analysis experiments.
Modified from the following repo:
https://github.com/cc-hpc-itwm/GradVis

Classes
-------
Tensorflow_NNModel
    An interface between TF keras models and analysis tools.
"""
#                                                                       Modules
# =============================================================================
# Standard
import pickle
from typing import Union

# Third-party
import tensorflow as tf

# Local
from probe_nrto.neural_structural_opt import models
from probe_nrto.neural_structural_opt import train
#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class Tensorflow_NNModel():
    """Provides an interface for TF models to be used with various tools.

    Attributes
    ----------
    model
        Any subclassed model from TF keras.
        Can be CNNModel, PixelModel. etc from models.py
    vol_const_hard
        Whether to apply the hard-volume contraint strategy
    cone_filter
        Whether to apply the cone filtering on the densities
    pixelmodel_init
        Whether to initialize a pixelmodel to calculate
        a loss value for scaling
    pvalue
        SIMP penalty value
    alphaval
        Penalty for enforcing the soft volume constraint

    Methods
    -------
    get_parameters
        Returns the parameters of the current model attribute as a dictionary.
    set_parameters
        Sets a dictionary of weights as the model's state.
    load_parameters
        Load saved pickled weights from hard disk.
    calc_loss
        Calculates the current model's loss.
    _calc_init_loss
        Calculates an initial loss for scaling purposes in
        certain optimizers.
    _tf_params_to_dict
        Converts a model's state into a dictionary of parameters.
    """

    def __init__(self, model : tf.keras.Model,
                 cone_filter: bool = True,
                 vol_const_hard: bool = True,
                 pixelmodel_init: bool = False,
                 pvalue: float = 3.0,
                 alphaval: float = 0.2) -> None:

        """
        Parameters
        ----------
        model
            Converged tensorflow keras models
        filename
            pickled dictionary of weights of converged model

        Returns
        -------
            None
        """
        self.model = model
        self.filter = cone_filter
        self.env = model.env

        self.penalty = pvalue
        self.alphaval = alphaval

        self.vol_const = vol_const_hard
        self.pixelmodel_init = pixelmodel_init
        self._calc_init_loss()

    def get_parameters(self, all_params: bool = True) -> dict:
        """Returns the parameters of the model (basically the model's state).
        There is an option to return all parameters (state)
        or just the trainable ones.

        Parameters
        ----------
        all_params
            Whether to return all the parameters or just the trainable ones.

        Returns
        -------
            A dictionary of parameters with keys as the model's variable names.
        """
        if all_params:
            return self._tf_params_to_dict(all_params=True)
        else:
            return self._tf_params_to_dict(all_params=False)

    def load_parameters(self, filename: str) -> dict:
        """Load saved weights from file.
        The file should be a pickle file containing the parameters of the model
        as a dictionary with keys as the variable names and values
        as the list of Tensors

        Parameters
        ----------
        filename
            The path to the saved file.

        Returns
        -------
            The loaded value from the file.
        """
        lis_var_file = pickle.load(open(filename, 'rb'))
        return lis_var_file

    def set_parameters(self, parameter_dict: dict) -> None:
        """Set parameters to a model.
        Since we set the state of the model, we need all the parameters.

        Parameters
        ----------
        parameter_dict
            A dictionary for the parameters of the model.
            E.g. parameter_dict = {'Variable:0' : [tf.Tensor, tf.Tensor],
                                    'dense/kernel:0' : [tf.Tensor],
                                    ....}
        Returns
        -------
            None.
        """
        if not isinstance(self.model, models.PixelModel):
            for i, layer in enumerate(self.model.core_model.layers):
                if layer.variables == []:
                    continue
                else:
                    wt_names = [wt.name for wt in layer.variables]
                    templst = [arr for k, arr in parameter_dict.items()
                               if k in wt_names]
                    layer.set_weights(templst)
            if isinstance(self.model, models.CNNModel_c2dt_corr) \
               or isinstance(self.model, models.CNNModel):
                # The beta vector (self.z) in CNNModel is trainable
                self.model.z.assign(parameter_dict['z:0'])
        else:
            # Only one variable for PixelModel
            self.model.z.assign(parameter_dict['Variable:0'])

    def calc_loss(self, diffn: bool = False) -> Union[tf.Tensor, float]:
        """Calculates the loss based on the current model state.
        This utilizes the Class attributes to determine the filtering,
        SIMP penalty, volume constraint enforcing strategy etc.

        Parameters
        ----------
        diffn
            Whether to allow differentiation of the loss calculating process.
            If yes, the loss calculated can be backproped.

        Returns
        -------
            loss
                The model's loss value as either a tf.tensor or numpy float.
        """
        if self.vol_const:
            logits = self.model(None)
            # calculates just the compliance
            J = self.model.loss(logits, vol_const_hard=self.vol_const,
                                cone_filter=self.filter, p=self.penalty)
            loss = J
        else:
            # Uses soft volume constraint - uses a model scaling factor J0
            logits = self.model(None)
            J = self.model.loss(logits, vol_const_hard=self.vol_const,
                                cone_filter=self.filter, p=self.penalty)
            cur_density = train.mean_density(logits,
                                             self.env.args, self.filter)
            loss = tf.cast(self.alphaval*((
                           cur_density/self.env.args['volfrac']) - 1)**2,
                           dtype=tf.float64) + J/self.model.J0
        if diffn:
            return loss
        else:
            return loss.numpy().item()

    def _calc_init_loss(self) -> None:
        """Calculates the initial compliance of the model for scaling."""
        if self.pixelmodel_init:
            pix_mdl = models.PixelModel(seed=0, args=self.model.env.args)
            pix_logits = pix_mdl(None)
            J0 = pix_mdl.loss(pix_logits, False, False, 3.0)
            self.model.J0 = J0.numpy().item()
        else:
            self.model.J0 = self.model.loss(self.model(None), self.vol_const,
                                            self.filter,
                                            self.penalty).numpy().item()

    def _tf_params_to_dict(self, all_params: bool = True) -> dict:
        """Extracts the variables from a TF model into a dictionary."""
        new_param = dict()
        if all_params:
            lis_tv = self.model.variables
        else:
            lis_tv = self.model.trainable_variables

        for i, var in enumerate(lis_tv):
            if all_params:
                key = self.model.variables[i].name
            else:
                key = self.model.trainable_variables[i].name
            new_param[key] = var.numpy()
        return new_param
