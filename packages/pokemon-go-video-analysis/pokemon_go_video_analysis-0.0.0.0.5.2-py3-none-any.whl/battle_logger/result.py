import os
from typing import Dict, List, Optional, Any

import ezplotly as ep
import pandas as pd
from ezplotly import EZPlotlyPlot
from ocr_ops.run_finding.interval import Interval


class Battle:
    def __init__(
        self,
        battle_interval: Interval,
        player_pokemon_in_frames: Dict[str, List[int]],
        opponent_pokemon_in_frames: Dict[str, List[int]],
        player_won: bool,
    ):
        # data quality checks
        if len(player_pokemon_in_frames.keys()) > 3:
            raise ValueError("Player can only have 3 pokemon")
        if len(opponent_pokemon_in_frames.keys()) > 3:
            raise ValueError("Opponent can only have 3 pokemon")
        for pokemon in player_pokemon_in_frames.keys():
            frames = player_pokemon_in_frames[pokemon]
            if any(not battle_interval.contains(frame) for frame in frames):
                raise ValueError(
                    "Player pokemon frames must be in battle interval. The following frames were not "
                    "in the battle interval: "
                    + str(frames)
                    + " for pokemon "
                    + pokemon
                    + "."
                )
        for pokemon in opponent_pokemon_in_frames.keys():
            frames = opponent_pokemon_in_frames[pokemon]
            if any(not battle_interval.contains(frame) for frame in frames):
                raise ValueError(
                    "Opponent pokemon frames must be in battle interval. The following frames were not "
                    "in the battle interval: "
                    + str(frames)
                    + " for pokemon "
                    + pokemon
                    + "."
                )

        # set data
        self.battle_interval: Interval = battle_interval
        self.player_pokemon_in_frames: Dict[str, List[int]] = player_pokemon_in_frames
        self.opponent_pokemon_in_frames: Dict[
            str, List[int]
        ] = opponent_pokemon_in_frames
        self.player_won: bool = player_won

    def plot(
        self,
        outfile: Optional[str] = None,
        suppress_output: bool = False,
    ) -> None:
        """
        Plots the result of the BattleLoggerOp operation.

        param outfile: The path to the output file. If None, the plot is not saved to file.
        param suppress_output: If True, the plot is not displayed.
        """

        h: List[Optional[EZPlotlyPlot]] = [None] * (
            len(self.player_pokemon_in_frames.keys())
            + len(self.opponent_pokemon_in_frames.keys())
        )
        whose_pokemon = ["Player"] * len(self.player_pokemon_in_frames.keys()) + [
            "Opponent"
        ] * len(self.opponent_pokemon_in_frames.keys())
        for i, hit in enumerate(self.player_pokemon_in_frames.keys()):
            matched_indices = self.player_pokemon_in_frames[hit]
            h[i] = ep.scattergl(
                x=matched_indices,
                y=[whose_pokemon[i] + " " + hit] * len(matched_indices),
                xlabel="Video Frame",
                ylabel="Detected Pokemon",
            )
        for i, hit in enumerate(self.opponent_pokemon_in_frames.keys()):
            matched_indices = self.opponent_pokemon_in_frames[hit]
            h[i + len(self.player_pokemon_in_frames.keys())] = ep.scattergl(
                x=matched_indices,
                y=[
                    whose_pokemon[i + len(self.player_pokemon_in_frames.keys())]
                    + " "
                    + hit
                ]
                * len(matched_indices),
                xlabel="Video Frame",
                ylabel="Detected Pokemon",
            )
        ep.plot_all(
            h, panels=[1] * len(h), outfile=outfile, suppress_output=suppress_output
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Output battle to dictionary
        """
        player_pokemon_names = list(self.player_pokemon_in_frames.keys())
        player_pokemon_frames = list(self.player_pokemon_in_frames.values())
        opponent_pokemon_names = list(self.opponent_pokemon_in_frames.keys())
        opponent_pokemon_frames = list(self.opponent_pokemon_in_frames.values())
        rtn_dict: Dict[str, Any] = dict()
        rtn_dict["battle_interval"] = "[" + str(self.battle_interval) + "]"

        # player Pokémon log
        i = 0
        for i, player_pokemon in enumerate(player_pokemon_names):
            rtn_dict["player_pokemon_" + str(i + 1)] = player_pokemon
        if i != 2:
            for j in range(i + 1, 3):
                rtn_dict["player_pokemon_" + str(j + 1)] = None

        # opponent Pokémon log
        i = 0
        for i, opponent_pokemon in enumerate(opponent_pokemon_names):
            rtn_dict["opponent_pokemon_" + str(i + 1)] = opponent_pokemon
        if i != 2:
            for j in range(i + 1, 3):
                rtn_dict["opponent_pokemon_" + str(j + 1)] = None

        # battle result log
        rtn_dict["player_won"] = self.player_won

        # frames log
        for i, player_pokemon in enumerate(player_pokemon_names):
            rtn_dict[
                "player_pokemon_" + str(i + 1) + "_frames"
            ] = player_pokemon_frames[i]
        if i != 2:
            for j in range(i + 1, 3):
                rtn_dict["player_pokemon_" + str(j + 1) + "_frames"] = None
        for i, opponent_pokemon in enumerate(opponent_pokemon_names):
            rtn_dict[
                "opponent_pokemon_" + str(i + 1) + "_frames"
            ] = opponent_pokemon_frames[i]
        if i != 2:
            for j in range(i + 1, 3):
                rtn_dict["opponent_pokemon_" + str(j + 1) + "_frames"] = None

        # return dictionary
        return rtn_dict


class BattleLoggerResult:
    """
    Result of the BattleLoggerOp operation.
    """

    def __init__(self, battles: List[Battle]):
        self.battles = battles

    def to_df(self) -> pd.DataFrame:
        """
        Output battles to dataframe.
        """
        return pd.DataFrame([battle.to_dict() for battle in self.battles])

    def plot(
        self,
        out_root: Optional[str] = None,
        suppress_output: bool = False,
    ) -> None:
        """
        Plots the result of the BattleLoggerOp operation.

        param outfile: The path to the output file. If None, the plot is not saved to file.
        param suppress_output: If True, the plot is not displayed.
        """
        if out_root is not None:
            os.makedirs(out_root, exist_ok=True)
        for i, battle in enumerate(self.battles):
            outfile = None
            if out_root is not None:
                outfile = os.path.join(out_root, "battle_" + str(i + 1) + ".png")
            battle.plot(outfile=outfile, suppress_output=suppress_output)

    def vis(self):
        """
        Visualize the battles.
        """
        self.plot(suppress_output=False, out_root=None)

    def __len__(self):
        return len(self.battles)

    def __getitem__(self, item: int):
        return self.battles[item]

    def __setitem__(self, key: int, value: Battle):
        self.battles[key] = value
