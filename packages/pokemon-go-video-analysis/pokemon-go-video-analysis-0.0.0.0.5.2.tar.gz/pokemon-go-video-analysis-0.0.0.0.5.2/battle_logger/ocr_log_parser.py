import os
from typing import List, Tuple, Dict

import numpy as np
import pandas as pd
from ocr_ops.run_finding.interval import Interval

from battle_logger.calc import find_runs_with_tol
from battle_logger.result import BattleLoggerResult, Battle


class OCRLogParser:
    """
    Parses the OCR log.
    """

    def __init__(self):
        # configuration
        self.opponent_pkmn_screen_coord = np.array([696, 164], dtype=float)
        self.my_pkmn_screen_coord = np.array([105, 164], dtype=float)
        self.max_text_dist: float = 50.0
        self.win_text: List[str] = ["you", "win"]
        self.loss_text: List[str] = ["good", "effort"]
        self.max_text_detections_on_win_loss_frame: int = 10

        # load Pokémon moves backend file
        pokemon_moves_df = pd.read_csv(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "pkmn_data",
                "pokemon_moves.csv",
            )
        )
        self.pokemon_moves_df = pokemon_moves_df

    def _isolate_win_loss_screen_intervals(
        self, ocr_log_df: pd.DataFrame
    ) -> Tuple[List[Interval], List[Interval]]:
        """
        Isolates the frame intervals in which the win or loss screen is shown.

        param ocr_log_df: Dataframe containing the OCR result.

        return:
            List of frame intervals in which the win screen is shown
            List of frame intervals in which the loss screen is shown
        """

        # find frames in which the player won or lost the battle
        win_textbox_indic = (
            ocr_log_df.text.str.lower()
            .str.contains("|".join(self.win_text))
            .values.astype(bool)
        )
        loss_text_box_indic = (
            ocr_log_df.text.str.lower()
            .str.contains("|".join(self.loss_text))
            .values.astype(bool)
        )
        win_txt_frames = ocr_log_df[win_textbox_indic].frame.unique()
        loss_txt_frames = ocr_log_df[loss_text_box_indic].frame.unique()
        win_screen_frames = [
            frame
            for frame in win_txt_frames
            if all(
                str(a)
                in " ".join(
                    ocr_log_df[ocr_log_df.frame == frame]
                    .text.str.lower()
                    .values.astype(str)
                )
                for a in self.win_text
            )
            and (
                np.sum(ocr_log_df.frame == frame)
                < self.max_text_detections_on_win_loss_frame
            )
        ]
        loss_screen_frames = [
            frame
            for frame in loss_txt_frames
            if all(
                str(a)
                in " ".join(
                    ocr_log_df[ocr_log_df.frame == frame]
                    .text.str.lower()
                    .values.astype(str)
                )
                for a in self.loss_text
            )
            and (
                np.sum(ocr_log_df.frame == frame)
                < self.max_text_detections_on_win_loss_frame
            )
        ]

        # do run finding on win and loss frames
        win_screen_intervals = find_runs_with_tol(vals=win_screen_frames, tol=1)
        loss_screen_intervals = find_runs_with_tol(vals=loss_screen_frames, tol=1)
        return win_screen_intervals, loss_screen_intervals

    def _identify_battle_intervals(
        self, ocr_log_df: pd.DataFrame
    ) -> Tuple[List[Interval], List[bool]]:
        """
        Identifies the unique battle intervals in the OCR log based on delineation by win/loss screens.

        param ocr_log_df: Dataframe containing the OCR result.

        return:
            List of battle intervals.
            List of booleans indicating whether the player won the battle in the corresponding battle interval.
        """

        # Find the frames in which the player won or lost the battle. Then find the frames in between the win/loss
        # screens that define the "battle intervals".
        (
            win_screen_intervals,
            loss_screen_intervals,
        ) = self._isolate_win_loss_screen_intervals(ocr_log_df=ocr_log_df)
        sorted_intervals: List[Interval] = sorted(
            win_screen_intervals + loss_screen_intervals, key=lambda run: run.start
        )
        battle_intervals = [Interval(0, sorted_intervals[0].start)]
        battle_intervals.extend(
            [
                Interval(sorted_intervals[i].end, sorted_intervals[i + 1].start)
                for i in range(len(sorted_intervals) - 1)
            ]
        )
        player_won: List[bool] = [False] * len(battle_intervals)
        for i in range(len(sorted_intervals)):
            if sorted_intervals[i] in win_screen_intervals:
                player_won[i] = True
        return battle_intervals, player_won

    def extract_battles(self, ocr_log_df: pd.DataFrame) -> BattleLoggerResult:
        """
        Extracts the battles from the video OCR text log.

        param ocr_log_df: Dataframe containing the OCR results for the video as a dataframe of detected text boxes.

        return:
            BattleLoggerResult object containing the extracted battles.
        """

        # parse frames
        ocr_log_df["frame"] = [
            int(os.path.basename(f).split(".")[0][3:]) for f in ocr_log_df.input_path
        ]

        # Run Pokémon filter on text in text boxes and identify text boxes with Pokémon names.
        all_pokemon_names = self.pokemon_moves_df["Pokémon"].str.lower().values
        found_pokemon = ocr_log_df.text.str.lower().str.contains(
            "|".join(all_pokemon_names)
        )
        found_pokemon[found_pokemon.isnull()] = False
        ocr_log_df["found_pokemon"] = ocr_log_df.text.str.lower().str.extract(
            "(" + "|".join(all_pokemon_names) + ")", expand=False
        )

        # Find battle intervals.
        battle_intervals, player_won = self._identify_battle_intervals(
            ocr_log_df=ocr_log_df
        )

        # Isolate text boxes that fall within player or the opponent's Pokémon screen locations.
        # Then find the "battle action frames" where both text boxes show up in the same frame.
        text_boxes = ocr_log_df.bounding_box.values.astype(str)
        starting_vertices = [
            text[str(text).find("(") + 2 : str(text).find(",")] for text in text_boxes
        ]
        starting_vertices = np.array(
            [[float(v.split()[0]), float(v.split()[1])] for v in starting_vertices],
            dtype=float,
        )
        d1 = np.sum(np.abs(starting_vertices - self.my_pkmn_screen_coord), 1)
        player_pkmn_text_boxes = ocr_log_df[
            (d1 < self.max_text_dist) & found_pokemon
        ].reset_index(drop=True)
        d2 = np.sum(np.abs(starting_vertices - self.opponent_pkmn_screen_coord), 1)
        opponent_pkmn_text_boxes = ocr_log_df[
            (d2 < self.max_text_dist) & found_pokemon
        ].reset_index(drop=True)
        battle_action_frames = sorted(
            list(
                set(player_pkmn_text_boxes.frame.unique()).intersection(
                    set(opponent_pkmn_text_boxes.frame.unique())
                )
            )
        )

        # prepare BattleLoggerResult
        battles: List[Battle] = list()
        for i, battle_interval in enumerate(battle_intervals):
            # identify frames in battle
            battle_action_frames_in_interval = [
                frame
                for frame in battle_action_frames
                if battle_interval.start <= frame <= battle_interval.end
            ]

            # identify Pokémon in battle
            player_battle_pokemon = (
                player_pkmn_text_boxes[
                    player_pkmn_text_boxes.frame.isin(battle_action_frames_in_interval)
                ]
                .text.str.lower()
                .unique()
            )
            opponent_battle_pokemon = (
                opponent_pkmn_text_boxes[
                    opponent_pkmn_text_boxes.frame.isin(
                        battle_action_frames_in_interval
                    )
                ]
                .text.str.lower()
                .unique()
            )
            assert len(player_battle_pokemon) <= 3
            assert len(opponent_battle_pokemon) <= 3

            # identifying mapping of Pokémon to frame appearances in battle
            player_pokemon_in_frames: Dict[str, List[int]] = dict()
            for pkmn in player_battle_pokemon:
                player_pokemon_in_frames[pkmn] = (
                    player_pkmn_text_boxes[
                        (player_pkmn_text_boxes.text.str.lower() == pkmn)
                        & (
                            player_pkmn_text_boxes.frame.isin(
                                battle_action_frames_in_interval
                            )
                        )
                    ]
                    .frame.unique()
                    .tolist()
                )
            opponent_pokemon_in_frames: Dict[str, List[int]] = dict()
            for pkmn in opponent_battle_pokemon:
                opponent_pokemon_in_frames[pkmn] = (
                    opponent_pkmn_text_boxes[
                        (opponent_pkmn_text_boxes.text.str.lower() == pkmn)
                        & (
                            opponent_pkmn_text_boxes.frame.isin(
                                battle_action_frames_in_interval
                            )
                        )
                    ]
                    .frame.unique()
                    .tolist()
                )

            # create battle object
            battle = Battle(
                battle_interval=battle_interval,
                player_pokemon_in_frames=player_pokemon_in_frames,
                opponent_pokemon_in_frames=opponent_pokemon_in_frames,
                player_won=player_won[i],
            )
            battles.append(battle)

        # create BattleLoggerResult object
        battle_logger_result = BattleLoggerResult(battles=battles)
        return battle_logger_result
