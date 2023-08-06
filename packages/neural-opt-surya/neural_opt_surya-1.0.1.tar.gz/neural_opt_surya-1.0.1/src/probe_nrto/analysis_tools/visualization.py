"""
Make 2D projections of the loss landscape of neural network models.

Based on the paper by Li et al
    Visualizing the Loss Landscape of Neural Nets
    https://arxiv.org/pdf/1712.09913.pdf
These functions were modified from the github repo:
    https://github.com/cc-hpc-itwm/GradVis

Functions
---------
visualize
    Wrapper for _visualize function.
_visualize
    Main function to visualize loss landscapes and trajectories.
vectoriz
    Reshapes vector into model's parameters' shape.
flatten_parameter_list
    Concatenates a List of numpy arrays into a single, flat numpy array.
get_pca_vec
    Performs PCA on a set of model parameters.
cont_loss
    Calculates the loss values at several grid points.
give_coefs
    Projects iterates onto the plane spanned by two vectors.
normalize
    Normalizes the vectors spanning the 2D space
cosine_similarity
    Checks the orthogonality of two vectors.
"""
#                                                                       Modules
# =============================================================================
# Standard
import warnings
from typing import Union, Tuple, List

# Third-party
import numpy as np
from pathlib import Path
from sklearn.decomposition import PCA
from scipy import sparse
from scipy.sparse import linalg

# Local
from . import tf_model_interface
# from tf_model_interface import Tensorflow_NNModel
#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S', 'Avraam Chatzimichailidis et al.']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================
Tensorflow_NNModel = tf_model_interface.Tensorflow_NNModel


def visualize(interface_model: Tensorflow_NNModel,
              filenames: List[str] = [], resolution: int = 50,
              path_to_file: str = './visual_data', random_dir: bool = True,
              magnification : float = 1.0,
              v_vec: List = [], w_vec: List = []) -> None:
    """Wrapper for _visualize function.

    Saves results as npz (numpy_compressed) file.

    Parameters
    ----------
    interface_model
        Tensorflow model interface.
    filenames
        List of checkpoint names (files with parameters),
        orderered with the centerpoint last in list. This is used
        only for calculating PCA plots.
    resolution
        Number of grid points for plotting along one axis.
    path_to_file
        Path and filename where the results are going to be saved at.
    random_dir
        If random directions should be used instead of PCA.
    magnification
        Margins for visualized space (in %)
    v_vec, w_vec
        If defined, custom vectors will be used instead of PCA.

    Returns
    -------
        None
    """
    my_file = Path(path_to_file+".npz")
    if my_file.is_file():
        print("File {} already exists!".format(path_to_file+".npz"))
    else:
        outputs, flag = _visualize(interface_model, filenames, resolution,
                                   random_dir=random_dir,
                                   magnification=magnification,
                                   v_vec=v_vec, w_vec=w_vec,
                                   )
        np.savez_compressed(path_to_file, a=outputs, b=flag)


def _visualize(interface_model: Tensorflow_NNModel,
               filenames: List[str], resolution: int,
               random_dir: bool = False, magnification : float = 0.5,
               v_vec: List = [],
               w_vec: List = []) -> Tuple[List[np.ndarray], int]:
    """Main function to visualize loss landscapes and trajectories.

    Projects the loss landscape into 2 directions and embeds
    the trajectory of the optimizer in this place. Since the trajectory
    is meangingful only for non-random directions, it is not calculated
    when filter-normalized random directions are used as the axes.

    Parameters
    ----------
    interface_model
        Tensorflow model interface. Assumes that the model is
        converged since the parameters are treated as the origin of plane of
        projection for filter-normalized random projection.
    filenames
        List of checkpoint names (files with parameters),
        orderered with the centerpoint last in list. This is used
        only for calculating PCA plots.
    resolution
        Number of grid points for plotting along one axis.
    random_dir
        If random directions should be used instead of PCA.
    magnification
        Margins for visualized space (in %)
    v_vec, w_vec
        If defined, custom vectors will be used instead of PCA.

    Returns
    -------
        Array containing loss values, path values, variance data
        and the two pca components.
        Also a flag value is returned.
        1 - Vectors were provided
            Returns [x coordinates of the plane, y coordinates of the plane,
            loss value at each of the points,
            x-coordinates of the trajectory, y coordinates of the trajectory,
            loss at each point of the trajectory]
        2 - PCA directions
            Returns the same as above. In addition, the calculated PCA vectors
            and the variance explained by them are also returned.
        3 - Filter normalized random directions.
            Returns [x coordinates of the plane, y coordinates of the plane,
            loss value at each of the points, random_dir_1, random_dir_2]
    """
    # Load all the parameters of the model
    parameter = interface_model.get_parameters()
    parlis = list(parameter.values())
    # If the directions are provided, use them
    if len(v_vec) != 0 and len(w_vec) != 0:
        v = v_vec
        w = w_vec
    elif random_dir:
        # Random filter normalized directions
        total_params = sum(np.size(p) for p in parlis)
        warn = False
        for i in range(51):  # 50 tries to make it perpendicular!
            if i == 0 or warn:
                v = np.random.normal(size=total_params)
                w = np.random.normal(size=total_params)
                # Converts flattened vector to a list with the
                # same structure as the model's parameters
                get_v = vectoriz(v, parlis)
                get_w = vectoriz(w, parlis)
                # Filter normalize the directions
                get_v, get_w = normalize(parameter, get_v, get_w)
                # check orthogonality
                warn = cosine_similarity(get_v, get_w)
        if warn:
            print("Unsuccessful orthogonality")
        else:
            print('Successfully normalized')
    else:
        # Choose PCA directions
        v, w, pca_variance = get_pca_vec(
                    interface_model, filenames)
        get_v = vectoriz(v, parlis)
        get_w = vectoriz(w, parlis)

    if not random_dir:
        # Plot trajectories on the loss landscape
        # using previously stored parameters
        v = flatten_parameter_list(get_v)
        w = flatten_parameter_list(get_w)
        coefs = give_coefs(interface_model, filenames, parameter, v, w)
        coefs = np.array(coefs)  # 2 coeffs for each iterate

        paths = []
        for val in range(len(coefs)):
            #  Loss for a given point (coeff_x,coeff_y)
            yo = cont_loss(interface_model, parameter,
                           [coefs[val][0]], coefs[val][1],
                           get_v, get_w)
            paths.append(yo)

        paths = np.array(paths)
        coefs_x = coefs[:, 0][np.newaxis]
        coefs_y = coefs[:, 1][np.newaxis]
        boundaries_x = max(coefs_x[0])-min(coefs_x[0])
        boundaries_y = max(coefs_y[0])-min(coefs_y[0])

        x = np.linspace(min(coefs_x[0]) - magnification*boundaries_x,
                        max(coefs_x[0]) + magnification*boundaries_x,
                        resolution)
        y = np.linspace(min(coefs_y[0]) - magnification*boundaries_y,
                        max(coefs_y[0]) + magnification*boundaries_y,
                        resolution)
    else:
        boundaries_x = 1.0
        boundaries_y = 1.0

        x = np.linspace(-magnification*boundaries_x,
                        magnification*boundaries_x,
                        resolution)
        y = np.linspace(-magnification*boundaries_y,
                        magnification*boundaries_y,
                        resolution)
    X, Y = np.meshgrid(x, y)
    Z = []
    # Calculating loss at the projected landscape grid
    for i in range(len(y)):
        vals = cont_loss(interface_model,
                         parameter,
                         X[i], Y[i][0],
                         get_v, get_w)
        Z.append(vals)
    if not random_dir:
        if len(v_vec) != 0 and len(w_vec) != 0:
            return [(X, Y, np.vstack(Z)),
                    (coefs_x[0], coefs_y[0], paths.T[0])], 1
        else:
            cache = (pca_variance, v, w)
            return [(X, Y, np.vstack(Z)),
                    (coefs_x[0], coefs_y[0], paths.T[0]), cache], 2
    else:
        cache = (v, w)
        return [(X, Y, np.vstack(Z)) , cache], 3


def vectoriz(flat_vector: np.array,
             parameter_list: List[np.ndarray]) -> List[np.ndarray]:
    """Reshapes vector into model's parameters' shape.

    Parameters
    ----------
    flat_vector
        Unstructured flat vector
    parameter_list
        List of numpy arrays (target shape)

    Returns
    -------
        List of numpy arrays, with data from flat_vector and
        shape like parameter_list
    """
    vector = []
    indic = 0
    for p in parameter_list:
        len_p = p.size
        p_size = p.shape
        vec_it = flat_vector[indic:(indic+len_p)].reshape(p_size)
        vector.append(np.array(vec_it, dtype=np.float32))
        indic += len_p
    return vector


def flatten_parameter_list(parameter_list: List[np.ndarray]) -> np.array:
    """Concatenates a List of numpy arrays into a single, flat numpy array.

    Parameters
    ----------
    parameter_list
        List of model's parameters

    Returns
    -------
        Flattened array of the model's parameters
    """
    return np.concatenate([ar.flatten() for ar in parameter_list], axis=None)


def get_pca_vec(interface_model: Tensorflow_NNModel,
                filenames: List[str]) -> Tuple[np.array, np.array, float]:
    """Performs PCA on a set of model parameters.

    Parameters
    ----------
    interface_model
        Tensorflow interface model.
    filenames
        filenames of the iterates to be included into the PCA.
        Assumes that the filenames are ordered according to the
        iteration history (from initialization to convergence)

    Returns
    -------
        Two vectors with highest variance
    """
    mats = []
    for file in filenames:
        testi = interface_model.load_parameters(file)
        parlis = np.ndarray([0])
        for key in testi:
            if "moving" in key:
                # Do not consider non-trainable moving statistics
                testi[key] *= 0
            parlis = np.concatenate((parlis, testi[key]), axis=None)
        pas = parlis
        mats.append(pas)
    mats = np.vstack(mats)  # Shape of (n_indices, n_params)
    mats_new = mats[:-1]-mats[-1]
    data = mats_new
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(data.T)
    print("Explained ratio ", pca.explained_variance_ratio_)

    return (np.array(principalComponents[:, 0]),
            np.array(principalComponents[:, 1]), pca.explained_variance_ratio_)


def cont_loss(interface_model: Tensorflow_NNModel,
              parameter: dict, alph: List[float],
              bet: float,
              get_v: List[np.ndarray],
              get_w: List[np.ndarray]) -> np.array:
    """Calculates the loss values at several grid points.

    Changes the internal state of model. Executes model.
    Theta* = Theta + alpha * v + beta * w, where Theta is the
    model's parameters, alpha and beta are the perturbations along
    directions v and w respectively.

    Parameters
    ----------
    interface_model
        Tensorflow model interface
    parameter
        Dictionary of parameters of the model.
        Forms the centre of the plane i.e. this is the point
        that get perturbed to calculate the loss landscape.
    alph
        List of scalars for 1st direction/alpha in paper --grid coords
    bet
        Scalar for 2nd direction/beta in paper
    get_v
        1st direction
    get_w
        2nd direction

    Returns
    -------
    loss_vals
        Loss values at the calculated points.
    """
    loss_vals = []
    for al in alph:
        testi_clone = parameter.copy()
        ind = 0
        # calculate new parameters for model by perturbing
        for key in parameter:
            testi_clone[key] += al*get_v[ind] + bet*get_w[ind]
            ind += 1
        # load parameters into model and calcualte loss
        interface_model.set_parameters(testi_clone)
        loss = interface_model.calc_loss()
        loss_vals = np.append(loss_vals, loss)
    return loss_vals


def give_coefs(interface_model: Tensorflow_NNModel,
               filenames: List[str],
               parameter: dict,
               v: np.array, w: np.array) -> Tuple:
    """Projects iterates onto the plane spanned by two vectors.

    Once a place is defined, the saved iterates corresponding to the
    trajectory of the optimizer is projected onto this plane using a least
    squares regression.
    Note: Needs a converged model! --'pas' variable uses this implicitly
    i.e. Assumes that the current state of the model is the last iterate.

    Parameters
    ----------
    interface_model
        tensorflow interface model.
    filenames
        Checkpoint files, which define the trajectory.
    parameter
        Central point, to which the trajectory will be calculated.
    v
        1st vector spanning the 2D space
    w
        2nd vector spanning the 2D space

    Returns
    -------
        list of coefficients in the plane
    """
    matris = [v, w]
    matris = np.vstack(matris)
    matris = matris.T  # shape of (n_params, 2)

    parlis = list(parameter.values())
    pas = flatten_parameter_list(parlis)
    coefs = []
    for file in filenames:
        par_step = interface_model.load_parameters(file)
        parstep = list(par_step.values())
        st = flatten_parameter_list(parstep)
        b = st - pas
        coefs.append(np.hstack(np.linalg.lstsq(matris, b, rcond=None)[0]))
    # Find x S.T -> matris @ x =  b
    # solution - n_pars x 2 @ 2 x 1 = n_pars, 1
    return (coefs)


def normalize(parameter: dict, get_v: List[np.ndarray],
              get_w: List[np.ndarray]) -> Tuple[List[np.ndarray]]:
    """Normalizes the vectors spanning the 2D space.

    Performs filter-normalization as per :
    Visualizing the Loss Landscape of Neural Nets
    (https://arxiv.org/abs/1712.09913)

    Parameters
    ----------
    parameter
        The parameters to normalize to.(The point of interest
        - centre of the plane)
    get_v, get_w
        The vectors in the 2D space, which should be normalized to 'parameter'.

    Returns
    -------
        Tuple of normalized vectors get_v, get_w.
    """

    parlis = list(parameter.values())
    parnames = list(parameter.keys())

    for i in range(len(parlis)):
        # Don't consider non-trainable parameters of batch normalization
        if 'moving' in parnames[i]:
            get_v[i] = get_v[i]*0
            get_w[i] = get_w[i]*0
        else:
            # For fully-connected layers
            # The FC layer is equivalent to a Conv layer with a 1 × 1
            # output feature map and the filter corresponds to the weights
            # that generate one neuron.
            if 'dense/kernel' in parnames[i]:
                for j in range(parlis[i].shape[1]):
                    factor_v = np.linalg.norm(parlis[i][:, j])/(
                                np.linalg.norm(get_v[i][:, j]) + 1e-10)
                    factor_w = np.linalg.norm(parlis[i][:, j])/(
                                np.linalg.norm(get_w[i][:, j]) + 1e-10)
                    get_v[i][:, j] = get_v[i][:, j] * factor_v
                    get_w[i][:, j] = get_w[i][:, j] * factor_w
            else:
                factor_v = np.linalg.norm(parlis[i])/(
                            np.linalg.norm(get_v[i]) + 1e-10)
                factor_w = np.linalg.norm(parlis[i])/(
                            np.linalg.norm(get_w[i]) + 1e-10)
                #  returns 2-norm
                get_v[i] = get_v[i]*factor_v
                get_w[i] = get_w[i]*factor_w
    return get_v, get_w


def cosine_similarity(vec_a: List[np.ndarray],
                      vec_b: List[np.ndarray]) -> bool:
    """Checks the orthogonality of two vectors.

    Parameters
    ----------
    vec_a, vec_b
        Two vectors to be checked.

    Returns
    -------
        Whether they are sufficiently orthogonal or not.
    """
    a = flatten_parameter_list(vec_a)
    b = flatten_parameter_list(vec_b)
    # find the cosine of the angle between them
    costheta = np.dot(a, b)/(np.linalg.norm(a) * np.linalg.norm(b))
    print("The angle between chosen directions is ",
          np.arccos(costheta)*180/np.pi)
    warn = False
    if np.abs(costheta - 0) >= 1e-2:
        # They are not orthogonal
        warn = True
    return warn
