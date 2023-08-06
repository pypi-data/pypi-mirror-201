from fairscape_models.base import FairscapeBaseModel
from fairscape_models.dataset import Dataset
from fairscape_models.software import Software
from fairscape_models.computation import Computation

from typing import Optional, Union, Dict, List
from pydantic import (
    constr,
    AnyUrl
)
from datetime import datetime

class ROCrate(FairscapeBaseModel):

    name: str
    metadataType: str = "ROCrate" 
    graph: List[Union[Dataset, Software, Computation]]

    class Config: 
        fields={
            "graph": {
                "title": "graph",
                "alias": "@graph"
            }
        }

    def __repr__(self):

        return f"ROCrate(guid='{self.id}', metadataType='{self.type}', graph={self.graph})"

    def __str__(self):
        return self.dict(by_alias=True)
