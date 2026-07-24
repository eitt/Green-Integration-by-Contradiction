from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed" / "ejatlas_lng_database.csv"
FIG_DIR = ROOT / "figures"


def clean_series(series, top_n=None):
    counts = series.fillna("").replace("", "Unknown").value_counts()
    if top_n is not None:
        counts = counts.head(top_n)
    return counts


def save_barh(series, title, filename, color="#1f5a91", xlabel="Cases"):
    plt.figure(figsize=(10, 6))
    ax = series.sort_values().plot(kind="barh", color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=220)
    plt.close()


def save_stacked_core(df):
    order = [
        "Europe",
        "US East Coast (provisional)",
        "Russia",
        "Algeria",
        "UAE (Abu Dhabi)",
    ]
    subset = df[df["core_article_flag"] == "yes"].copy()
    table = (
        subset.groupby(["core_article_group", "status_standardized"])
        .size()
        .unstack(fill_value=0)
        .reindex(order)
        .fillna(0)
    )
    plt.figure(figsize=(10, 6))
    table.plot(
        kind="bar",
        stacked=True,
        color=["#8fb8de", "#f0a202", "#d95d39", "#5f9e6e", "#7d5ba6"],
    )
    plt.title("Core 26 Cases by Group and Standardized Status")
    plt.xlabel("")
    plt.ylabel("Cases")
    plt.xticks(rotation=20, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "core_cases_by_group_and_status.png", dpi=220)
    plt.close()


def save_core_relevance(df):
    subset = df[df["core_article_flag"] == "yes"]["link_to_eu"].value_counts()
    plt.figure(figsize=(8, 8))
    colors = ["#1f5a91", "#4c956c", "#f0a202"]
    subset.plot(kind="pie", autopct="%1.0f%%", startangle=90, colors=colors[: len(subset)])
    plt.ylabel("")
    plt.title("EU Linkage in the Core Comparative Sample")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "core_eu_linkage_pie.png", dpi=220)
    plt.close()


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    save_barh(clean_series(df["country"], top_n=15), "Top Countries in Live EJAtlas LNG Pull", "cases_by_country.png")
    save_barh(clean_series(df["infrastructure_type"]), "Infrastructure Types Across LNG Cases", "infrastructure_types.png", color="#d95d39")
    save_barh(clean_series(df["supply_chain_role"]), "Supply-Chain Roles Across LNG Cases", "supply_chain_roles.png", color="#5f9e6e")
    save_barh(clean_series(df["us_coast_bucket"][df["country"] == "United States"]), "US LNG-Related Cases by Coast Bucket", "us_coast_buckets.png", color="#7d5ba6")
    save_stacked_core(df)
    save_core_relevance(df)


if __name__ == "__main__":
    main()
