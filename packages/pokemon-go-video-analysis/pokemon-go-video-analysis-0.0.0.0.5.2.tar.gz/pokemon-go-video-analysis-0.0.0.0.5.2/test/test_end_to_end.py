import os
import unittest

import pandas as pd
from ocr_ops.run_finding.interval import Interval

from battle_logger.op import BattleLoggerOp
from battle_logger.pipeline import BattleLoggerPipeline
from battle_logger.result import BattleLoggerResult


class TestEndToEnd(unittest.TestCase):
    def test_dep(self) -> None:
        """
        Test that the dependencies are installed.
        """

        # check availability of pkmn_data
        file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "pkmn_data",
            "pokemon_moves.csv",
        )
        self.assertTrue(os.path.exists(file))

    def test_end_to_end(self) -> None:
        """
        Test end-to-end functionality of the BattleLoggerPipeline on vals test video.
        """

        # test up paths
        data_path = os.path.join(os.path.dirname(__file__), "test_data")
        test_video_path = os.path.join(data_path, "test_video.mp4")
        out_root = "test_output"
        image_out_path = os.path.join(out_root, "images")
        autosave_output_img_path = os.path.join(out_root, "ocr_images")

        # create BattleLoggerPipeline
        pogo_pipeline = BattleLoggerPipeline()
        pogo_pipeline.set_output_paths(
            image_out_path=image_out_path,
            autosave_output_img_path=autosave_output_img_path,
        )
        output = pogo_pipeline.exec(test_video_path)
        self.assertTrue(isinstance(output, BattleLoggerResult))

        # check results
        self.assertTrue(len(output), 1)
        self.assertTrue(output[0].battle_interval.equals(Interval(0, 9)))
        self.assertEqual(
            output[0].opponent_pokemon_in_frames,
            {"plusle": [3], "electrode": [5, 6], "jolteon": [7]},
        )
        self.assertEqual(output[0].player_pokemon_in_frames, {"medicham": [3, 5, 6, 7]})
        self.assertTrue(output[0].player_won)

        # save to file and check
        battle_logger_op = pogo_pipeline.find_ops_by_class(op_class=BattleLoggerOp)[0]
        battle_logger_op.save_input(out_path=out_root, basename="ocr_output")

        # save output and check
        pogo_pipeline.save_output(out_path=out_root, basename="battle_logger_output")
        csv_file = [
            file for file in os.listdir(out_root) if "parse_battle_log.csv" in file
        ][0]
        self.assertTrue(os.path.exists(os.path.join(out_root, csv_file)))
        df = pd.read_csv(os.path.join(out_root, csv_file))
        self.assertEqual(len(df), 1)
