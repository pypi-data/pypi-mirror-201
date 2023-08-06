import unittest
import plotly.graph_objects as go
import numpy as np

import naclo
from chemeye import TSNE


class TestTSNE(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_smiles = [
            'CCC',
            'O',
            'C',
            'SOO'
        ]
        test_mols = naclo.smiles_2_mols(test_smiles)
        
        cls.ecfp4_prints = naclo.mols_2_ecfp(test_mols, radius=2, return_numpy=True)
        # cls.ecfp6_prints = naclo.mols_2_ecfp(test_mols, radius=3, return_numpy=False)
        # cls.maccs_keys = naclo.mols_2_maccs(test_mols)
        
        return super().setUpClass()
    
    # def test_plot(self):
    #     fig = self.tsne.plot('tsne1', 'tsne2', [1, 'a', True])
        
    #     self.assertIsInstance(
    #         fig,
    #         go.Figure
    #     )
    
    def test_tsne(self):
        print(self.ecfp4_prints)
        # print(self.ecfp4_prints.shape)
        tsne = TSNE(self.ecfp4_prints)
        tsne.main()
        # print(tsne)


if __name__ == '__main__':
    unittest.main()
