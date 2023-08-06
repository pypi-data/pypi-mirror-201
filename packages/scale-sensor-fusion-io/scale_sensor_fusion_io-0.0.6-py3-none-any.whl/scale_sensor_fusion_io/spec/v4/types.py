from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Tuple, Union

import numpy as np
import numpy.typing as npt
from scale_sensor_fusion_io.spec.common.types import Pose
from typing_extensions import TypeAlias

"""
This file contains type definitions for our external representation of 3D attachment
and binary point cloud. This is separate from `internal_types.py`, which contains type
definitions for our internal representation (which will only be used during the EKS
attachment processing job).

This similar, but separate from `internal_types.py`, because it provides a more
frontend-friendly way to organize data.

Please see our "Binary Point Cloud Specification" for details:
https://docs.google.com/document/d/1rI1DN8E7_VkAukFy5yvKMGaF3tv97gDl8olnkVyNOMA/
"""

""" POINTS """


@dataclass
class LidarPoints:
    # shape = (-1,3), dtype=np.float32
    # NOTE: positions MUST preserve order of the attachments provided
    positions: npt.NDArray[np.float32]

    # shape = (-1,3), dtype=np.uint8
    colors: Optional[npt.NDArray[np.uint8]] = None

    # shape = (-1,), dtype=np.uint8
    intensities: Optional[npt.NDArray[np.uint8]] = None
    # Normally, we would want to split up this up into separate sensor devices, but for
    # backwards-compatibility, we need to encode this information into a single device
    # Main reason is that order of points matter, and splitting up data by device_ids will
    # make us lose that order
    # shape = (-1,), dtype=np.uint8
    device_ids: Optional[npt.NDArray[np.uint8]] = None
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
    # Current flags (from least to most significant bit):
    # 0: is_outlier
    # 7: is_ground
    flags: Optional[npt.NDArray[np.uint8]] = None


@dataclass
class RadarPoints:
    # shape = (-1,3), dtype=np.float32
    # 2D array where `positions[i]` = `[x, y, z]` for point number i
    positions: npt.NDArray[np.float32]
    # shape = (-1,3), dtype=np.float32
    # 2D array where `directions[i]` = `[x, y, z]` for point number i
    directions: Optional[npt.NDArray[np.float32]] = None
    # shape = (-1,), dtype=np.float32
    sizes: Optional[npt.NDArray[np.float32]] = None
    # For tasks with frames, timestamps are used to derive which points belong in which frames.
    # Given the fps from a Device, the 0th frame contains all points with timestamps in the
    # first 1/fps second, and so on.
    # shape = (-1,), dtype=np.float32
    timestamps: Optional[npt.NDArray[np.float32]] = None
    # Metadata flags. A binary mask for specific boolean features.
    # shape = (-1,), dtype=np.uint32
    flags: Optional[npt.NDArray[np.uint8]] = None


""" SENSORS """


@dataclass
class SensorBase(ABC):
    type: Literal["camera", "lidar", "radar"]
    poses: List[Pose]
    # Only one of fps or timestamps is required
    fps: Optional[float]
    # shape = (-1,), dtype=np.float32
    # timestamp of frame 0 must be 0
    timestamps: Optional[List[float]]

    def __init__(
        self,
        type: Literal["camera", "lidar", "radar"],
        poses: List[Pose],
        fps: Optional[float] = None,
        timestamps: Optional[List[float]] = None,
    ):
        if not fps and not timestamps:
            raise Exception(f"{type} sensor must provide either fps or timestamps.")

        self.type = type
        self.poses = poses
        self.fps = fps
        self.timestamps = timestamps


@dataclass
class CameraSensor(SensorBase):
    camera_id: int
    name: str
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
        camera_id: int,
        poses: List[Pose],
        name: str,
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
        type: Literal["camera"] = "camera",  # Need this for dacite to work properly
    ):
        super().__init__("camera", poses, fps, timestamps)
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
class LidarSensor(SensorBase):
    lidar_id: int
    type: Literal["lidar"]
    # One of points and point_chunks must be provided
    points: Optional[LidarPoints] = None
    point_chunks: Optional[Dict[int, LidarPoints]] = None
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
        frame_ranges: Optional[List[Tuple[float, float]]] = None,
        fps: Optional[float] = None,
        timestamps: Optional[List[float]] = None,
        type: Literal["lidar"] = "lidar",  # Need this for dacite to work properly
    ):
        super().__init__("lidar", poses, fps, timestamps)
        self.lidar_id = lidar_id
        self.points = points
        self.point_chunks = point_chunks
        self.frame_offsets = frame_offsets
        self.frame_ranges = frame_ranges


@dataclass
class RadarSensor(SensorBase):
    radar_id: int
    type: Literal["radar"]
    points: RadarPoints
    # frame_offsets contains the index of the points list corresponding to the start of each frame
    # This is used as a fallback in case timestamps sent by customer is not accurate
    frame_offsets: List[int] = field(default_factory=list)
    # frame_ranges contains tuples of timestamps that indicate what a frame is
    # This is useful for handling flattened scenes
    frame_ranges: Optional[List[Tuple[float, float]]] = None

    def __init__(
        self,
        radar_id: int,
        poses: List[Pose],
        points: RadarPoints,
        frame_offsets: List[int],
        frame_ranges: Optional[List[Tuple[float, float]]] = None,
        fps: Optional[float] = None,
        timestamps: Optional[List[float]] = None,
        type: Literal["radar"] = "radar",  # Need this for dacite to work properly
    ):
        super().__init__("radar", poses, fps, timestamps)
        self.radar_id = radar_id
        self.points = points
        self.frame_offsets = frame_offsets
        self.frame_ranges = frame_ranges


""" SPEC """


Sensor: TypeAlias = Union[CameraSensor, LidarSensor, RadarSensor]


@dataclass
class BinaryScene:
    # One Sensor object per sensor type and per device. Each Sensor object contains all
    # encoded information, including points and image data. E.g. If there are 5 cameras,
    # 2 lidars, and 1 radar sensor, len(sensors) === 8.
    sensors: List[Sensor]
    version: str = "4.0.0"
