import os
from typing import Optional

from algo_ops.ops.op import Op
from ocr_ops.framework.op.result.ocr_result import OCRPipelineResult

from battle_logger.ocr_log_parser import OCRLogParser
from battle_logger.result import BattleLoggerResult


class BattleLoggerOp(Op):
    def __init__(self):
        """
        Operation that parses the battle log and determines which Pokémon are in the battle.
        """
        super().__init__(func=self.parse_battle_log)
        self.ocr_log_parser = OCRLogParser()
        self.input: Optional[OCRPipelineResult] = None
        self.output: Optional[BattleLoggerResult] = None

    def parse_battle_log(self, ocr_result: OCRPipelineResult) -> BattleLoggerResult:
        """
        Parses the battle log and determines which Pokémon are in the battles.

        param ocr_result: OCRPipelineResult object containing the OCR result.

        return:
            BattleLoggerResult object containing the Pokémon in the battle.
        """

        # obtain the OCR result as vals dataframe of detected text boxes
        ocr_log_df = ocr_result.to_df()
        return self.ocr_log_parser.extract_battles(ocr_log_df=ocr_log_df)

    def vis(self) -> None:
        """
        Visualizes the result of the BattleLoggerOp operation.
        """
        if self.output is None:
            raise ValueError("Output is None. Run the operation first.")
        self.output.vis()

    def vis_input(self) -> None:
        """
        Visualizes the input to the BattleLoggerOp operation.
        """
        if self.input is None:
            raise ValueError("Input is None. Run the operation first.")
        print(self.input.to_df())

    def save_input(self, out_path: str, basename: Optional[str] = None) -> None:
        """
        Saves the input to the BattleLoggerOp operation.
        """
        if self.input is None:
            raise ValueError("Input is None. Run the operation first.")
        self.input.to_df().to_csv(
            os.path.join(out_path, basename + ".csv"), index=False
        )

    def save_output(self, out_path: str, basename: Optional[str] = None) -> None:
        """
        Saves the output of the BattleLoggerOp operation.
        """
        if self.output is None:
            raise ValueError("Output is None. Run the operation first.")
        self.output.to_df().to_csv(
            os.path.join(out_path, basename + ".csv"), index=False
        )
        self.output.plot(out_root=out_path, suppress_output=True)
