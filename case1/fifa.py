# import matplotlib.pyplot as plt
import pandas as pd
from services.analysis import AnalysisService
from services.results import ResultsService

url_wc = "https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/world_cup_women.csv"
url_matches = "https://raw.githubusercontent.com/daramireh/simonBolivarCienciaDatos/refs/heads/main/matches_1991_2023.csv"

world_cup = pd.read_csv(url_wc)
matches = pd.read_csv(url_matches)

analysis_wc = AnalysisService(world_cup)
analysis_matches = AnalysisService(matches)

analysis_wc.summary()
analysis_matches.summary()

AnalysisService.related_columns(world_cup, matches)

matches_1991 = matches[matches["Year"] == 1991].copy()

results = ResultsService(matches_1991)
table_1991 = results.get_results()
print(table_1991)

matches_2023 = matches[matches["Year"] == 2023].copy()

results = ResultsService(matches_2023)
top_scorers_2023 = results.top_scorers()
print(top_scorers_2023)

results = ResultsService(matches)
summary = results.world_cup_summary()
print(summary)

# 1. ¿Cómo ha cambiado el promedio de goles por partido a lo largo de los torneos?
goals_trend = (
    summary.groupby("Year").agg({"GF Avg": "mean", "GA Avg": "mean"}).reset_index()
)

goals_trend["Total Goals Avg"] = goals_trend["GF Avg"] + goals_trend["GA Avg"]
print("\nAverage Goals Trend:")
print(goals_trend)

# plt.figure(figsize=(12, 6))
# plt.plot(goals_trend["Year"], goals_trend["Total Goals Avg"], marker="o", linewidth=2)
# plt.title("Average Goals Trend")
# plt.xlabel("Year")
# plt.ylabel("Average Goals")
# plt.grid(True, alpha=0.3)
# plt.show()

# 2. ¿Cuáles son las selecciones con mejor desempeño en términos de victorias?
best_teams = (
    summary.groupby("Team")
    .agg({"W": "sum", "GP": "sum", "GF": "sum", "GA": "sum"})
    .reset_index()
)

best_teams["Win Rate"] = (best_teams["W"] / best_teams["GP"] * 100).round(2)
best_teams["GD"] = best_teams["GF"] - best_teams["GA"]

best_teams = best_teams.sort_values("W", ascending=False, ignore_index=True)
print("\nTop 10 teams:")
print(best_teams[["Team", "GP", "W", "Win Rate", "GD"]].head(10))

# 3. ¿Existen tendencias en los equipos dominantes y con peor desempeño?
dominant_teams = best_teams[best_teams["GP"] >= 10].sort_values(
    "Win Rate", ascending=False
)
print("\nMost dominant teams (min 10 games):")
print(dominant_teams[["Team", "GP", "W", "Win Rate", "GD"]].head(10))

worst_teams = best_teams[best_teams["GP"] >= 10].sort_values("Win Rate", ascending=True)
print("\nWorst performing teams (min 10 games):")
print(worst_teams[["Team", "GP", "W", "Win Rate", "GD"]].head(10))

team_evolution = (
    summary.groupby(["Team", "Year"]).agg({"W": "sum", "GP": "sum"}).reset_index()
)

team_evolution["Win Rate"] = (team_evolution["W"] / team_evolution["GP"] * 100).round(2)

consistency = (
    team_evolution.groupby("Team")
    .agg({"Win Rate": ["mean", "std", "count"]})
    .reset_index()
)
consistency.columns = ["Team", "Avg Win Rate", "Std Win Rate", "Tournaments"]
consistency = consistency[consistency["Tournaments"] >= 3].sort_values(
    "Std Win Rate", ignore_index=True
)

print("\nMost consistent teams (min 3 tournaments):")
print(consistency.head(10))

print("\nMost inconsistent teams (min 3 tournaments):")
print(consistency.tail(10))
