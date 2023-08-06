from dataclasses import dataclass


@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float


@dataclass
class Size2D:
    width: float
    height: float


@dataclass
class Pose:
    position: Point3D
    heading: Quaternion
