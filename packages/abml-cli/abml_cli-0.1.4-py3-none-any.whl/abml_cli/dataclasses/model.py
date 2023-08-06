from pydantic import BaseModel, Field, validator
from typing import Literal, List, Optional
from enum import Enum

# from jinja2 import Template
import json
import os


class Sketch_Rect(BaseModel):
    type: Literal["rect"]
    p1: List[int | float | str] = Field(min_items=2, max_items=2)
    p2: List[int | float | str] = Field(min_items=2, max_items=2)


class Sketch_Line(BaseModel):
    type: Literal["line"]
    p1: List[int | float] = Field([0, 0], min_items=2, max_items=2, example=[0, 0])
    p2: List[int | float] = Field([10, 10], min_items=2, max_items=2, example=[10, 10])


class Sketch_Circle(BaseModel):
    type: Literal["circle"]
    center: List[int | float] = Field(min_items=2, max_items=2)
    r1: List[int | float] = Field(min_items=2, max_items=2)


class Sketch_Ellipse(BaseModel):
    type: Literal["ellipse"]
    center: List[int | float] = Field(min_items=2, max_items=2)
    r1: List[int | float] = Field(min_items=2, max_items=2)
    r2: List[int | float] = Field(min_items=2, max_items=2)


class Sketch_Arc_Center_Ends(BaseModel):
    type: Literal["arc_center_2points"]
    center: List[int | float] = Field(min_items=2, max_items=2)
    p1: List[int | float] = Field(min_items=2, max_items=2)
    p2: List[int | float] = Field(min_items=2, max_items=2)


class Sketch_Arc_3Points(BaseModel):
    type: Literal["arc_3points"]
    p1: List[int | float] = Field(min_items=2, max_items=2, default=[0, 0])
    p2: List[int | float] = Field(min_items=2, max_items=2)
    p3: List[int | float] = Field(min_items=2, max_items=2)


class Sketch_Autotrim(BaseModel):
    type: Literal["arc_3points"]
    p1: List[int | float] = Field(min_items=2, max_items=2)


class PartTypes(str, Enum):
    extrusion = "extrusion"


class PartShapes(str, Enum):
    solid = "solid"
    shell = "shell"


class Part(BaseModel):
    """_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    name: str = Field(title="name", description="name of of the part")
    type: PartTypes = Field(title="type")
    shape: PartShapes = Field(title="shape")
    sketch: list[
        Sketch_Rect
        | Sketch_Line
        | Sketch_Circle
        | Sketch_Ellipse
        | Sketch_Arc_Center_Ends
        | Sketch_Arc_3Points
        | Sketch_Autotrim
    ]
    depth: Optional[float]

    @validator("depth")
    def valdiate_optional_depth(cls, v, values, **kwargs):  # noqa
        if values["type"] not in ["extrusion"]:
            raise ValueError("type extrusion must conatin a depth")

    class Config:
        arbitrary_types_allowed = True


class Part_Extrude_Solid_Rect(BaseModel):
    """_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    name: str = Field(title="name", description="name of of the part")
    type: PartTypes = Field(title="type", default="extrusion")
    shape: PartShapes = Field(title="shape", default="solid")
    sketch: Sketch_Rect
    depth: float


class Part_Extrude_Solid_Cylinder(BaseModel):
    """_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    name: str = Field(title="name", description="name of of the part")
    type: PartTypes = Field(title="type", default="extrusion")
    shape: PartShapes = Field(title="shape", default="solid")
    sketch: Sketch_Circle
    depth: float


class Models(BaseModel):
    """_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    name: str = Field(title="name", description="name of of the model")
    parts: list[Part | Part_Extrude_Solid_Rect | Part_Extrude_Solid_Cylinder] = Field(
        title="parts", description="list of part objects"
    )

    class Config:
        arbitrary_types_allowed = True


class Base(BaseModel):
    """_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    models: list[Models] = Field(title="parts", description="list of part objects")


if __name__ == "__main__":
    data = Base.schema()
    data["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    data["$id"] = "https://example.com/product.schema.json"
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, "abml_schema.json"), mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
