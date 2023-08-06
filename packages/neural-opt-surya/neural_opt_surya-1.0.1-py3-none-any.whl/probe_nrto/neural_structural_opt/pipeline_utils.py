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
"""Pipeline utilties to create images from designs.

Functions
---------
image_from_array
    Convert a NumPy array into a Pillow Image using a colormap.
image_from_design
    Convert a design and problem into a Pillow Image.
"""
#                                                                       Modules
# =============================================================================
# Standard
import math
from typing import Any, Dict

# Third-party
import matplotlib.cm
import matplotlib.colors
import numpy as np
from PIL import Image
import xarray

# Local
from . import problems
#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Suryanarayanan (s.manojsanu@tudelft.nl)'
__credits__ = ['Suryanarayanan M S']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


def image_from_array(
    data: np.ndarray, cmap: str = 'Greys', vmin: float = 0, vmax: float = 1,
        ) -> Image.Image:
    """Convert a NumPy array into a Pillow Image using a colormap.

    Parameters
    ----------
    data
        Design as a numpy array.
    cmap
        The colormap scheme to be used.
    vmin
        The minimum density value.
    vmax
        The maximum density value.

    Returns
    -------
    image
        A PIL image of the numpy array.
    """
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    frame = np.ma.masked_invalid(data)
    image = Image.fromarray(mappable.to_rgba(frame, bytes=True), mode='RGBA')
    return image


def image_from_design(
        design: xarray.DataArray, problem: problems.Problem,
        ) -> Image.Image:
    """Convert a design and problem into a Pillow Image.
    The designs are appropriately mirrored before rendering
    as image.

    Parameters
    ----------
    design
        A single design.
    problem
        An instance of Problem class.
        Used only for checking the mirroring.

    Returns
    -------
        An image of the design.
    """
    assert design.dims == ('y', 'x'), design.dims
    imaged_designs = []

    if problem.mirror_left:
        imaged_designs.append(design.isel(x=slice(None, None, -1)))
    imaged_designs.append(design)

    if problem.mirror_right:
        imaged_designs.append(design.isel(x=slice(None, None, -1)))
    return image_from_array(xarray.concat(imaged_designs, dim='x').data)
