from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional, Union

import numpy as np
import numpy.typing as npt
from scale_sensor_fusion_io.spec.common import Pose, Size2D
from typing_extensions import TypeAlias

"""
Spec as defined in
https://docs.google.com/document/d/1Yf9x3nrB_69Y82KULgbwxGfvalgj606HLPyFGBOlEjo
"""

""" POINTS """


@dataclass
class PointCloud:
    positions: npt.NDArray[np.float32]
    # shape = (-1,3), dtype=np.uint8
    colors: Optional[npt.NDArray[np.uint8]] = None
    # shape = (-1,), dtype=np.uint8
    intensities: Optional[npt.NDArray[np.uint8]] = None
    # Metadata flags. A binary mask for specific boolean features.
    # shape = (-1,), dtype=np.uint8
    flags: Optional[npt.NDArray[np.uint8]] = None


@dataclass
class LidarPointCloud:
    # shape = (-1,3), dtype=np.float32
    # NOTE: positions MUST preserve order of the attachments provided
    positions: npt.NDArray[np.float32]
    # shape = (-1,3), dtype=np.uint8
    colors: Optional[npt.NDArray[np.uint8]] = None
    # shape = (-1,), dtype=np.uint8
    intensities: Optional[npt.NDArray[np.uint8]] = None
    # shape = (-1,), dtype=np.uint32
    timestamps: Optional[npt.NDArray[np.uint32]] = None
    # shape = (-1,), dtype=np.uint32
    labels: Optional[npt.NDArray[np.uint32]] = None
    # Metadata flags. A binary mask for specific boolean features.
    # shape = (-1,), dtype=np.uint8
    # Current flags (from least to most significant bit):
    # 0: is_outlier
    # 7: is_ground
    flags: Optional[npt.NDArray[np.uint8]] = None


@dataclass
class RadarPointCloud:
    # shape = (-1,3), dtype=np.float32
    # 2D array where `positions[i]` = `[x, y, z]` for point number i
    positions: npt.NDArray[np.float32]
    # shape = (-1,3), dtype=np.float32
    # 2D array where `directions[i]` = `[x, y, z]` for point number i
    directions: Optional[npt.NDArray[np.float32]] = None
    # shape = (-1,), dtype=np.float32
    sizes: Optional[npt.NDArray[np.float32]] = None
    # shape = (-1,), dtype=np.uint32
    timestamps: Optional[npt.NDArray[np.uint32]] = None
    # Metadata flags. A binary mask for specific boolean features.
    # shape = (-1,), dtype=np.uint8
    flags: Optional[npt.NDArray[np.uint8]] = None


""" SENSORS """


@dataclass
class SensorBase(ABC):
    type: Literal["camera", "lidar", "radar", "points"]
    sensor_id: int
    parent_sensor: Optional[int]


@dataclass
class PointsSensor(SensorBase):
    type: Literal["points"]
    points: PointCloud

    def __init__(
        self,
        sensor_id: int,
        points: PointCloud,
    ):
        self.type = "points"
        self.sensor_id = sensor_id
        self.points = points


@dataclass
class LidarSensorFrame:
    timestamp: int
    pose: Pose
    points: LidarPointCloud
    duration: Optional[float] = None


class CoordinateSystem(Enum):
    Local = "local"
    World = "world"


@dataclass
class LidarSensor(SensorBase):
    type: Literal["lidar"]
    frames: List[LidarSensorFrame]
    parent_sensor: Optional[int]
    # coordinates: CoordinateSystem = CoordinateSystem.World

    def __init__(
        self,
        sensor_id: int,
        frames: List[LidarSensorFrame],
        parent_sensor: Optional[int] = None,
        coordinates: CoordinateSystem = CoordinateSystem.World,
        type: Literal["lidar"] = "lidar",  # Need this for dacite to work properly
    ):
        self.type = "lidar"
        self.sensor_id = sensor_id
        self.frames = frames
        self.parent_sensor = parent_sensor
        # self.coordinates = coordinates


@dataclass
class RadarSensorFrame:
    timestamp: int
    pose: Pose
    points: RadarPointCloud
    duration: Optional[float] = None


@dataclass
class RadarSensor(SensorBase):
    type: Literal["radar"]
    frames: List[RadarSensorFrame]

    def __init__(
        self,
        sensor_id: int,
        frames: List[RadarSensorFrame],
        parent_sensor: Optional[int] = None,
        type: Literal["radar"] = "radar",  # Need this for dacite to work properly
    ):
        self.parent_sensor = parent_sensor
        self.type = "radar"
        self.sensor_id = sensor_id
        self.frames = frames


@dataclass
class VideoCameraContent:
    video: npt.NDArray[np.uint8]
    fps: float
    type: Literal["video"] = "video"


@dataclass
class ImagesCameraContent:
    images: List[npt.NDArray[np.uint8]]
    type: Literal["images"] = "images"


@dataclass
class CameraSensorFrame:
    pose: Pose
    timestamp: int
    image: Optional[npt.NDArray[np.uint8]]


CameraContent: TypeAlias = Union[VideoCameraContent, ImagesCameraContent]


@dataclass
class CameraSensor(SensorBase):
    type: Literal["camera"]
    name: str
    cx: float
    cy: float
    fx: float
    fy: float
    poses: List[Pose]
    timestamps: List[int]
    distortion: dict
    image_size: Optional[Size2D]
    content: CameraContent

    def __init__(
        self,
        sensor_id: int,
        name: str,
        cx: float,
        cy: float,
        fx: float,
        fy: float,
        poses: List[Pose],
        timestamps: List[int],
        distortion: dict,
        content: CameraContent,
        image_size: Optional[Size2D] = None,
        parent_sensor: Optional[int] = None,
        type: Literal["camera"] = "camera",  # Need this for dacite to work properly
    ):
        self.type = "camera"
        self.parent_sensor = parent_sensor

        self.sensor_id = sensor_id
        self.name = name
        self.cx = cx
        self.cy = cy
        self.fx = fx
        self.fy = fy
        self.poses = poses
        self.timestamps = timestamps
        self.content = content
        self.image_size = image_size
        self.images = content
        self.distortion = distortion


""" SPEC """


Sensor: TypeAlias = Union[PointsSensor, LidarSensor, RadarSensor, CameraSensor]


@dataclass
class Scene:
    sensors: List[Sensor]
    timestamp: Optional[int]
    pose: Optional[Pose]
    version: str = "5.0"
