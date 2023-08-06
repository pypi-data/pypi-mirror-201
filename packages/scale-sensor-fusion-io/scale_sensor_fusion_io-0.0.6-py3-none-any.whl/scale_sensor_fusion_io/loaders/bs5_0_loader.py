from enum import Enum
from typing import Optional, cast

import dacite
import scale_sensor_fusion_io.spec.v5.types_0 as BS5_0
from scale_json_binary import JSONBinaryEncoder

encoder = JSONBinaryEncoder()


def fix_data_shape(scene: BS5_0.Scene) -> BS5_0.Scene:
    """
    When reading via dacite, the numpy arrays aren't correctly shaped (since that's not included in the typedef)
    This function fixes all the fields that need to be reshaped
    """
    for sensor in scene.sensors:
        if sensor.type == "lidar":
            for l_frame in sensor.frames:
                l_frame.points.positions = l_frame.points.positions.reshape(-1, 3)
                if l_frame.points.colors is not None:
                    l_frame.points.colors = l_frame.points.colors.reshape(-1, 3)

        elif sensor.type == "radar":
            for r_frame in sensor.frames:
                r_frame.points.positions = r_frame.points.positions.reshape(-1, 3)
                if r_frame.points.directions is not None:
                    r_frame.points.directions = r_frame.points.directions.reshape(-1, 3)

        elif sensor.type == "points":
            sensor.points.positions = sensor.points.positions.reshape(-1, 3)
    return scene


class BS5_0Loader:
    def __init__(
        self,
        scene_url: str,
        skip_typecheck: bool = False,
    ):
        self.scene_url = scene_url
        self.skip_typecheck = skip_typecheck

    def load(self) -> BS5_0.Scene:
        raw_data: bytes
        with open(self.scene_url, "rb") as fd:
            raw_data = cast(bytes, fd.read())

        obj = encoder.loads(raw_data)
        if "version" not in obj or not obj["version"].startswith("5.0"):
            raise Exception(f"Cannot load scene with version {obj['version']}")

        scene_bs5 = dacite.from_dict(
            data_class=BS5_0.Scene,
            data=obj,
            config=dacite.Config(
                cast=[Enum, tuple],
                # check_types=(not self.skip_typecheck),
            ),
        )

        print(scene_bs5)
        scene = fix_data_shape(scene_bs5)

        return scene
