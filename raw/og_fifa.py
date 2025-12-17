import ast

import pandas as pd

worldcup = "https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/world_cup_women.csv"
matches = "https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/matches_1991_2023.csv"

df_worldcup = pd.read_csv(worldcup)
df_matches = pd.read_csv(matches)


def summary(df):
    summary = pd.DataFrame(
        {
            "Column": df.columns,
            "# Nulls": [df[col].isna().sum() for col in df.columns],
            "Type": [df[col].dtype for col in df.columns],
        }
    )

    print(summary)
    print(f"{df.duplicated().sum()} duplicated rows")


def related_columns(df1, df2):
    common_columns = set(df1.columns) & set(df2.columns)
    validation = []

    for col in common_columns:
        only_in_df1 = set(df1[col].dropna()) - set(df2[col].dropna())
        only_in_df2 = set(df2[col].dropna()) - set(df1[col].dropna())

        validation.append(
            {
                "column": col,
                "df1_nulls": df1[col].isna().sum(),
                "df2_nulls": df2[col].isna().sum(),
                "only_df1": len(only_in_df1),
                "only_df2": len(only_in_df2),
            }
        )

    val_df = pd.DataFrame(validation)

    print(f"Common columns: {common_columns}\n")
    print(val_df)


summary(df_worldcup)
summary(df_matches)

related_columns(df_worldcup, df_matches)

matches_1991 = df_matches[df_matches["Year"] == 1991].copy()

home_teams = matches_1991[
    ["home_team", "home_score", "away_score", "home_yellow_card_long", "home_red_card"]
].copy()
home_teams.columns = [
    "team",
    "goals_for",
    "goals_against",
    "yellow_cards",
    "red_cards",
]

away_teams = matches_1991[
    ["away_team", "away_score", "home_score", "away_yellow_card_long", "away_red_card"]
].copy()
away_teams.columns = [
    "team",
    "goals_for",
    "goals_against",
    "yellow_cards",
    "red_cards",
]

results_1991 = pd.concat([home_teams, away_teams], ignore_index=True)


def count_cards(x):
    if pd.isna(x):
        return 0

    if isinstance(x, list):
        return len(x)

    if isinstance(x, str):
        try:
            parsed = ast.literal_eval(x)
            if isinstance(parsed, list):
                return len(parsed)
            return 1
        except (ValueError, SyntaxError):
            return 1

    return 0


results_1991["yellow_cards"] = results_1991["yellow_cards"].apply(count_cards)
results_1991["red_cards"] = results_1991["red_cards"].apply(count_cards)

results_1991["win"] = (
    results_1991["goals_for"] > results_1991["goals_against"]
).astype(int)
results_1991["draw"] = (
    results_1991["goals_for"] == results_1991["goals_against"]
).astype(int)
results_1991["loss"] = (
    results_1991["goals_for"] < results_1991["goals_against"]
).astype(int)

results_1991["points"] = results_1991["win"] * 3 + results_1991["draw"]
results_1991["fair_play"] = (
    -1 * results_1991["yellow_cards"] - 2 * results_1991["red_cards"]
)

print(results_1991)

results = (
    results_1991.groupby("team")
    .agg(
        PJ=("team", "count"),
        PG=("win", "sum"),
        PE=("draw", "sum"),
        PP=("loss", "sum"),
        GF=("goals_for", "sum"),
        GC=("goals_against", "sum"),
        JL=("fair_play", "sum"),
        Puntos=("points", "sum"),
    )
    .reset_index()
)

results["DG"] = results["GF"] - results["GC"]

results = results.sort_values(by=["Puntos", "DG"], ascending=False)

print(results)
