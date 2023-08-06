from fairscape_models.base import FairscapeBaseModel
from typing import Optional, Union, Dict, List
from pydantic import (
    constr,
    AnyUrl
)
from datetime import datetime

class Computation(FairscapeBaseModel):
    metadataType: Optional[str] = "https://w3id.org/EVI#Computation"
    runBy: str
    dateCreated: str
    description: constr(min_length=10, max_length=2056)
    associatedPublication: Optional[Union[str, AnyUrl]]
    additionalDocumentation: Optional[Union[str, AnyUrl]]
    command: Optional[Union[List[str], str]] 
    usedSoftware: List[str]
    calledBy: Optional[str]
    usedDataset: Union[List[str], str]
    generated: Union[str,List[str]]
     
