# lint as python3
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
Autograd implementation of topology optimization for compliance minimization.
Exactly reproduces the result of "Efficient topology optimization in MATLAB
using 88 lines of code":
http://www.topopt.mek.dtu.dk/Apps-and-software/Efficient-topology-optimization-in-MATLAB

A note on conventions:
- forces and freedofs are stored flattened, but logically represent arrays of
  shape (Y+1, X+1, 2), where Y corresponds to the no: of elements
  along the height (nely).
- mask is either a scalar (1) or an array of shape (X, Y).
Yes, this is confusing. Sorry!

Functions
---------
heavyside_density_projection
    Performs a heavyside based projection of densities.
volume_violation_after_projection
    Calculates the difference in the volume before and after projection.
find_eta
    Uses bisection to find the root of a bounded function.
physical_density
    Convert model outputs to physical densities.
mean_density
    Calculates the mean volume/density.
get_stiffness_matrix
    Calculates the element stiffness matrix.
_get_dof_indices
    Helper function to keep track of free indices.
displace
    Displaces the load x using finite element techniques.
get_k
    Constructs a sparse stiffness matrix.
young_modulus
    Calculates the interpolated young's modulus.
compliance
    Calculates the compliance.
sigmoid
    Element-wise application of sigmoid function.
logit
    Useful for calculating the bracketing interval.
sigmoid_with_constrained_mean
    Constrains the densities to have a certain average.
calculate_forces
    Calculates the total forces acting on the domain.
objective
    Objective function (compliance) for topology optimization.


ToDo:
1. Check whether the gradient calculated through find_eta is correct.
    Currently, this function is not traced and only its final calculation is
    used in the heavyside projection. A similar function is used to perform
    hard volume constraint enforcement and it is implemented as being traced.
    If they are both same, try to remove one of these functions.
2. Understand how the lower and upper bounds are calculated for
    sigmoid_with_constrained_mean()
3. Find whether changing the element size is to be reflected elsewhere.
4. Debug code such that the use of body forces is independent of the
    mesh resolution.
5. Awaiting reply from Hoyer regarding access to their colab link on
    vectorization of compliance calculation.
"""
#                                                                       Modules
# =============================================================================
# Standard
from typing import Tuple

# Third-party
import autograd
import autograd.numpy as np

# Local
from . import autograd_lib
from . import caching
#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S', 'Gawel Kus']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


def heavyside_density_projection(x: np.ndarray, beta: float,
                                 eta: float) -> float:
    """Performs a heavyside based projection of densities.
    See On projection methods, convergence and
        robust formulationsin topology optimization.
        (DOI 10.1007/s00158-010-0602-y)

    Parameters
    ----------
    x
        Input densities with shape (nely, nelx)
    beta
        Projection parameter. Determines the approximation to the
        heavyside function. A large value implies larger similarity and
        causes stricter black and white designs.
    eta
        Parameter controlling volume fraction preservation.
        For a given beta, eta should be chosen such that the volume of
        x = volume of x_proj. This is done using a bisection algorithm.

    Returns
    -------
    x_proj
        The projected densities.
    """
    x_proj = (np.tanh(beta*eta) + np.tanh(beta*(x-eta))) / \
             (np.tanh(beta*eta) + np.tanh(beta*(1-eta)))
    return x_proj


def volume_violation_after_projection(x: np.ndarray, beta: float,
                                      eta: float) -> float:
    """Calculates the difference in the volume before and after projection.

    Parameters
    ----------
    x
        Input densities with shape (nely, nelx)
    beta
        Projection parameter. Determines the approximation to the
        heavyside function. A large value implies larger similarity and
        causes stricter black and white designs.
    eta
        Parameter (between 0 and 1) controlling volume fraction preservation.
        For a given beta, eta should be chosen such that the volume of
        x = volume of x_proj. This is done using a bisection algorithm.

    Returns
    -------
    volume_violation
        The difference in the mean volume fractions.
    """
    x_proj = heavyside_density_projection(x, beta, eta)
    volume_violation = x_proj.mean() - x.mean()
    return volume_violation


def find_eta(func: callable, a: float, b: float,
             tol: float) -> float:
    """Uses bisection to find the root of a bounded function.
        # approximates a root, R, of f bounded
    # by a and b to within tolerance
    # | f(m) | < tol with m the midpoint
    # between a and b Recursive implementation

    Parameters
    ----------
    func
        A function that returns the difference in the mean volumes
        between the original and projected densities.
    a
        Lower bounding limit
    b
        Upper bounding limit
    tol
        The tolerance to which the final point should match the root of
        the function 'func'

    Returns
    -------
    eta
        The parameter that is the root of the function.
        This value will ensure that teh colume is preserved upon using
        desnity projection.
    """
    # check if a and b bound a root
    if np.sign(func(a)) == np.sign(func(b)):
        raise Exception("The scalars a and b do not bound a root")

    # get midpoint
    m = (a + b)/2
    if np.abs(func(m)) < tol:
        # stopping condition, report m as root
        return m
    elif np.sign(func(a)) == np.sign(func(m)):
        # case where m is an improvement on a.
        # Make recursive call with a = m
        return find_eta(func, m, b, tol)
    elif np.sign(func(b)) == np.sign(func(m)):
        # case where m is an improvement on b.
        # Make recursive call with b = m
        return find_eta(func, a, m, tol)


def physical_density(x: np.ndarray,
                     args: dict, volume_contraint: bool = False,
                     cone_filter: bool = True,
                     den_proj: bool = False,
                     beta: float = 1) -> np.ndarray:
    """Convert model outputs to physical densities.
    Physical density are analyzed using FEA and represents the design.
    args['filter_width']: Physical domain size over which
        the filter has to act.
    args['filter_width'] / elem_size : Number of elements to
        be included for cone_filtering

    Parameters
    ----------
    x
        Unfiltered densities- output from the model
    args
        Contains the problem details
    volume_contraint
        Constrain the densities such that volume constraint is not
        violated
    cone_filter
        Apply density filtering using a cone filter
    den_proj
        Apply heavyside density projection.
    beta
        The parameter used to control the severity of the density projection

    Returns
    -------
        x
            Physical densities that can be sent for FEA.
    """
    shape = (args['nely'], args['nelx'])
    assert x.shape == shape or x.ndim == 1
    x = x.reshape(shape)
    # Apply hard volume constraint if needed
    if volume_contraint:
        mask = np.broadcast_to(args['mask'], x.shape) > 0
        x_designed = sigmoid_with_constrained_mean(x[mask], args['volfrac'])
        x_flat = autograd_lib.scatter1d(
                        x_designed, np.flatnonzero(mask), x.size)
        x = x_flat.reshape(x.shape)
    else:
        x = x * args['mask']
    if cone_filter:
        # Works only with a square element
        assert args['width']/args['nelx'] == args['height'] / args['nely']
        # elem_size = args['width']/args['nelx']
        # Currently filtering using 2 elements only
        x = autograd_lib.cone_filter(x, 2, args['mask'])
    if den_proj:
        # When its an arraybox for autograd and not a numpy array
        if not isinstance(x, np.ndarray):
            # For rendering designs
            f = lambda eta : volume_violation_after_projection(x._value,
                                                               beta, eta)
        else:
            # During actual forward pass.
            f = lambda eta : volume_violation_after_projection(x, beta, eta)
        # Use a bisection algorithm to find eta parameter that maintains
        # the same volume
        eta = find_eta(f, 0, 1, 1e-3)
        x = heavyside_density_projection(x, beta, eta)
    return x


def mean_density(x: np.ndarray,
                 args: dict, volume_contraint: bool = False,
                 cone_filter: bool = True, den_proj: bool = False,
                 beta: float = 1) -> np.ndarray:
    """Calculates the mean volume/density.
    Converts the model outputs to physical densities before
    calculating the average.

    Parameters
    ----------
    x
        Unfiltered densities- output from the model
    args
        Contains the problem details
    volume_contraint
        Constrain the densities such that volume constraint is not
        violated
    cone_filter
        Apply density filtering using a cone filter
    den_proj
        Apply heavyside density projection.
    beta
        The parameter used to control the severity of the density projection

    Returns
    -------
        Average density
    """
    return (np.mean(physical_density(x, args, volume_contraint,
            cone_filter, den_proj, beta)) / np.mean(args['mask']))


def get_stiffness_matrix(args: dict) -> np.ndarray:
    """Calculates the element stiffness matrix.
    Considers rectangular elements of height 'H' and width 'W'.
    This was derived symbolically by Gawel Kus following
    https://homepages.rpi.edu/~des/4NodeQuad.pdf and
    http://inside.mines.edu/~vgriffit/pubs/All_J_Pubs/28.pdf

    See the notebook: neural_opt/notebooks/Stiffness_matrix.ipynb

    Parameters
    ----------
    args
        Contains the problem details

    Returns
    -------
        Element stiffness matrix
    """
    # e-Young's modulus, nu- poisson ratio
    e, nu = args['young'], args['poisson']
    H = args['height'] / args['nely']
    W = args['width'] / args['nelx']

    k = np.array([
        12*H**2 - 6*W**2*nu + 6*W**2,
        4.5*H*W*(1 + nu),
        -12*H**2 - 3*W**2*nu + 3*W**2,
        36*H*W*(-0.125 + 0.375*nu),
        -6*H**2 + 3*W**2*nu - 3*W**2,
        -4.5*H*W*(1 + nu),
        6*H**2 + 6*W**2*nu - 6*W**2,
        36*H*W*(0.125 - 0.375*nu)
        ])

    return e/(36*H*W*(1 - nu**2)) * np.array([
        [k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7]],
        [k[1], k[0], k[7], k[6], k[5], k[4], k[3], k[2]],
        [k[2], k[7], k[0], k[5], k[6], k[3], k[4], k[1]],
        [k[3], k[6], k[5], k[0], k[7], k[2], k[1], k[4]],
        [k[4], k[5], k[6], k[7], k[0], k[1], k[2], k[3]],
        [k[5], k[4], k[3], k[2], k[1], k[0], k[7], k[6]],
        [k[6], k[3], k[4], k[1], k[2], k[7], k[0], k[5]],
        [k[7], k[2], k[1], k[4], k[3], k[6], k[5], k[0]]
        ])


@caching.ndarray_safe_lru_cache(1)
def _get_dof_indices(freedofs: np.array, fixdofs: np.array,
                     k_xlist: np.array,
                     k_ylist: np.array) -> Tuple[np.array]:
    """Helper function to keep track of free indices.

    Parameters
    ----------
    freedofs
        Node numbers which are unrestricted.
    fixdofs
        Node numbers which have fixed displacement (=0).
    k_xlist
        The x coordinates of values in the stiffness matrix.
    k_ylist
        The y coordinates of values in the stiffness matrix.

    Returns
    -------
    index_map
        Inverse indices corresponing to the nodes. For example, if ixs
        is a list of indices that permutes the list A, then this function
        gives us a second list of indices inv_ixs such that
        A[ixs][inv_ixs] = A
    keep
        Array of booleans that determine whether the corresponding
        element in the global stiffness matrix is to be kept (if free)
        or not (if fixed) for displacement calculation.
    indices
        Numpy array with shape (2, num_zeros) giving x and y indices for
        non-zero matrix entries.
    """
    index_map = autograd_lib.inverse_permutation(
        np.concatenate([freedofs, fixdofs]))
    keep = np.isin(k_xlist, freedofs) & np.isin(k_ylist, freedofs)
    i = index_map[k_ylist][keep]
    j = index_map[k_xlist][keep]
    indices = np.stack([i, j])
    return index_map, keep, indices


def displace(x_phys: np.ndarray, ke: np.ndarray,
             forces: np.array, freedofs: np.array,
             fixdofs: np.array,
             penal: float = 3, e_min: float = 1e-9,
             e_0: float = 1) -> np.array:
    """Displaces the load x using finite element techniques.
    The spsolve here occupies the majority of this entire
    simulation's runtime.

    Parameters
    ----------
    x_phys
        The physical densities
    ke
        Element stiffness matrix
    forces
        Flattened array of forces at all nodes.
    freedofs
        Node numbers which are unrestricted.
    fixdofs
        Node numbers which have fixed displacement (=0).
    penal
        SIMP penalty value.
    e_min
        Young's modulus of the void region
    e_o
        Young's modulus of the material

    Returns
    -------
        Displacement vector corrponding to the original node ordering.
        (Node ordering - Top-left start, column wise, Bot-right end)
    """
    stiffness = young_modulus(x_phys, e_0, e_min, p=penal)
    k_entries, k_ylist, k_xlist = get_k(stiffness, ke)

    index_map, keep, indices = _get_dof_indices(
        freedofs, fixdofs, k_ylist, k_xlist
    )
    u_nonzero = autograd_lib.solve_coo(k_entries[keep],
                                       indices, forces[freedofs],
                                       sym_pos=False)
    u_values = np.concatenate([u_nonzero, np.zeros(len(fixdofs))])

    return u_values[index_map]


def get_k(stiffness: np.ndarray, ke: np.ndarray) -> Tuple[np.ndarray]:
    """Constructs a sparse stiffness matrix.
    This matrix is used in the displace function and is stored in
    a sparse way (flattened with pointers to the non-zero locations).
    Luckily, since our nodes are locally-connected, most of the entries
    in K are zero. We can save a vast amount of memory by representing it
    with a sparse “coordinate list” or COO format.
    https://greydanus.github.io/2022/05/08/structural-optimization/

    Parameters
    ----------
    stiffness
        The stiffness values of each element.
    ke
        Element stiffness matrix.

    Returns
    -------
    value_list
        The non-zero entries of the global stiffnes matrix flattened.
    y_list
        The y coordinates of values in the stiffness matrix.
    x_list
        The x coordinates of values in the stiffness matrix.
    """
    nely, nelx = stiffness.shape
    # get position of the nodes of each element in the stiffness matrix
    ely, elx = np.meshgrid(range(nely), range(nelx))  # x, y coords
    ely, elx = ely.reshape(-1, 1), elx.reshape(-1, 1)

    n1 = (nely+1)*(elx+0) + (ely+0)
    n2 = (nely+1)*(elx+1) + (ely+0)
    n3 = (nely+1)*(elx+1) + (ely+1)
    n4 = (nely+1)*(elx+0) + (ely+1)
    edof = np.array([2*n1, 2*n1+1, 2*n2, 2*n2+1, 2*n3, 2*n3+1, 2*n4, 2*n4+1])
    edof = edof.T[0]
    # flat list pointer of each node in an element
    x_list = np.repeat(edof, 8)
    y_list = np.tile(edof, 8).flatten()

    # make the stiffness matrix
    kd = stiffness.T.reshape(nelx*nely, 1, 1)
    value_list = (kd * np.tile(ke, kd.shape)).flatten()
    return value_list, y_list, x_list


def young_modulus(x: np.ndarray, e_0: float, e_min: float,
                  p: float = 3) -> np.ndarray:
    """Calculates the interpolated young's modulus.
    This is calculated accoring to the modified SIMP law.

    Parameters
    ----------
    x
        The physical densities.
    e_0
        Young's modulus of the material
    e_min
        Young's modulus of the void
    p
        SIMP penalty

    Returns
    -------
        Interpolated young's modulus for each element.
    """
    return e_min + x ** p * (e_0 - e_min)


def compliance(x_phys: np.ndarray, u: np.array, ke: np.ndarray,
               penal: float = 3, e_min: float = 1e-9,
               e_0: float = 1) -> np.array:
    """Calculates the compliance.
    Read about how this was vectorized here:
    https://colab.research.google.com/drive/1PE-otq5hAMMi_q9dC6DkRvf2xzVhWVQ4

    Parameters
    ----------
    x_phys
        Physical densities
    u
        global displacement vector
    ke
        element stiffness matrix
    penal
        SIMP penalty
    e_min
        Young's modulus of the void.
    e_0
        Young's modulus of the material.

    Returns
    -------
        The compliance of the structure.
    """
    # index map
    nely, nelx = x_phys.shape
    ely, elx = np.meshgrid(range(nely), range(nelx))  # x, y coords

    # nodes
    n1 = (nely+1)*(elx+0) + (ely+0)
    n2 = (nely+1)*(elx+1) + (ely+0)
    n3 = (nely+1)*(elx+1) + (ely+1)
    n4 = (nely+1)*(elx+0) + (ely+1)
    all_ixs = np.array([2*n1, 2*n1+1, 2*n2, 2*n2+1,
                        2*n3, 2*n3+1, 2*n4, 2*n4+1])

    # select from u matrix
    u_selected = u[all_ixs]

    # compute x^penal * U.T @ ke @ U in a vectorized way
    ke_u = np.einsum('ij,jkl->ikl', ke, u_selected)
    ce = np.einsum('ijk,ijk->jk', u_selected, ke_u)
    C = young_modulus(x_phys, e_0, e_min, p=penal) * ce.T
    return np.sum(C)


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Element-wise application of sigmoid function.
    Parameters
    ----------
    x
        Input densities of shape (nely, nelx)

    Returns
    -------
        Transformed densities.
    """
    return np.tanh(0.5*x)*.5 + 0.5


def logit(p: float) -> float:
    """Useful for calculating the bracketing interval.
    I don't know why they use this function.

    Parameters
    ----------
    p
        The desired volume fraction

    Returns
    -------
        A clipped and scaled value?
    """
    # ToDo: figure out how this function is used.
    p = np.clip(p, 0, 1)
    return np.log(p) - np.log1p(-p)


def sigmoid_with_constrained_mean(x: np.ndarray,
                                  average: float) -> np.ndarray:
    """Constrains the densities to have a certain average.
    This transforms the densities using a sigmoid transformation/
    The value of 'b' is found using a root solver that results in
    the descired average value. Using this function, voluem constraint
    can be enforced in a hard way.

    Parameters
    ----------
    x
        Densities in the shape (nely, nelx)
    average
        The desired volume fraction

    Returns
    -------
        The constrained densities such that the average is
        the desired volume fraction.
    """
    # The function whose root is to be found
    f = lambda x, y: sigmoid(x + y).mean() - average
    lower_bound = logit(average) - np.max(x)
    upper_bound = logit(average) - np.min(x)
    # Uses a bisection algorithm
    b = autograd_lib.find_root(f, x, lower_bound, upper_bound)
    return sigmoid(x + b)


def calculate_forces(x_phys: np.ndarray, args: dict):
    """Calculates the total forces acting on the domain.
    If body forces are to be considered, args['g'] has to be non-zero.
    The body forces will be distributed to all the nodes.
    Body force = args['g'] * density * element_volume.
    Total force =  Body force + Applied force
    Warning: Currently, body force increases with the number of elements.

    Parameters
    ----------
    x_phys
        The physical densities.
    args
        The details of the problem instance.

    Returns
    -------
        Forces acting on each node.
    """
    applied_force = args['forces']
    if not args.get('g'):
        # If g is given as 0, ignore body forces
        return applied_force
    # distribute the density to the surrounding nodes [forces act of nodes]
    # to obtain an array of (n_nodes_x, n_nodes_y)
    density = 0
    for pad_left in [0, 1]:
        for pad_up in [0, 1]:
            padding = [(pad_left, 1 - pad_left), (pad_up, 1 - pad_up)]
            density += (1/4) * np.pad(
                            x_phys.T, padding, mode='constant',
                            constant_values=0)
    # assuming square elements
    assert args['width']/args['nelx'] == args['height']/args['nely']
    elem_vol = (args['width']/args['nelx'])**2 * 1
    # Create an ndarray of shape (n_nodes_x, n_nodes_y, 2)
    # such that gravitional_force[:,:,0] correspond to x direction forces
    density = density[..., np.newaxis] * np.array([0, 1])
    gravitional_force = -args['g'] * density * elem_vol
    # Forces along x = 0 [array[0]] correspnds to this
    # ToDo: Normalize the effect of body forces against discretization
    return applied_force + gravitional_force.ravel()


def objective(x: np.ndarray,
              ke: np.ndarray, args: dict,
              volume_contraint: bool = False, cone_filter: bool = True,
              p: float = 3.0, den_proj: float = False,
              beta: float = 1) -> float:
    """Objective function (compliance) for topology optimization.
    c = U.T K U, where U is teh global equilibrium displacement vector and
        K is the global stiffness matrix.

    Parameters
    ----------
    x
        Unfiltered densities- output from the model
    ke
        Element stiffness matrix
    args
        Contains the problem details
    volume_contraint
        Constrain the densities such that volume constraint is not
        violated.
    cone_filter
        Apply density filtering using a cone filter
    den_proj
        Apply heavyside density projection.
    beta
        The parameter used to control the severity of the density projection

    Returns
    -------
        c
            The compliance value.
    """
    kwargs = dict(penal=p, e_min=args['young_min'], e_0=args['young'])
    # Calculate the physical density from logits (model's outputs)
    x_phys = physical_density(x, args, volume_contraint=volume_contraint,
                              cone_filter=cone_filter,
                              den_proj=den_proj, beta=beta)
    # Calculate the forces
    forces = calculate_forces(x_phys, args)
    # Find the equilibrium displacement field
    u = displace(
        x_phys, ke, forces, args['freedofs'], args['fixdofs'], **kwargs)
    # Calculate the scalar compliance value
    c = compliance(x_phys, u, ke, **kwargs)
    return c
