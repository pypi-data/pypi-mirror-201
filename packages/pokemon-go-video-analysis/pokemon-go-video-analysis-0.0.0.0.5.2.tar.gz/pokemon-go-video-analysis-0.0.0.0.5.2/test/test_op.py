import unittest

import pandas as pd
import os

from battle_logger.ocr_log_parser import OCRLogParser
from battle_logger.op import BattleLoggerOp


class TestBattleLoggerOp(unittest.TestCase):
    def test_ocr_log_parser(self) -> None:
        """
        Test that the OCRLogParser returns the correct result on a test file.
        """
        log_path = os.path.join(
            os.path.dirname(__file__), "test_data", "ocr_output.csv"
        )
        ocr_log_df = pd.read_csv(log_path)
        ocr_log_parser = OCRLogParser()
        result = ocr_log_parser.extract_battles(ocr_log_df=ocr_log_df)
        self.assertTrue(result is not None)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            list(result[0].player_pokemon_in_frames.keys()),
            ["gyarados", "swampert", "muk"],
        )
        self.assertEqual(
            list(result[0].opponent_pokemon_in_frames.keys()),
            ["dialga", "primarina", "clefable"],
        )
        self.assertEqual(
            list(result[1].player_pokemon_in_frames.keys()),
            ["gyarados", "swampert", "muk"],
        )
        self.assertEqual(
            list(result[1].opponent_pokemon_in_frames.keys()),
            ["umbreon", "gyarados", "escavalier"],
        )
        self.assertTrue(~result[0].player_won)
        self.assertTrue(~result[1].player_won)

        # save and plot
        result.plot(out_root="test_op_output", suppress_output=True)
        result.to_df().to_csv(
            os.path.join("test_op_output", "test_op_output.csv"), index=False
        )
