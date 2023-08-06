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
Contains all the models tested for neural reparameterization.

Classes
-------
Environment
    An interface between the simulation and models.

Functions
---------
specified_task
    Given a problem, return parameters for running topology optimization.
"""
#                                                                       Modules
# =============================================================================

# Third-party
import autograd.numpy as np

# Local
from . import topo_physics
from . import problems


def specified_task(problem: problems.Problem) -> dict:
    """Given a problem, return parameters for running topology optimization.

    Parameters
    ----------
    problem
        A Problem instance that contains the boundary conditiuons details.

    Returns
    -------
    args
        A dictionary of details of the specific problem.
    """
    fixdofs = np.flatnonzero(problem.normals.ravel())
    alldofs = np.arange(2 * (problem.nelx + 1) * (problem.nely + 1))
    freedofs = np.sort(list(set(alldofs) - set(fixdofs)))

    args = {
        # material properties
        'young': 1,  # Young's modulus, E
        'young_min': 1e-9,  # E_min for the void
        'poisson': 0.3,  # Poisson ratio
        'g': 0,  # Gravity body force
        # constraints
        'volfrac': problem.density,
        'xmin': 0.001,  # Minimum density
        'xmax': 1.0,  # maximum density
        # input parameters
        'nelx': problem.nelx,
        'nely': problem.nely,
        'mask': problem.mask,
        'width': problem.width,
        'height': problem.height,
        'freedofs': freedofs,
        'fixdofs': fixdofs,
        'forces': problem.forces.ravel(),
        'penal': 3.0,  # SIMP penalty
        'filter_width': 2  # Default cone filter width
    }
    return args


class Environment:
    """An interface between the simulation and models.

    Attributes
    ----------
    args
        The problem details extracted using 'specified_task'.
    ke
        Element stiffness matrix

    Methods
    -------
    __init__
        Calculates and stores the element stiffness matrix.
    reshape
        Reshapes logits to a 2D shape.
    render
        Calculates the design from the model output.
    objective
        Calculates the objective value from the model output.
    constraint
        Calculates the value of the volume constraint.
    """

    def __init__(self, args: dict) -> None:
        """Calculates and stores the element stiffness matrix.
        This is dependent on the problem details supplied.

        Parameters
        ----------
        args
            The problem details extracted using 'specified_task'.
        """
        self.args = args
        self.ke = topo_physics.get_stiffness_matrix(self.args)

    def reshape(self, params: np.ndarray) -> np.ndarray:
        """Reshapes logits to a 2D shape.
        Parameters
        ----------
        params
            The output of the models as a numpy array.

        Returns
        -------
            Output reshaped into (nely, nelx)
        """
        return params.reshape(self.args['nely'], self.args['nelx'])

    def render(self, params: np.ndarray,
               volume_contraint: bool = True,
               cone_filter : bool = True,
               den_proj: bool = False, beta: float = 1) -> np.ndarray:
        """Calculates the design from the model output.

        Parameters
        ----------
        params
            The output of the models as a numpy array.
        volume_constraint
            Whether to apply a hard volume constraint.
        cone_filter
            Whether to apply a cone filter on the output.
        den_proj
            Whether to apply a heavyside based projection.
        beta
            The projection parameter used.

        Returns
        -------
            The physical densities that are used in the FEA.
        """
        return topo_physics.physical_density(
                    self.reshape(params), self.args,
                    volume_contraint=volume_contraint,
                    cone_filter=cone_filter, den_proj=den_proj,
                    beta=beta)

    def objective(self, params: np.ndarray,
                  volume_contraint: bool = False, cone_filter: bool = True,
                  p: float = 3.0, den_proj: bool = False,
                  beta: float = 1) -> float:
        """Calculates the objective value from the model output.
        Runs the FEA to find the compliance value.

        Parameters
        ----------
        params
            The output of the models as a numpy array.
        volume_constraint
            Whether to apply a hard volume constraint.
        cone_filter
            Whether to apply a cone filter on the output.
        den_proj
            Whether to apply a heavyside based projection.
        beta
            The projection parameter used.
        p
            SIMP penalty to be used.

        Returns
        -------
            The objective value (compliance).
        """
        return topo_physics.objective(
                    self.reshape(params), self.ke, self.args,
                    volume_contraint=volume_contraint,
                    cone_filter=cone_filter, p=p,
                    den_proj=den_proj, beta=beta)

    def constraint(self, params: np.ndarray,
                   den_proj: bool = False,
                   beta: bool = 1):
        """Calculates the value of the volume constraint.

        Parameters
        ----------
        params
            The output of the models as a numpy array.
        den_proj
            Whether to apply a heavyside based projection.
        beta
            The projection parameter used.

        Returns
        -------
            The constraint value.
        """
        volume = topo_physics.mean_density(self.reshape(params),
                                           self.args, den_proj=den_proj,
                                           beta=1)
        return volume - self.args['volfrac']
