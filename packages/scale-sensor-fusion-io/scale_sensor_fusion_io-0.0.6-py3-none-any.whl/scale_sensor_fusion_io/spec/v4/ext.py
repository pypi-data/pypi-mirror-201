from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Sequence, Tuple, Union

import numpy as np
import numpy.typing as npt
from typing_extensions import TypeAlias

from .types import LidarPoints, Pose, RadarSensor, SensorBase

"""
This file defines a modified bs4 spec used for classic tool. We have a separate spec for classic to alleviate performance issues
"""


@dataclass
class LidarSensor(SensorBase):
    lidar_id: int
    type: Literal["lidar"]
    # One of points and point_chunks must be provided
    points: Optional[LidarPoints] = None
    point_chunks: Optional[Dict[int, LidarPoints]] = None
    # Classic tool requires ground points to already be separated
    ground_points: Optional[LidarPoints] = None
    # frame_offsets contains the index of the points list corresponding to the start of each frame
    # This is used as a fallback in case timestamps sent by customer is not accurate
    frame_offsets: List[int] = field(default_factory=list)
    # frame_ranges contains tuples of timestamps that indicate what a frame is
    # This is useful for handling flattened scenes
    frame_ranges: Optional[List[Tuple[float, float]]] = None

    def __init__(
        self,
        lidar_id: int,
        poses: List[Pose],
        frame_offsets: List[int],
        points: Optional[LidarPoints] = None,
        point_chunks: Optional[Dict[int, LidarPoints]] = None,
        ground_points: Optional[LidarPoints] = None,
        frame_ranges: Optional[List[Tuple[float, float]]] = None,
        fps: Optional[float] = None,
        timestamps: Optional[List[float]] = None,
    ):
        super().__init__("lidar", poses, fps, timestamps)
        self.lidar_id = lidar_id
        self.points = points
        self.ground_points = ground_points
        self.point_chunks = point_chunks
        self.frame_offsets = frame_offsets
        self.frame_ranges = frame_ranges


# This is a temp structure to support classic tooling
@dataclass
class ImagesCameraSensor(SensorBase):
    camera_id: int
    name: str
    cx: float
    cy: float
    fx: float
    fy: float
    images: List[npt.NDArray[np.uint8]]
    # model: str
    distortion: dict
    type: Literal["camera"]
    thumbnails: Optional[npt.NDArray[np.uint8]] = None
    thumbnail_size: Optional[int] = None

    def __init__(
        self,
        camera_id: int,
        poses: List[Pose],
        name: str,
        cx: float,
        cy: float,
        fx: float,
        fy: float,
        images: List[npt.NDArray[np.uint8]],
        distortion: dict,
        thumbnails: Optional[npt.NDArray[np.uint8]] = None,
        thumbnail_size: Optional[int] = None,
        fps: Optional[float] = None,
        timestamps: Optional[List[float]] = None,
    ):
        super().__init__("camera", poses, fps, timestamps)
        self.camera_id = camera_id
        self.name = name
        self.cx = cx
        self.cy = cy
        self.fx = fx
        self.fy = fy
        self.images = images
        self.distortion = distortion
        self.thumbnails = thumbnails
        self.thumbnail_size = thumbnail_size


Sensor: TypeAlias = Union[ImagesCameraSensor, LidarSensor, RadarSensor]


@dataclass
class BinaryScene:
    # One Sensor object per sensor type and per device. Each Sensor object contains all
    # encoded information, including points and image data. E.g. If there are 5 cameras,
    # 2 lidars, and 1 radar sensor, len(sensors) === 8.
    sensors: Sequence[Sensor]
    version: str = "4.0.0-classic"
