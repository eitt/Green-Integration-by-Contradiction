from pathlib import Path
from itertools import combinations
import math

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from shapely.geometry import LineString


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed" / "ejatlas_lng_database.csv"
PROCESSED = ROOT / "data" / "processed"
FIG_DIR = ROOT / "figures"


def split_values(value):
    if pd.isna(value) or str(value).strip() == "":
        return set()
    return {item.strip() for item in str(value).split(";") if item.strip()}


def relation_score(row_a, row_b):
    score = 0
    reasons = []

    if row_a["core_article_group"] == row_b["core_article_group"] and row_a["core_article_group"]:
        score += 3
        reasons.append(f"same_core_group:{row_a['core_article_group']}")

    if row_a["supply_chain_role"] == row_b["supply_chain_role"] and row_a["supply_chain_role"]:
        score += 2
        reasons.append(f"same_supply_role:{row_a['supply_chain_role']}")

    if row_a["infrastructure_type"] == row_b["infrastructure_type"] and row_a["infrastructure_type"]:
        score += 2
        reasons.append(f"same_infrastructure:{row_a['infrastructure_type']}")

    if row_a["status_standardized"] == row_b["status_standardized"] and row_a["status_standardized"]:
        score += 1
        reasons.append(f"same_status:{row_a['status_standardized']}")

    if row_a["link_to_eu"] == row_b["link_to_eu"] and row_a["link_to_eu"]:
        score += 1
        reasons.append("same_eu_link")

    impact_overlap = split_values(row_a["main_impacts"]) & split_values(row_b["main_impacts"])
    if impact_overlap:
        impact_score = min(len(impact_overlap), 3)
        score += impact_score
        reasons.append("shared_impacts:" + "|".join(sorted(list(impact_overlap))[:3]))

    group_overlap = split_values(row_a["affected_groups"]) & split_values(row_b["affected_groups"])
    if group_overlap:
        group_score = min(len(group_overlap), 2)
        score += group_score
        reasons.append("shared_groups:" + "|".join(sorted(list(group_overlap))[:3]))

    actor_overlap = split_values(row_a["companies"]) & split_values(row_b["companies"])
    if actor_overlap:
        actor_score = min(len(actor_overlap), 2)
        score += actor_score
        reasons.append("shared_companies:" + "|".join(sorted(list(actor_overlap))[:3]))

    return score, reasons


def short_label(row):
    name = row["case_name"]
    if len(name) > 32:
        name = name[:29] + "..."
    country = row["country"]
    return f"{name}\n({country})"


def build_edge_table(df):
    core = df[df["core_article_flag"] == "yes"].copy()
    core = core[core["longitude"].notna() & core["latitude"].notna()].copy()
    edges = []
    for (_, row_a), (_, row_b) in combinations(core.iterrows(), 2):
        weight, reasons = relation_score(row_a, row_b)
        if weight >= 4:
            edges.append(
                {
                    "source_id": row_a["ejatlas_id"],
                    "target_id": row_b["ejatlas_id"],
                    "source_case": row_a["case_name"],
                    "target_case": row_b["case_name"],
                    "source_country": row_a["country"],
                    "target_country": row_b["country"],
                    "weight": weight,
                    "relation_reasons": "; ".join(reasons),
                    "source_longitude": row_a["longitude"],
                    "source_latitude": row_a["latitude"],
                    "target_longitude": row_b["longitude"],
                    "target_latitude": row_b["latitude"],
                }
            )
    edge_df = pd.DataFrame(edges).sort_values(["weight", "source_case", "target_case"], ascending=[False, True, True])
    return core, edge_df


def draw_network(core_df, edge_df):
    graph = nx.Graph()
    for _, row in core_df.iterrows():
        graph.add_node(
            row["ejatlas_id"],
            label=short_label(row),
            group=row["core_article_group"],
            country=row["country"],
        )

    for _, edge in edge_df.iterrows():
        graph.add_edge(edge["source_id"], edge["target_id"], weight=edge["weight"])

    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(graph, seed=42, weight="weight", k=1.1 / math.sqrt(max(len(graph.nodes), 1)))
    group_colors = {
        "Europe": "#1f5a91",
        "US East Coast (provisional)": "#d95d39",
        "Russia": "#7d5ba6",
        "Algeria": "#4c956c",
        "UAE (Abu Dhabi)": "#f0a202",
    }
    node_colors = [group_colors.get(graph.nodes[n]["group"], "#999999") for n in graph.nodes]
    edge_widths = [0.6 + graph[u][v]["weight"] * 0.45 for u, v in graph.edges]
    node_sizes = [450 + (graph.degree(n) * 60) for n in graph.nodes]

    nx.draw_networkx_edges(graph, pos, width=edge_widths, edge_color="#7f8c8d", alpha=0.45)
    nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color=node_colors, alpha=0.92, linewidths=0.8, edgecolors="white")
    nx.draw_networkx_labels(graph, pos, labels={n: graph.nodes[n]["label"] for n in graph.nodes}, font_size=8)

    plt.title("Relational Network of Core LNG Cases\nEdge weight = shared coded relations across cases")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "core_case_relation_network.png", dpi=240)
    plt.close()


def draw_world_map(core_df, edge_df):
    points = gpd.GeoDataFrame(
        core_df.copy(),
        geometry=gpd.points_from_xy(core_df["longitude"], core_df["latitude"]),
        crs="EPSG:4326",
    )
    line_rows = []
    for _, edge in edge_df.iterrows():
        line_rows.append(
            {
                "weight": edge["weight"],
                "relation_reasons": edge["relation_reasons"],
                "geometry": LineString(
                    [
                        (edge["source_longitude"], edge["source_latitude"]),
                        (edge["target_longitude"], edge["target_latitude"]),
                    ]
                ),
            }
        )
    lines = gpd.GeoDataFrame(line_rows, geometry="geometry", crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_facecolor("#eef6fb")
    ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.35, color="#8aa4b8")
    if not lines.empty:
        for weight in sorted(lines["weight"].unique()):
            subset = lines[lines["weight"] == weight]
            subset.plot(ax=ax, linewidth=0.3 + weight * 0.25, alpha=0.35, color="#3f6c8f")

    group_colors = {
        "Europe": "#1f5a91",
        "US East Coast (provisional)": "#d95d39",
        "Russia": "#7d5ba6",
        "Algeria": "#4c956c",
        "UAE (Abu Dhabi)": "#f0a202",
    }
    for group, subset in points.groupby("core_article_group"):
        subset.plot(ax=ax, markersize=65, color=group_colors.get(group, "#999999"), label=group, edgecolor="white", linewidth=0.6)

    label_subset = points.copy()
    for _, row in label_subset.iterrows():
        ax.text(row.geometry.x + 1.5, row.geometry.y + 0.8, row["country"], fontsize=7, color="#333333")

    ax.set_title("World Map of Relational Links Across Core LNG Cases\nArc width scales with shared coded relations")
    ax.set_xlim([-170, 170])
    ax.set_ylim([-60, 85])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(loc="lower left", frameon=True, fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "core_case_relation_world_map.png", dpi=240)
    plt.close()


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    core_df, edge_df = build_edge_table(df)
    edge_df.to_csv(PROCESSED / "core_case_relation_edges.csv", index=False)
    draw_network(core_df, edge_df)
    draw_world_map(core_df, edge_df)


if __name__ == "__main__":
    main()
