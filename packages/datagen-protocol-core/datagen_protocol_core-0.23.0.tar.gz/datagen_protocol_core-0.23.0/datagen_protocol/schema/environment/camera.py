from enum import Enum, IntEnum

from datagen_protocol.config import conf
from datagen_protocol.schema import fields
from datagen_protocol.schema.base import SchemaBaseModel
from datagen_protocol.schema.d3 import Point, Rotation
from pydantic import Field


class CameraProjection(str, Enum):
    PERSPECTIVE = "perspective"


class SequenceCameraProjection(str, Enum):
    PERSPECTIVE = "perspective"
    PANORAMIC = "panoramic"
    ORTHOGRAPHIC = "orthographic"


class Wavelength(str, Enum):
    VISIBLE = "visible"
    NIR = "nir"


class FramesPerSecond(IntEnum):
    FPS_0 = 0
    FPS_1 = 1
    FPS_5 = 5
    FPS_10 = 10
    FPS_15 = 15
    FPS_30 = 30
    FPS_60 = 60


class CameraIntrinsicParams(SchemaBaseModel):
    projection: CameraProjection = fields.enum(CameraProjection, conf["camera"]["projection"])
    wavelength: Wavelength = fields.enum(Wavelength, conf["camera"]["wavelength"])
    resolution_height: int = fields.numeric(conf["camera"]["res"]["height"])
    resolution_width: int = fields.numeric(conf["camera"]["res"]["width"])
    fov_horizontal: int = fields.numeric(conf["camera"]["fov"]["horizontal"])
    fov_vertical: int = fields.numeric(conf["camera"]["fov"]["vertical"])
    sensor_width: float = fields.numeric(conf["camera"]["sensor"]["width"])

    def dict(self, exclude_none=True, **kwargs):
        return super().dict(exclude_none=exclude_none, **kwargs)

    class Config:
        validate_assignment = True


class CameraExtrinsicParams(SchemaBaseModel):
    location: Point = fields.point(conf["camera"]["location"])
    rotation: Rotation = fields.rotation(conf["camera"]["rotation"])


class Camera(SchemaBaseModel):
    name: str = conf["camera"]["name"]
    extrinsic_params: CameraExtrinsicParams = Field(default_factory=CameraExtrinsicParams)
    intrinsic_params: CameraIntrinsicParams = Field(default_factory=CameraIntrinsicParams)


class SequenceIntrinsicParams(CameraIntrinsicParams):
    projection: SequenceCameraProjection = fields.enum(SequenceCameraProjection, conf["camera"]["projection"])
    fps: FramesPerSecond = fields.enum(FramesPerSecond, conf["camera"]["fps"])


class SequenceCamera(Camera):
    intrinsic_params: SequenceIntrinsicParams = Field(default_factory=SequenceIntrinsicParams)
