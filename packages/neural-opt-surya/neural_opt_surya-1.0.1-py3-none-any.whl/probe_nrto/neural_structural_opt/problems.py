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
"""A suite of topology optimization boundary conditions.

Classes
-------
Problem
    Description of a topology optimization boundary condition.

Functions
---------
cantilever_beam_two_point
    Cantilever supported by two points.
tensile_rod
    Cantilever beam with a tensile load at the end.
causeway_bridge
    A bridge supported by columns at a regular interval.
mbb_beam
    Textbook beam example.
l_shape
    An L-shaped structure, with a limited design region.
dam
    Support horizitonal forces, proportional to depth.
multistory_building
    A multi-story building, supported from the ground.
michell_centered_both
    A single force down at the center, with support from the side.
pure_bending_moment
    Pure bending forces on a beam.
staggered_points
    A staggered grid of points with downward forces, supported from below.
"""
#                                                                       Modules
# =============================================================================
# Standard
from typing import Optional, Union
import dataclasses
import sys

# Third-party
import numpy as np
import skimage.draw

X, Y = 0, 1


@dataclasses.dataclass
class Problem:
    """Description of a topology optimization problem.

    Attributes:
    -----------
    normals
        Array of shape (width+1, height+1, 2) where a value of 1
        indicates a "fixed" coordinate, and 0 indicates no normal force.
    forces
        Array of shape (width+1, height+1, 2) indicating external
        applied forces in the x and y directions.
    density
        Fraction of the design region that should be non-zero.
    mask
        Scalar or float64 array of shape (height, width) that is multiplied by
        the design mask before and after applying the blurring filters.
        Values of 1 indicate regions where the material can be optimized;
        values of 0 are constrained to be empty.
    name
        Optional name of this problem.
    width
        Integer width of the domain.
    height
        Integer height of the domain.
    mirror_left
        Should the design be mirrored to the left when displayed.
    mirror_right
        Should the design be mirrored to the right when displayed.
    nelx
        Number of elements in the FEM grid along width
    nely
        Number of elements in the FEM grid along height
    """
    normals: np.ndarray
    forces: np.ndarray
    density: float
    width: int = 2  # Domain size
    height: int = 1  # Domain size
    mask: Union[np.ndarray, float] = 1
    name: Optional[str] = None
    nelx: int = dataclasses.field(init=False)
    nely: int = dataclasses.field(init=False)
    mirror_left: bool = dataclasses.field(init=False)
    mirror_right: bool = dataclasses.field(init=False)

    def __post_init__(self):
        self.nelx = self.normals.shape[0] - 1
        self.nely = self.normals.shape[1] - 1
        print("nely has been set to {}".format(self.nely))

        if self.normals.shape != (self.nelx + 1, self.nely + 1, 2):
            raise ValueError(f'normals has wrong shape: {self.normals.shape}')
        if self.forces.shape != (self.nelx + 1, self.nely + 1, 2):
            raise ValueError(f'forces has wrong shape: {self.forces.shape}')
        if (isinstance(self.mask, np.ndarray)
                and self.mask.shape != (self.nelx, self.nely)):
            raise ValueError(f'mask has wrong shape: {self.mask.shape}')

        self.mirror_left = (
            self.normals[0, :, X].all() and not self.normals[0, :, Y].all()
        )
        self.mirror_right = (
            self.normals[-1, :, X].all() and not self.normals[-1, :, Y].all()
        )


def cantilever_beam_two_point(
        nelx: int = 64, density: float = 0.15,
        width: int = 64, height: int = 32,
        support_position: float = 0.0,
        force_position: float = 0.5) -> Problem:
    """Cantilever supported by two points.
    The optimal structure has fine features that depend on the mesh resolution.
    # https://link.springer.com/content/pdf/10.1007%2Fs00158-010-0557-z.pdf

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    support_position
        Location of the two supports.
    force_location
        Location of the point load.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[0, round(nely*(1 - support_position)), :] = 1
    normals[0, round(nely*support_position), :] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[-1, round((1 - force_position)*nely), Y] = -1

    return Problem(normals, forces, density, width, height,
                   1, 'cantilever_fine')


def tensile_rod(
        nelx: int = 64, density: float = 0.2,
        width: int = 64, height: int = 32,
        force_position: float = 0.5) -> Problem:
    """Cantilever beam with a tensile load at the end.
    Intended to produce a simple rod like structure.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    force_location
        Location of the point load.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[0, :, :] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[-1, round((1 - force_position)*nely), X] = -1

    return Problem(normals, forces, density, width, height, 1, 'tensile_rod')


def causeway_bridge(nelx: int = 64, density: float = 0.1, width: int = 64,
                    height: int = 64, deck_level: float = 0.5) -> Problem:
    """A bridge supported by columns at a regular interval.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    deck_level
        Location of the deck of the bridge.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[-1, -1, Y] = 1
    normals[-1, :, X] = 1
    normals[0, :, X] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[:, round(nely * (1 - deck_level)), Y] = -1 / nelx
    return Problem(normals, forces, density, width, height, 1,
                   'causeway_bridge')


def mbb_beam(nelx: int = 64, density: float = 0.2,
             width: int = 64, height: int = 32) -> Problem:
    """Textbook beam example.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[-1, -1, Y] = 1
    normals[0, :, X] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[0, 0, Y] = -1

    return Problem(normals, forces, density, width, height, 1, 'mbb')


def l_shape(nelx: int = 64, density: float = 0.1, width: int = 64,
            height: int = 64, aspect: float = 0.4,
            force_position: float = 0.5) -> Problem:
    """An L-shaped structure, with a limited design region.
    Topology Optimization Benchmarks in 2D.
    Doesn't work for assymetrical width and height.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    force_position
        Location of the point load.
    aspect
        Determines how much region should be masked from optimization.

    Returns
    -------
        A problem instance with the necessary details.
    """

    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[:round(aspect*nelx), 0, :] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[-1, round((1 - aspect*force_position)*nely), Y] = -1

    mask = np.ones((nelx, nely))
    mask[round(nely*aspect):, :round(nelx*(1-aspect))] = 0

    return Problem(normals, forces, density, width, height, mask.T, 'lshape')


def dam(nelx: int = 64, density: float = 0.25, width: int = 32,
        height: int = 64) -> Problem:
    """Support horizitonal forces, proportional to depth.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[:, -1, X] = 1
    normals[:, -1, Y] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[0, :, X] = 2 * np.arange(1, nely+2) / nely ** 2
    return Problem(normals, forces, density, width, height, 1, 'dam')


def multistory_building(nelx: int = 64, density: float = 0.3,
                        width: int = 32, height: int = 64,
                        interval: int = 32) -> Problem:
    """A multi-story building, supported from the ground.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    interval
        The spacing between the each floor

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[:, -1, Y] = 1
    normals[-1, :, X] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[:, ::interval, Y] = -1 / nelx
    return Problem(normals, forces, density, width, height, 1, 'multistory')


def michell_centered_both(nelx: int = 64, density: float = 0.1,
                          width: int = 64, height: int = 32,
                          position: float = 0.05) -> Problem:
    """A single force down at the center, with support from the side.
    https://en.wikipedia.org/wiki/Michell_structures#Examples

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    position
        Location of the support to prevent motion along Y axis.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[round(position*nelx), round(nely/2), Y] = 1
    normals[-1, :, X] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[-1, round(nely/2), Y] = -1

    return Problem(normals, forces, density, width, height, 1, "michell")


def pure_bending_moment(nelx: int = 64, density: float = 0.15, width: int = 32,
                        height: int = 16,
                        support_position: float = 0.45) -> Problem:
    """Pure bending forces on a beam.
    Figure 28 from
    http://naca.central.cranfield.ac.uk/reports/arc/rm/3303.pdf

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    support_position
        Location of the support.

    Returns
    -------
        A problem instance with the necessary details.
    """

    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[-1, :, X] = 1
    # for numerical stability, fix y forces here at 0
    normals[0, round(nely*(1-support_position)), Y] = 1
    normals[0, round(nely*support_position), Y] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    forces[0, round(nely*(1-support_position)), X] = 1
    forces[0, round(nely*support_position), X] = -1

    return Problem(normals, forces, density, width, height, 1, 'bending')


def staggered_points(nelx: int = 32, density: float = 0.3, width: int = 32,
                     height: int = 16, interval: int = 16,
                     break_symmetry: bool = False) -> Problem:
    """A staggered grid of points with downward forces, supported from below.

    Parameters
    ----------
    nelx
        Number of elements along x direction.
    density
        Desired volume fraction to be filled with material.
    width
        The physical width of the design domain.
    height
        The physical height of the design domain.
    interval
        The difference between the points.
    break_symmetry
        Breaks horizontal symmetry.

    Returns
    -------
        A problem instance with the necessary details.
    """
    nely = int(height*nelx/width)
    try:
        assert nely == height*nelx/width
    except Exception:
        sys.exit("nely is not an integer")
    normals = np.zeros((nelx + 1, nely + 1, 2))
    normals[:, -1, Y] = 1
    normals[0, :, X] = 1
    normals[-1, :, X] = 1

    forces = np.zeros((nelx + 1, nely + 1, 2))
    f = interval ** 2 / (nelx * nely)
    # intentionally break horizontal symmetry?
    forces[interval//2+int(break_symmetry)::interval, ::interval, Y] = -f
    forces[int(break_symmetry)::interval, interval//2::interval, Y] = -f
    return Problem(normals, forces, density, width, height, 1, 'staggered')


PROBLEMS_BY_NAME = {'tensile_rod': tensile_rod,
                    'causeway_bridge': causeway_bridge,
                    'cantilever_fine': cantilever_beam_two_point,
                    'michell': michell_centered_both,
                    'mbb': mbb_beam,
                    'lshape': l_shape,
                    'dam': dam,
                    'multistory': multistory_building,
                    'bending': pure_bending_moment,
                    'staggered': staggered_points}
