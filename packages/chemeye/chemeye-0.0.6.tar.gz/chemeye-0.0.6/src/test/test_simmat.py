import unittest
import naclo
from chemeye import SimMat
from plotly.graph_objects import Figure
import numpy as np


class TestSimMat(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_smiles = [
            'CCC',
            'O',
            'C',
            'SOO'
        ]
        test_mols = naclo.smiles_2_mols(test_smiles)
        
        cls.ecfp4_prints = naclo.mols_2_ecfp(test_mols, radius=2, return_numpy=False)
        cls.ecfp6_prints = naclo.mols_2_ecfp(test_mols, radius=3, return_numpy=False)
        cls.maccs_keys = naclo.mols_2_maccs(test_mols)
        
        return super().setUpClass()
    
    def test_sim_matrix(self):
        mat_maccs = SimMat.sim_matrix(self.maccs_keys, self.maccs_keys, key_type='maccs')  # Test MACCS keys
        mat_ecfp4 = SimMat.sim_matrix(self.ecfp4_prints, self.ecfp4_prints)  # Test ECFP4
        mat_ecfp6 = SimMat.sim_matrix(self.ecfp6_prints, self.ecfp6_prints)  # Test ECFP6
        
        # Check same molecules equal 1 in matrix in all cases (along identity)
        arr_len = len(self.ecfp4_prints)
        np.testing.assert_array_equal(
            mat_maccs[np.eye(arr_len, dtype=bool)],
            mat_ecfp4[np.eye(arr_len, dtype=bool)],
            mat_ecfp6[np.eye(arr_len, dtype=bool)],
            arr_len*[1]
        )
        
        # Check maccs is different than ecfp but ecfp4,6 are equal
        self.assertFalse(
            np.array_equal(
                mat_maccs,
                mat_ecfp4
            )
        )
        self.assertTrue(
            np.array_equal(
                mat_ecfp4,
                mat_ecfp6
            )
        )
        
    def test_main(self):
        simmat = SimMat(self.ecfp4_prints, self.ecfp4_prints)
        fig, sim_arr = simmat.main()
        
        self.assertIsInstance(
            fig,
            Figure
        )
        self.assertIsInstance(
            sim_arr,
            np.ndarray
        )

      
if __name__ == '__main__':
    unittest.main()
