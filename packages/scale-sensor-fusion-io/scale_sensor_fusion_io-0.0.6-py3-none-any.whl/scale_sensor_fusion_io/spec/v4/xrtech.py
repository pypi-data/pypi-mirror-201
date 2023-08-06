from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt
from scale_sensor_fusion_io.spec.common.types import Pose
from typing_extensions import TypeAlias

from .types import LidarPoints

"""
Busted version of bs4 used for xrtech scenes currently

Noteable differences:
* device ids aren't set
* lidar point cloud is static
    * poses aren't set - we default to []
    * no fps or timestamp
* no radar support, so removed for simplicity

"""


@dataclass
class CameraSensor:
    camera_id: Optional[int]
    name: str
    poses: List[Pose]
    # Only one of fps or timestamps is required
    fps: Optional[float]
    # timestamp of frame 0 must be 0
    timestamps: Optional[List[float]]
    cx: float
    cy: float
    fx: float
    fy: float
    video: npt.NDArray[np.uint8]
    # model: str
    distortion: dict
    type: Literal["camera"]
    thumbnails: Optional[npt.NDArray[np.uint8]] = None
    thumbnail_size: Optional[int] = None

    def __init__(
        self,
        name: str,
        poses: List[Pose],
        cx: float,
        cy: float,
        fx: float,
        fy: float,
        video: npt.NDArray[np.uint8],
        distortion: dict,
        thumbnails: Optional[npt.NDArray[np.uint8]] = None,
        thumbnail_size: Optional[int] = None,
        fps: Optional[float] = None,
        timestamps: Optional[List[float]] = None,
        camera_id: Optional[int] = None,
        type: Literal["camera"] = "camera",  # Need this for dacite to work properly
    ):
        if not fps and not timestamps:
            raise Exception(f"{type} sensor must provide either fps or timestamps.")

        self.type = "camera"
        self.poses = poses
        self.fps = fps
        self.timestamps = timestamps

        self.camera_id = camera_id
        self.name = name
        self.cx = cx
        self.cy = cy
        self.fx = fx
        self.fy = fy
        self.video = video
        self.distortion = distortion
        self.thumbnails = thumbnails
        self.thumbnail_size = thumbnail_size


@dataclass
class LidarSensor:
    lidar_id: Optional[int]
    type: Literal["lidar"]

    # One of points and point_chunks must be provided
    points: Optional[LidarPoints] = None
    point_chunks: Optional[Dict[int, LidarPoints]] = None
    # frame_offsets contains the index of the points list corresponding to the start of each frame
    # This is used as a fallback in case timestamps sent by customer is not accurate
    frame_offsets: Optional[List[int]] = None
    # frame_ranges contains tuples of timestamps that indicate what a frame is
    # This is useful for handling flattened scenes
    frame_ranges: Optional[List[Tuple[float, float]]] = None

    def __init__(
        self,
        frame_offsets: Optional[List[int]] = [0],
        points: Optional[LidarPoints] = None,
        point_chunks: Optional[Dict[int, LidarPoints]] = None,
        frame_ranges: Optional[List[Tuple[float, float]]] = None,
        lidar_id: Optional[int] = None,
        type: Literal["lidar"] = "lidar",  # Need this for dacite to work properly
    ):
        self.type = "lidar"
        self.lidar_id = lidar_id
        self.points = points
        self.point_chunks = point_chunks
        self.frame_offsets = frame_offsets
        self.frame_ranges = frame_ranges


""" SPEC """

Sensor: TypeAlias = Union[CameraSensor, LidarSensor]


@dataclass
class BinaryScene:
    # One Sensor object per sensor type and per device. Each Sensor object contains all
    # encoded information, including points and image data. E.g. If there are 5 cameras,
    # 2 lidars, and 1 radar sensor, len(sensors) === 8.
    sensors: List[Sensor]
    version: str = "4.0"
