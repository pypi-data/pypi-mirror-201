from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import numpy.typing as npt

"""
This file contains type definitions for the first version of our binary scene formate (internally referred to as bpcv3)
"""


@dataclass
class Points:
    # shape = (-1,3), dtype=np.float32
    # NOTE: positions MUST preserve order of the attachments provided
    positions: Optional[npt.NDArray[np.float32]] = None
    # shape = (-1,3), dtype=np.uint8
    colors: Optional[npt.NDArray[np.uint8]] = None
    # shape = (-1,), dtype=np.uint8
    intensities: Optional[npt.NDArray[np.uint8]] = None
    # For tasks with frames, timestamps are used to derive which points belong in which frames.
    # Given the fps from a Device, the 0th frame contains all points with timestamps in the
    # first 1/fps second, and so on. This may be None if no timestamps were given.
    # timestamps is in seconds
    # shape = (-1,), dtype=np.float32
    timestamps: Optional[npt.NDArray[np.float32]] = None
    # shape = (-1,), dtype=np.uint32
    labels: Optional[npt.NDArray[np.uint32]] = None
    # Metadata flags. A binary mask for specific boolean features.
    # shape = (-1,), dtype=np.uint32
    # Current flags: 0: is_outlier, 1: is_ground
    flags: Optional[npt.NDArray[np.uint32]] = None


@dataclass
class Device:
    poses: npt.NDArray[np.float32]


@dataclass
class Frame:
    index: int
    points: Points


@dataclass
class Camera:
    index: int
    name: str
    cx: float
    cy: float
    fx: float
    fy: float
    distortion: Optional[Dict]
    video: npt.NDArray[np.uint8]
    fps: int
    poses: npt.NDArray[np.float32]

    thumbnails: Optional[npt.NDArray[np.uint8]] = None
    thumbnail_size: Optional[int] = None


@dataclass
class LidarScene:
    labels: Optional[List[str]]
    frames: List[Frame]
    cameras: List[Camera]
    device: Device
