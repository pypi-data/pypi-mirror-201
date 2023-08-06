import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fairscape_models import Software

example_software = {

    "id": "ARK:calibrate_pariwise_distance.1/467f5ebd-cb29-43a1-beab-aa2d50606eff.py",
    "name": "calibrate pairwise distance",
    "type": "evi:Software",
    "author": "Qin, Y.",
    "dateModified": "2021-06-20",
    "version": "1.0",
    "description": "script written in python to calibrate pairwise distance.",
    "associatedPublication": "Qin, Y. et al. A multi-scale map of cell structure fusing protein images and interactions. Nature 600, 536–542 2021",
    "additionalDocumentation": ["https://idekerlab.ucsd.edu/music/"],
    "format": "py",
    "usedByComputation": ["ARK:compute_standard_proximities.1/f9aa5f3f-665a-4ab9-8879-8d0d52f05265"],
    "contentUrl": "https://github.com/idekerlab/MuSIC/blob/master/calibrate_pairwise_distance.py"
}



class TestSoftwareModel(unittest.TestCase):
    def test_model_init(self):
        software_model = Software(**example_software)

    def test_optional_properties(self):
        pass
