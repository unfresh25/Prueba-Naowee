import ast

import pandas as pd


class ResultsService:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.base_matches = self._build_base_matches()
        self.matches = self._build_results_matches()

    @staticmethod
    def _parse_events(x) -> list:
        if pd.isna(x) or isinstance(x, list):
            return x if isinstance(x, list) else []
        if isinstance(x, str):
            try:
                parsed = ast.literal_eval(x)
                return parsed if isinstance(parsed, list) else []
            except (ValueError, SyntaxError):
                return []
        return []

    @staticmethod
    def _count_events(x) -> int:
        return len(ResultsService._parse_events(x))

    @staticmethod
    def _parse_penalty_goals(x) -> list:
        if pd.isna(x) or not isinstance(x, str):
            return []
        return [
            event.split("·")[0].replace("(P)", "").strip() for event in x.split("|")
        ]

    def _explode_events(self, df, event_col, team_col, parser):
        return (
            df[[event_col, team_col]]
            .dropna()
            .assign(player=lambda x: x[event_col].apply(parser))
            .explode("player")
            .drop(columns=event_col)
            .dropna()
            .rename(columns={team_col: "team"})
        )

    def _count_goal_assists(self, df, goal_col, team_col):
        return (
            df[[goal_col, team_col, "Year", "Host"]]
            .dropna(subset=[goal_col])
            .assign(events=lambda x: x[goal_col].apply(self._parse_events))
            .explode("events")
            .assign(has_assist=lambda x: x["events"].str.contains("Assist:"))
            .rename(columns={team_col: "team"})
            .groupby(["Year", "Host", "team"])["has_assist"]
            .sum()
            .reset_index(name="assists")
        )

    def _build_base_matches(self) -> pd.DataFrame:
        cols_home = [
            "Year",
            "Host",
            "Attendance",
            "home_team",
            "home_score",
            "away_score",
            "home_yellow_card_long",
            "home_red_card",
        ]
        cols_away = [
            "Year",
            "Host",
            "Attendance",
            "away_team",
            "away_score",
            "home_score",
            "away_yellow_card_long",
            "away_red_card",
        ]
        cols_final = [
            "Year",
            "Host",
            "Attendance",
            "team",
            "goals_for",
            "goals_against",
            "yellow_cards",
            "red_cards",
        ]

        home = self.data[cols_home].copy()
        home.columns = cols_final

        away = self.data[cols_away].copy()
        away.columns = cols_final

        return pd.concat([home, away], ignore_index=True)

    def _build_results_matches(self) -> pd.DataFrame:
        df = self.base_matches.copy()
        df["yellow_cards"] = df["yellow_cards"].apply(self._count_events)
        df["red_cards"] = df["red_cards"].apply(self._count_events)
        df["win"] = (df["goals_for"] > df["goals_against"]).astype(int)
        df["draw"] = (df["goals_for"] == df["goals_against"]).astype(int)
        df["loss"] = (df["goals_for"] < df["goals_against"]).astype(int)
        df["points"] = df["win"] * 3 + df["draw"]
        df["fair_play"] = -df["yellow_cards"] - 2 * df["red_cards"]
        return df

    def get_results(self) -> pd.DataFrame:
        results = (
            self.matches.groupby("team")
            .agg(
                GP=("team", "count"),
                W=("win", "sum"),
                D=("draw", "sum"),
                L=("loss", "sum"),
                GF=("goals_for", "sum"),
                GA=("goals_against", "sum"),
                FP=("fair_play", "sum"),
                Points=("points", "sum"),
            )
            .reset_index()
        )
        results["GD"] = results["GF"] - results["GA"]
        results = results[
            ["team", "GP", "W", "D", "L", "GF", "GA", "GD", "FP", "Points"]
        ]
        return results.sort_values(
            by=["Points", "GD"], ascending=False, ignore_index=True
        ).rename(columns={"team": "Team"})

    def top_scorers(
        self, include_penalties: bool = True, top_n: int = 10
    ) -> pd.DataFrame:
        parser = lambda x: [e.split("|")[2].strip() for e in self._parse_events(x)]

        goals_play = pd.concat(
            [
                self._explode_events(self.data, "home_goal_long", "home_team", parser),
                self._explode_events(self.data, "away_goal_long", "away_team", parser),
            ],
            ignore_index=True,
        )

        dfs = [goals_play]

        if include_penalties:
            penalties = pd.concat(
                [
                    self._explode_events(
                        self.data,
                        "home_penalty_goal",
                        "home_team",
                        self._parse_penalty_goals,
                    ),
                    self._explode_events(
                        self.data,
                        "away_penalty_goal",
                        "away_team",
                        self._parse_penalty_goals,
                    ),
                ],
                ignore_index=True,
            )
            dfs.append(penalties)

        scorers = (
            pd.concat(dfs, ignore_index=True)
            .value_counts(["player", "team"])
            .reset_index(name="Goals")
            .sort_values("Goals", ascending=False)
            .reset_index(drop=True)
        )

        scorers["Position"] = (
            scorers["Goals"].rank(method="min", ascending=False).astype(int)
        )
        scorers = scorers[["Position", "player", "team", "Goals"]].rename(
            columns={"player": "Player", "team": "Team"}
        )

        return scorers.sort_values(["Position", "Player"], ignore_index=True).head(
            top_n
        )

    def world_cup_summary(self) -> pd.DataFrame:
        summary = (
            self.matches.groupby(["Year", "Host", "team"])
            .agg(
                GP=("team", "count"),
                GF=("goals_for", "sum"),
                GF_avg=("goals_for", "mean"),
                GA=("goals_against", "sum"),
                GA_avg=("goals_against", "mean"),
                W=("win", "sum"),
                D=("draw", "sum"),
                L=("loss", "sum"),
            )
            .reset_index()
        )

        assists = (
            pd.concat(
                [
                    self._count_goal_assists(self.data, "home_goal_long", "home_team"),
                    self._count_goal_assists(self.data, "away_goal_long", "away_team"),
                ],
                ignore_index=True,
            )
            .groupby(["Year", "Host", "team"], as_index=False)["assists"]
            .sum()
        )

        summary = summary.merge(assists, on=["Year", "Host", "team"], how="left")
        summary["assists"] = summary["assists"].fillna(0)
        summary["Assist Avg"] = summary["assists"] / summary["GP"]

        summary = summary[
            [
                "Year",
                "Host",
                "team",
                "GP",
                "GF",
                "GF_avg",
                "GA",
                "GA_avg",
                "W",
                "D",
                "L",
                "Assist Avg",
            ]
        ]
        summary.columns = [
            "Year",
            "Host",
            "Team",
            "GP",
            "GF",
            "GF Avg",
            "GA",
            "GA Avg",
            "W",
            "D",
            "L",
            "Assist Avg",
        ]

        return summary.sort_values(
            by=["Year", "GF"], ascending=[True, False], ignore_index=True
        )
