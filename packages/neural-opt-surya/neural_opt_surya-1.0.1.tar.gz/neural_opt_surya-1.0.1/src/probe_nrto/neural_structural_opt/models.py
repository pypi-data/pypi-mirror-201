# Copyright 2019 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Contains all the models tested for neural reparameterization.

Classes
-------
Model
    Base model for all other models.
PixelModel
    A conventional model without any neural network.
TounnModel
    TOuNN and F-TOuNN fully connected models.
TounnModelFS
    Modification to F-TOuNN that uses Fourier series.
CNNModel
    Hoyer's convolutional network model.
CNNModel_c2dt_corr
    Hoyer's CNNModel corrected to allow twice differentiability.
AddOffSet
    A keras layer used for offsetting an input

Functions
---------
batched_topo_loss
    Runs the topology optimization and return the compliance.
convert_autograd_to_tensorflow
    handshaking function between autograd and Tensorflow
set_random_seed
    Sets the random state for Tensorflow, python and numpy.
global_normalization
    A layer that uses mean and standard deviation to normalize.
Conv2D
    A convolutional layer
Conv2DT
    A transposed convolutional layer
UpSampling2D
    Layer that enlarges the image.

Note: Issue with using Conv2D layer - It is not twice differentiable.
https://github.com/tensorflow/tensorflow/issues/22208
regsiter gradient for bilinear resize
"""
#                                                                       Modules
# =============================================================================

# Standard
import random as py_random

# Third-party
import autograd
import autograd.core
import autograd.numpy as np
from autograd import elementwise_grad as egrad
import tensorflow as tf

# Locals
from . import topo_api
#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


def batched_topo_loss(params: tf.Tensor, envs: list,
                      vol_const_hard: bool = True,
                      cone_filter: bool = True, p: float = 3.0,
                      den_proj: bool = False, beta: float = 1):
    """Calculates loss from a model's output using FE analysis.

    Parameters
    ----------
    params
        Output of model
    envs
        List of environments
    vol_const_hard
        Whether to apply the hard-volume contraint strategy
    cone_filter
        Whether to apply the cone filtering on the densities
    p
        SIMP penalty factor to be used
    den_proj
        Whether to use density projection
    beta
        Density projection parameter.

    Returns
    -------
        loss: Compliance or Compliance + Volume constraint violation

    """
    losses = [env.objective(params[i], volume_contraint=vol_const_hard,
                            cone_filter=cone_filter, p=p, den_proj=den_proj,
                            beta=beta) for i, env in enumerate(envs)]
    return np.stack(losses)


def convert_autograd_to_tensorflow(func):
    """Handshakes functions written in Autograd to Tensorflow.
    This allows the gradients to flow from the physics to
    update the networks' weights.
    Main difference from Hoyer's work : Added the inner function -
                Allows twice differentiability of the entire graph.
    Warning:
        If 'func' is a vector-valued function, the jacobian returned
        is summed over (due to the presence of egrad). If you want accurate
        Jacobians, comment out the inner first_grad function and make the
        wrapper return ans, vjp directly.

    Parameters
    ----------
    func
        A function written completely in Autograd.numpy

    Returns
    -------
    wrapper
        A wrapper around the original function 'func' which allows
        tf tensor as input to 'func' and returns correct gradients
    """
    @tf.custom_gradient
    def wrapper(x):
        vjp, ans = autograd.core.make_vjp(func, x.numpy())

        #  Define the gradient and hessian of 'func'
        def first_grad(dy):
            @tf.custom_gradient
            def jacobian(a):
                vjp2, ans2 = autograd.core.make_vjp(egrad(func), a.numpy())
                return ans2, vjp2  # hessian
            return dy * jacobian(x)

        return ans, first_grad

    return wrapper


def set_random_seed(seed: int) -> None:
    """Set the gloabl random state.

    Parameters
    ----------
    seed
        A function written completely in Autograd.numpy

    Returns
    -------
    None
    """
    if seed is not None:
        py_random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)


class Model(tf.keras.Model):
    """Base model for all other models.
    Allows model sub-classing to create Keras models.

    Attributes
    ----------
    seed
        Set the global state for randomness
    args
        Dictionary with details about the boundary conditions.
        Can be created 'using topo_api.py' file.
    env
        An object of the Environment class
    J0
        Intial compliance value - Useful for scaling.
        Calculated at the start of optimization

    Methods
    -------
    loss(self, logits, other_arguments)
        Calculates the loss using the current model's outputs
    """

    def __init__(self, seed: int = None, args : dict = None) -> None:
        super().__init__()
        set_random_seed(seed)
        self.seed = seed
        self.env = topo_api.Environment(args)
        # Initial compliance for scaling purposes
        self.J0 = 0.0

    def loss(self, logits: tf.Tensor, vol_const_hard: bool = True,
             cone_filter: bool = True, p: float = 3.0,
             den_proj: bool = False, beta: float = 1):
        """Calculates the loss using the model's output

        Parameters
        ----------
        logits
            Output of model
        vol_const_hard
            Whether to apply the hard-volume contraint strategy
        cone_filter
            Whether to apply the cone filtering on the densities
        p
            SIMP penalty factor to be used
        den_proj
            Whether to use density projection
        beta
            Density projection parameter.

        Returns
        -------
            loss: Compliance or Compliance + Volume constraint violation
        """
        # for our neural network, we use float32, but we use float64
        # for the physics
        # to avoid any chance of overflow.
        # add 0.0 to work-around bug in grad of tf.cast on NumPy arrays
        logits = 0.0 + tf.cast(logits, tf.float64)
        f = lambda x: batched_topo_loss(x, [self.env],
                                        vol_const_hard=vol_const_hard,
                                        cone_filter=cone_filter, p=p,
                                        den_proj=den_proj, beta=beta)
        losses = convert_autograd_to_tensorflow(f)(logits)
        return tf.reduce_mean(losses)


class PixelModel(Model):
    """Dummy model for conventional topology optimization.
    Named as PixelModel because the model's variables are
    arranged as in an image [representing the density].

    Attributes
    ----------
    z
        The model's parameters

    Methods
    -------
    call(self, inputs)
        Simply returns the model's parameters as the output.
        This function is required by tensorflow
    """

    def __init__(self, seed: int = None, args : dict = None) -> None:
        super().__init__(seed, args)
        shape = (1, self.env.args['nely'], self.env.args['nelx'])
        z_init = np.broadcast_to(args['volfrac'] * args['mask'], shape)
        self.z = tf.Variable(z_init, trainable=True, dtype=tf.float32)

    def call(self, inputs=None):
        return self.z


#                                                         TOuNN & F-TOuNN Model
# =============================================================================
layers = tf.keras.layers


class TounnModel(Model):
    """Fully connected neural network models.
    This single model functions as both the TOuNN and the F-TOuNN models.
    1. https://github.com/UW-ERSL/TOuNN
    2. https://github.com/UW-ERSL/Fourier-TOuNN
    Both are coordinate-based networks representing the density field.
    TOuNN maps (x,y) in the design domain to density at that point
    F-TOuNN projects (x,y) using random Fourier features and uses this
    high dimensional vector as the input.

    Attributes
    ----------
    core_model
        The Keras model from the inputs to the output
    outputDim
        The output size of the neural network
    coordnMap
        The multplication matrix for different types of sampling.
    xy
        (x, y) coordinates in a grid on the design domain

    Methods
    -------
    call
        Forward pass through the network.
    generatePoints
        Generates (x,y) points based on grid in domain.
    applyFourierMapping
        Converts (x,y) coordinates to random fourier features.
    normalize
        Converts the (x,y) coordinates to lie between -1 and 1.
    """
    outputDim = 1  # if material/void at the point

    def __init__(self, seed: int = 0, args: dict = None,
                 depth: int = 1, width: int = 20,
                 fourier_features: bool = True, no_ffeatures: int = 150,
                 sampling: dict = {'default': (6, 30)},
                 vol_const_hard: bool = False,
                 var_batch: bool = False, resolution: int = 1,
                 normalize: bool = False
                 ):
        """Defining the TOuNN and F-TouNN models using Keras.
        Creates a dense neural network model based on the parameters chosen.

        Parameters
        ----------
        seed
            Sets the global random state
        args
            Details about the boundary condition.
        depth
            Number of network hidden layers
        width
            Number of neurons in each hidden layer
        fourier_features
            Whether to use random Fourier features.
            True would imply using the F-TOuNN model
        no_ffeatures
            Number of fourier features to project onto.
            Only applicable for F-TOuNN (Needs 'fourier_features' to be True).
        sampling
            Details of the distrbution from which sampling of
            random fourier features has to be done
            (Needs 'fourier_features' to be True).
            The format adopted is{'key' : (param1, param2)},
            where param1 and param2 are the distribution's parameters
            Options (Possible 'key's):
                'default': Disjoint uniform distribution (as in the paper)
                    param1 - rmin
                    param2 - rmax
                'gaussian': Gaussian distribution
                    param1 - mean
                    param2 - std
                'uniform': Uniform distribution
                    param1 - lower limit
                    param2 - higher limit
                'fixed-k': Non-random distribution. Samples points such that
                          the magnitude of the wave vector is constant
                    param1 - wave vector magnitude
                    param2 - None
                'fixed-dir': Non-random distribution. Samples points such that
                            the direction of the wave vector is constant
                    param1 - Angle in degrees (w.r.t x axis)
                    param2 - None
        var_batch
            Whether to use variable_batch.
            This sets the Batchnorm layer to inference mode.
            When set to True, allows sampling a trained model
            at intermediate points.
        resolution
            The resolution at which points are sampled in the design domain.
            resolution=1 means the nelx*nely points are sampled
        normalize
            Whether to normalize the inputs for TOuNN model to [-1,1]

        Returns
        -------
            None
        """
        super().__init__(seed, args)
        self.seed = seed
        self.args = args
        h = self.args['nely']
        w = self.args['nelx']
        hw = h*w
        if fourier_features:
            # (cos + sine) x n_fourier_features
            inputDim = 2*no_ffeatures
        else:
            inputDim = 2  # (x,y) only
        if var_batch:  # for inference - variable batch size
            bs = resolution**2 * hw
            net = inputs = layers.Input((inputDim,), batch_size=bs)
        else:
            assert resolution == 1
            # h * w # only works with resolution = 1
            net = inputs = layers.Input((inputDim,), batch_size=hw)

        initializer = tf.keras.initializers.GlorotNormal()
        for i in range(depth):
            net = layers.Dense(
                            units=width,
                            kernel_initializer=initializer,
                            bias_initializer='zeros',
                            activation=None)(net)
            if var_batch:
                net = layers.BatchNormalization(
                            momentum=0.01)(net, training=False)
            else:
                net = layers.BatchNormalization(
                            momentum=0.01)(net, training=True)
            # to be consistent with PyTorch
            net = tf.nn.leaky_relu(net, alpha=0.01)

        net = layers.Dense(
                        units=self.outputDim, kernel_initializer=initializer,
                        bias_initializer='zeros', activation=None)(net)
        # Use sigmoid to restrict densities between 0 and 1
        if not vol_const_hard:
            net = tf.keras.layers.Activation("sigmoid")(net)

        if var_batch:
            output = tf.transpose(
                            tf.reshape(
                                    net,
                                    [1, resolution*w, resolution*h]),
                            perm=[0, 2, 1])
        else:
            output = tf.transpose(tf.reshape(net, [1, w, h]), perm=[0, 2, 1])
        # Make the model
        self.core_model = tf.keras.Model(inputs=inputs, outputs=output)
        # Generate the xy coordinates in the domain
        self.xy = self.generatePoints(self.args['nelx'], self.args['nely'],
                                      width=args['width'],
                                      height=args['height'],
                                      resolution=resolution)
        # Project the xy coordinates using random fourier features (RFF)
        if fourier_features:
            # Default strategy presented in the paper
            if list(sampling.keys())[0] == 'default':
                coordnMap = np.zeros((2, no_ffeatures))
                rmin = sampling['default'][0]
                rmax = sampling['default'][1]
                for i in range(coordnMap.shape[0]):
                    for j in range(coordnMap.shape[1]):
                        coordnMap[i, j] = np.random.choice([-1., 1.]) * \
                                np.random.uniform(1./(2*rmax), 1./(2*rmin))
            elif list(sampling.keys())[0] == 'gaussian':
                mean = sampling['gaussian'][0]
                sigma = sampling['gaussian'][1]
                coordnMap = np.random.normal(scale=sigma,
                                             size=(2, no_ffeatures), loc=mean)
            elif list(sampling.keys())[0] == 'uniform':
                low_lim = sampling['uniform'][0]
                upp_lim = sampling['uniform'][1]
                coordnMap = np.random.uniform(low=low_lim,
                                              size=(2, no_ffeatures),
                                              high=upp_lim)
            elif list(sampling.keys())[0] == 'fixed-k':
                r_med = sampling['fixed-k'][0]
                xvals = np.linspace(0.001, r_med, int(no_ffeatures/2))
                yvals1 = np.sqrt(r_med**2 - xvals**2)
                yvals2 = -1 * yvals1
                x = np.hstack([xvals, xvals])
                y = np.hstack([yvals1, yvals2])
                coordnMap = np.vstack([x, y])
            else:
                slope = np.tan(sampling['fixed-dir'][0] * np.pi/180)  # y=mx
                lim = np.sqrt(1/(1+slope**2))
                xvals = np.linspace(0, lim, int(no_ffeatures))
                yvals = slope * xvals
                coordnMap = np.vstack([xvals, yvals])
            # RFF matrix
            self.coordnMap = tf.constant(coordnMap)
            # Input for F-TouNN
            self.z = self.applyFourierMapping(self.xy)
        else:  # for TouNN
            if normalize:
                self.z = self.normalize(self.xy)
            else:
                self.z = self.xy

    def call(self, inputs=None):
        """The forward pass through the model.
        The inputs argument has no role.
        """
        return self.core_model(self.z)

    def generatePoints(self, nelx: int, nely: int,
                       resolution: int = 1,
                       width: int = 20, height: int = 20):
        """Generate (x,y) coordinates in the domain.
        From up to bottom, row major - similar to FEM element numbering
        as per 88 lines code.

        Parameters
        ----------
        nelx
            Number of elements in the x direction
        nely
            Number of elements in the y direction
        resolution
            The multiplication factor to sample more points.
            nelx and nely are multipleid with this value
            if resolution=3 and nelx=10, 30 values will be sampled along
            x axis.
        width
            The physical width of the domain
        height
            The physical height of the domain

        Returns
        -------
        xy
            The (x,y) coordinates of all the sampled points,
            from top-left to top down - columnwise
        """
        ctr = 0
        xy = np.zeros((resolution*nelx*resolution*nely, 2))
        for i in range(resolution*nelx):
            for j in range(resolution*nely):
                xy[ctr, 0] = (i + 0.5)/resolution
                xy[ctr, 1] = (resolution*nely - j - 0.5)/resolution
                ctr += 1
        xy[:, 0] = (xy[:, 0]/nelx)*width
        xy[:, 1] = (xy[:, 1]/nely)*height
        return xy

    def applyFourierMapping(self, x: np.ndarray):
        """Converts (x,y) coordinates to random fourier features.
        Parameters
        ----------
        x
            The output of generatePoints() function.
            Matrix of (x,y) coordinates

        Returns
        -------
        xv
            Transformed features
        """
        c = tf.cos(2*np.pi*tf.matmul(x, self.coordnMap))  # (hw, n_features)
        s = tf.sin(2*np.pi*tf.matmul(x, self.coordnMap))
        xv = tf.concat((c, s), axis=1)  # (hw, 2*n_features)
        return xv

    def normalize(self, xy):
        ulx = self.args['width']
        uly = self.args['height']

        x = xy[:, 0]
        y = xy[:, 1]
        #  scale x
        xnew = (2*x/ulx) - 1
        #  scale y
        ynew = (2*y/uly) - 1
        return np.array([xnew, ynew]).T


class TounnModelFS(Model):
    """Fully connected neural network model with fourier series input.

    Attributes
    ----------
    core_model
        The Keras model from the inputs to the output
    outputDim
        The output size of the neural network
    coordnMap
        The multplication matrix for different types of sampling.
    xy
        (x, y) coordinates in a grid on the design domain

    Methods
    -------
    call
        Forward pass through the network.
    generatePoints
        Generates (x,y) points based on grid in domain.
    applyFourierMapping
        Converts (x,y) coordinates to random fourier features.
    normalize
        Converts the (x,y) coordinates to lie between -1 and 1.
    """
    outputDim = 1  # if material/void at the point

    def __init__(self, seed=0, args=None, depth: int = 1,
                 width: int = 20, n_terms: int = 5,
                 one_D: bool = True,
                 vol_const_hard: bool = False,
                 var_batch: bool = False, resolution: int = 1):
        super().__init__(seed, args)
        self.seed = seed
        self.args = args
        h = self.args['nely']
        w = self.args['nelx']
        if one_D:
            # (cos + sine) x n_fourier_features x 2 --> for x and y
            inputDim = 4 * n_terms
        else:
            inputDim = n_terms**2
        hw = h*w
        if var_batch:  # for inference - variable batch size
            bs = resolution**2 * hw
            net = inputs = layers.Input((inputDim,), batch_size=bs)
        else:
            assert resolution == 1
            #  h * w  only works with resolution = 1
            net = inputs = layers.Input((inputDim,), batch_size=hw)

        initializer = tf.keras.initializers.GlorotNormal()
        for i in range(depth):
            net = layers.Dense(units=width,
                               kernel_initializer=initializer,
                               bias_initializer='zeros', activation=None)(net)
            if var_batch:
                net = layers.BatchNormalization(momentum=0.01)(
                                        net, training=False)
            else:
                net = layers.BatchNormalization(momentum=0.01)(
                                        net, training=True)
            #  to be consistent with PyTorch
            net = tf.nn.leaky_relu(net, alpha=0.01)
        net = layers.Dense(units=self.outputDim,
                           kernel_initializer=initializer,
                           bias_initializer='zeros', activation=None)(net)
        if not vol_const_hard:
            net = tf.keras.layers.Activation("sigmoid")(net)
        if var_batch:
            output = tf.transpose(tf.reshape(
                                    net, [1, resolution * w, resolution * h]),
                                  perm=[0, 2, 1])
        else:
            output = tf.transpose(tf.reshape(net, [1, w, h]), perm=[0, 2, 1])
        self.core_model = tf.keras.Model(inputs=inputs, outputs=output)

        self.xy = self.generatePoints(
                            self.args['nelx'], self.args['nely'],
                            width=args['width'], height=args['height'],
                            resolution=resolution)
        if one_D:
            self.z = self.apply1DFourierSeries(self.xy, n_terms)
        else:
            self.z = self.apply2DFourierSeries(self.xy, n_terms)

    def call(self, inputs=None):
        return self.core_model(self.z)

    def generatePoints(self, nelx: int, nely: int,
                       resolution: int = 1,
                       width: int = 20, height: int = 20):
        """Generate (x,y) coordinates in the domain.
        From up to bottom, row major - similar to FEM element numbering
        as per 88 lines code.

        Parameters
        ----------
        nelx
            Number of elements in the x direction
        nely
            Number of elements in the y direction
        resolution
            The multiplication factor to sample more points.
            nelx and nely are multipleid with this value
            if resolution=3 and nelx=10, 30 values will be sampled along
            x axis.
        width
            The physical width of the domain
        height
            The physical height of the domain

        Returns
        -------
        xy
            The (x,y) coordinates of all the sampled points,
            from top-left to top down - columnwise
        """
        ctr = 0
        xy = np.zeros((resolution*nelx*resolution*nely, 2))
        for i in range(resolution*nelx):
            for j in range(resolution*nely):
                xy[ctr, 0] = (i + 0.5)/resolution
                xy[ctr, 1] = (resolution*nely - j - 0.5)/resolution
                ctr += 1
        xy[:, 0] = (xy[:, 0]/nelx)*width
        xy[:, 1] = (xy[:, 1]/nely)*height
        return xy

    def apply1DFourierSeries(self, x, n_terms):
        """Converts coordinates to a 1D Fourier series.
        Each (x,y) is transformed into [sin (pi*k*x/width),
                                        cos (pi*k*x/width),
                                        sin (pi*k*y/height),
                                        cos (pi*k*y/height)]
        with k representing the no: of terms (from 1 to infinity).

        Parameters
        ----------
        x
            Coordinates of the sampled points (input features).
        n_terms
            Number of Fourier terms to include (The maximum value of k)

        Returns
        -------
        Transformed features
        """
        xv = []
        Lx = self.args['width']
        Ly = self.args['height']
        for pt in x:
            xval = pt[0]
            yval = pt[1]
            inp_node_vals = []
            for k in range(1, n_terms+1):
                sinx = np.sin(np.pi*k*xval/Lx).item()
                cosx = np.cos(np.pi*k*xval/Lx).item()
                siny = np.sin(np.pi*k*yval/Ly).item()
                cosy = np.cos(np.pi*k*yval/Ly).item()
                inp_node_vals.extend([sinx, cosx, siny, cosy])
            xv.append(inp_node_vals)
        return tf.cast(tf.constant(xv), tf.float64)

    def apply2DFourierSeries(self, x, n_terms):
        """Converts coordinates to a 2D cosine Fourier series.
        Each (x,y) is transformed into a 2D discrete cosine transform.
        https://doi.org/10.1007/s00158-018-1962-y
        See above paper (Equation 30) for the 3D form of the equation
        from which the 2D form was taken.

        Parameters
        ----------
        x
            Coordinates of the sampled points (input features).
        n_terms
            Number of Fourier terms to include (The maximum value of k and l)

        Returns
        -------
        Transformed features
        """
        xv = []
        Lx = self.args['width']
        Ly = self.args['height']
        for pt in x:
            xval = pt[0]
            yval = pt[1]
            inp_node_vals = []
            for k1 in range(1, n_terms+1):
                for k2 in range(1, n_terms+1):
                    cosx = np.cos(np.pi*k1*xval/Lx).item()
                    cosy = np.cos(np.pi*k2*yval/Ly).item()
                    inp_node_vals.append(cosx * cosy)
            xv.append(inp_node_vals)
        return tf.cast(tf.constant(xv), tf.float64)


def global_normalization(inputs, epsilon=1e-6):
    """Normalizes the input using the mean and std of the values.
    """
    mean, variance = tf.nn.moments(inputs, axes=list(range(len(inputs.shape))))
    net = inputs
    net -= mean
    net *= tf.math.rsqrt(variance + epsilon)
    return net


def UpSampling2D(factor):
    """Layer that performs upsampling of an image.
    The upsampling is performed using a particular interpolation scheme.

    Parameters
    ----------
    factor
        The factor to upscale by.
        2 => Output image will have twice the number of pixels along each axis.
    """
    return layers.UpSampling2D((factor, factor), interpolation='bilinear')


def Conv2D(filters, kernel_size, **kwargs):
    """Function that performs convolution operation.

    Parameters
    ----------
    filters
        Number of filters in the kernel
    kernel_size
        Size of the convolution kernel

    Returns
    -------
    A keras colvolution layer
    """
    return layers.Conv2D(filters, kernel_size, padding='same', **kwargs)


def Conv2DT(filters, kernel_size, resize, **kwargs):
    """A transposed convolution layer.
    It can upsample by adjusting the strides and is
    completely differntaiable twice.
    """
    #  New CNN Model using conv2dtranspose
    if resize == 2:
        return layers.Conv2DTranspose(
                            filters=filters,
                            kernel_size=kernel_size,
                            strides=2,
                            padding='same', **kwargs)
    elif resize == 1:
        return layers.Conv2DTranspose(
                    filters=filters,
                    kernel_size=kernel_size,
                    strides=1,
                    padding='same', **kwargs)
    else:
        print('Given resize is not compatible')
        raise NotImplementedError


class AddOffset(layers.Layer):
    """A layer that adds a scaled bias to an input.
    """

    def __init__(self, scale=1):
        super().__init__()
        self.scale = scale

    def build(self, input_shape):
        self.bias = self.add_weight(
                    shape=input_shape, initializer='zeros',
                    trainable=True, name='bias')

    def call(self, inputs):
        return inputs + self.scale * self.bias


class CNNModel_c2dt_corr(Model):
    """Convolutional model that is completely differentiable twice.
    Model adapted from the one used in:
    https://github.com/google-research/neural-structural-optimization
    The main difference is in replaceing convolutional layers by
    transpose convolution, facilitating Hessian calculations.
    This is basically teh encoder part of a U-Net that upsamples to create
    a greyscale image of the required size.

    Attributes
    ----------
    core_model
        The Keras model from the inputs to the output
    z
        Trainable input parameter (beta vector in Hoyer's paper)

    Methods
    -------
    call
        Forward pass through the network.
    """
    def __init__(
                self,
                seed: int = 0,
                args : dict = None,
                latent_size: int = 128,
                dense_channels: int = 32,
                resizes: tuple = (1, 2, 2, 2, 1),
                conv_filters: tuple = (128, 64, 32, 16, 1),
                offset_scale: float = 10,
                kernel_size: tuple = (5, 5),
                latent_scale: float = 1.0,
                dense_init_scale: float = 1.0,
                activation=tf.keras.activations.tanh,
                conv_initializer=tf.initializers.VarianceScaling,
                normalization=global_normalization,
                latent_trainable=True,
                vol_const_hard=True):
        """Create the CNN keras model.

        Parameters
        ----------
        seed
            Sets the random state
        args
            Details of teh boundary conditions
        latent_size
            Size of the input parameter
        dense_channels
            Number of channels to rehape the output of the dense layer
        resizes
            When and by what multple to upsample the images
            E.g. (1,2) implies 2 CNN layers with the second layer enlarging
            the image by 2x
        conv_filters
            The number of filters to use at each layer
            Should be the same size as resizes
        offset_scale
            the parameter for the AddOffSet layer
        kernel_size
            size of the convolutional kernel
        latent_scale
            Used for the random initialziation of the latent vector "z"
        dense_init_scale
            Used for the random initialization of the dense layer's parameters
        activation
            The activation function to use
        conv_initializer
            The initialization schem for the convolutional layers
        normalization
            Normalize the values using mean and standard deviation
        latent_trainable
            Whether the latent vector should be trainable or fixed
        vol_const_hard
            Whether to apply a hard volume constraint later on. If so,
            the output of the model will not be constrained by sigmoid.
        """
        super().__init__(seed, args)

        if len(resizes) != len(conv_filters):
            raise ValueError('resizes and filters must be same size')
        activation = layers.Activation(activation)
        total_resize = int(np.prod(resizes))
        # Choose a startsize that results in an image of the required size.
        h = self.env.args['nely'] // total_resize
        w = self.env.args['nelx'] // total_resize
        net = inputs = layers.Input((latent_size,), batch_size=1)

        filters = h * w * dense_channels
        dense_initializer = tf.initializers.orthogonal(
            dense_init_scale * np.sqrt(max(filters / latent_size, 1)))
        net = layers.Dense(filters, kernel_initializer=dense_initializer)(net)
        net = layers.Reshape([h, w, dense_channels])(net)

        for resize, filters in zip(resizes, conv_filters):
            net = activation(net)
            net = normalization(net)
            net = Conv2DT(filters, kernel_size, resize,
                          kernel_initializer=conv_initializer)(net)
            if offset_scale != 0:
                net = AddOffset(offset_scale)(net)
        # if we will constrain the volume fraction later,
        # no need for sigmoid now
        if not vol_const_hard:
            net = tf.keras.layers.Activation("sigmoid")(net)
        outputs = tf.squeeze(net, axis=[-1])
        self.core_model = tf.keras.Model(inputs=inputs, outputs=outputs)

        latent_initializer = tf.initializers.RandomNormal(stddev=latent_scale)
        self.z = self.add_weight(
                shape=inputs.shape, initializer=latent_initializer, name='z',
                trainable=latent_trainable)

    def call(self, inputs=None):
        return self.core_model(self.z)


class CNNModel(Model):
    """Hoyer's original CNNModel.
    https://github.com/google-research/neural-structural-optimization
    This is basically teh encoder part of a U-Net that upsamples to create
    a greyscale image of the required size.

    Attributes
    ----------
    core_model
        The Keras model from the inputs to the output
    z
        Trainable input parameter (beta vector in Hoyer's paper)

    Methods
    -------
    call
        Forward pass through the network.
    """
    def __init__(
                self,
                seed=0,
                args=None,
                latent_size=128,
                dense_channels=32,
                resizes=(1, 2, 2, 2, 1),
                conv_filters=(128, 64, 32, 16, 1),
                offset_scale=10,
                kernel_size=(5, 5),
                latent_scale=1.0,
                dense_init_scale=1.0,
                activation=tf.nn.tanh,
                conv_initializer=tf.initializers.VarianceScaling,
                normalization=global_normalization):
        """Create the CNN keras model.

        Parameters
        ----------
        seed
            Sets the random state
        args
            Details of teh boundary conditions
        latent_size
            Size of the input parameter
        dense_channels
            Number of channels to rehape the output of the dense layer
        resizes
            When and by what multple to upsample the images
            E.g. (1,2) implies 2 CNN layers with the second layer enlarging
            the image by 2x
        conv_filters
            The number of filters to use at each layer
            Should be the same size as resizes
        offset_scale
            the parameter for the AddOffSet layer
        kernel_size
            size of the convolutional kernel
        latent_scale
            Used for the random initialziation of the latent vector "z"
        dense_init_scale
            Used for the random initialization of the dense layer's parameters
        activation
            The activation function to use
        conv_initializer
            The initialization schem for the convolutional layers
        normalization
            Normalize the values using mean and standard deviation
        """
        super().__init__(seed, args)

        if len(resizes) != len(conv_filters):
            raise ValueError('resizes and filters must be same size')

        activation = layers.Activation(activation)

        total_resize = int(np.prod(resizes))
        h = self.env.args['nely'] // total_resize
        w = self.env.args['nelx'] // total_resize

        net = inputs = layers.Input((latent_size,), batch_size=1)
        filters = h * w * dense_channels
        dense_initializer = tf.initializers.orthogonal(
                    dense_init_scale * np.sqrt(max(filters / latent_size, 1)))
        net = layers.Dense(filters, kernel_initializer=dense_initializer)(net)
        net = layers.Reshape([h, w, dense_channels])(net)

        for resize, filters in zip(resizes, conv_filters):
            net = activation(net)
            net = UpSampling2D(resize)(net)
            net = normalization(net)
            net = Conv2D(
                filters, kernel_size, kernel_initializer=conv_initializer)(net)
            if offset_scale != 0:
                net = AddOffset(offset_scale)(net)

        outputs = tf.squeeze(net, axis=[-1])

        self.core_model = tf.keras.Model(inputs=inputs, outputs=outputs)

        latent_initializer = tf.initializers.RandomNormal(stddev=latent_scale)
        self.z = self.add_weight(
            shape=inputs.shape, initializer=latent_initializer, name='z')

    def call(self, inputs=None):
        return self.core_model(self.z)
