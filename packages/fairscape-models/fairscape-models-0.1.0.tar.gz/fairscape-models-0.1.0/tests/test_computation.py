import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fairscape_models import Computation


test_computation = {
    "id": "ARK:average_predicted_protein_proximities.1/c295abcd-8ad8-44ff-95e3-e5e65f1667da",
    "name": "average predicted protein proximities",
    "type": "evi:Computation",
    "runBy": "Qin, Y.",
    "dateCreated": "2021-05-23",
    "description": "Average the predicted proximities",
    "usedSoftware":[
      "random_forest_output (https://github.com/idekerlab/MuSIC/blob/master/random_forest_output.py)"
    ],
    "usedDataset": [ 
"""predicted protein proximities:
Fold 1 proximities:
    IF_emd_1_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_1.pkl""",
    "IF_emd_2_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_1.pkl",
"""Fold 1 proximities:
      IF_emd_1_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_2.pkl""",
    "IF_emd_2_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_2.pkl",
"""Fold 1 proximities:
      IF_emd_1_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_3.pkl""",
    "IF_emd_2_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_3.pkl",
"""Fold 1 proximities:
      IF_emd_1_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_4.pkl""",
    "IF_emd_2_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_4.pkl",
"""Fold 1 proximities:
      IF_emd_1_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_5.pkl""",
"IF_emd_2_APMS_emd_1.RF_maxDep_30_nEst_1000.fold_5.pkl"
    ],
    "generated": [
    "averages of predicted protein proximities (https://github.com/idekerlab/MuSIC/blob/master/Examples/MuSIC_predicted_proximity.txt)"
]

}

class TestComputationModel(unittest.TestCase):
    def test_model_init(self):
        computation_model = Computation(**test_computation)


    def test_optional_properties(self):
        pass
