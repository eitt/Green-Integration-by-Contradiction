from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT_DIR = Path(__file__).resolve().parents[1]
ARTICLE_MATRIX = ROOT_DIR / "evidence" / "article_evidence_matrix.csv"
WEB_MATRIX = ROOT_DIR / "evidence" / "lengerke_web_matrix.csv"
OUTPUT_DIR = ROOT_DIR / "figures"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def add_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    lines: list[str],
    facecolor: str = "#f2f2f2",
    edgecolor: str = "#222222",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.015,rounding_size=0.02",
        linewidth=1.4,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(x + 0.015, y + h - 0.045, title, fontsize=11, weight="bold", va="top", ha="left")
    ax.text(x + 0.015, y + h - 0.09, "\n".join(lines), fontsize=9.3, va="top", ha="left")


def add_arrow(ax, start: tuple[float, float], end: tuple[float, float], linestyle: str = "-") -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.2,
        color="#333333",
        linestyle=linestyle,
    )
    ax.add_patch(arrow)


def build_figure_one(article_rows: list[dict[str, str]], web_rows: list[dict[str, str]]) -> Path:
    retained = len(article_rows)
    coded = sum(1 for row in article_rows if (row.get("exact_phrase") or "").strip())
    q1_verified = sum(
        1 for row in article_rows if (row.get("scopus_q1_verified") or "").strip().lower() == "yes"
    )
    official_sources = sum(1 for row in web_rows if (row.get("source_type") or "").strip().lower() == "official")
    contextual_sources = len(web_rows) - official_sources

    theme_counts = Counter((row.get("theme_code") or "").strip() for row in article_rows)
    method_count = theme_counts.get("METH", 0)
    governance_count = theme_counts.get("GOV", 0)
    competitiveness_count = theme_counts.get("COMP", 0) + theme_counts.get("VALUE", 0)
    sustainability_count = theme_counts.get("SUST", 0) + theme_counts.get("RES", 0) + theme_counts.get("PILG", 0)

    fig, ax = plt.subplots(figsize=(10.5, 6.4), dpi=180)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.95,
        "Evidence Architecture for the Camino de Lengerke Documentary Study",
        ha="center",
        va="top",
        fontsize=15,
        weight="bold",
    )
    ax.text(
        0.5,
        0.91,
        "Standalone chapter design built from a curated literature corpus and auditable Colombian sources",
        ha="center",
        va="top",
        fontsize=9.5,
    )

    add_box(
        ax,
        0.05,
        0.61,
        0.24,
        0.21,
        "Peer-reviewed corpus",
        [
            f"{retained} retained papers with local PDFs",
            f"{coded} records coded with exact phrases",
            f"{q1_verified} records with auditable Q1 verification",
            "Coverage: demand, governance, value creation,",
            "digital tourism, GIS routing, heritage corridors",
        ],
        facecolor="#efefef",
    )
    add_box(
        ax,
        0.05,
        0.31,
        0.24,
        0.19,
        "Institutional evidence",
        [
            f"{len(web_rows)} documentary sources for Santander",
            f"{official_sources} official sources and {contextual_sources} contextual sources",
            "Legal anchor: Resolution 0688/2015",
            "Registry anchor: ICOMOS Barichara-Guane",
            "Measurement anchor: DANE tourism portal",
        ],
        facecolor="#f7f7f7",
    )
    add_box(
        ax,
        0.38,
        0.46,
        0.25,
        0.24,
        "Analytical synthesis",
        [
            f"Governance and heritage coordination ({governance_count})",
            f"Route design and walkability methods ({method_count})",
            f"Competitiveness and local value creation ({competitiveness_count})",
            f"Demand, sustainability, and resilience ({sustainability_count})",
            "Claim rule: only audited, documentable assertions enter the text",
        ],
        facecolor="#ffffff",
    )
    add_box(
        ax,
        0.72,
        0.55,
        0.22,
        0.22,
        "Chapter outputs",
        [
            "Delimitation of the strongest audited route segment",
            "Territorial logic of the broader Camino de Lengerke system",
            "Propositions on governance, walkability, and local value",
        ],
        facecolor="#efefef",
    )
    add_box(
        ax,
        0.72,
        0.25,
        0.22,
        0.18,
        "Research agenda",
        [
            "Route-level indicators for preservation and access",
            "Stakeholder mapping and service-ecosystem interviews",
            "Field validation of distributed economic effects",
        ],
        facecolor="#f7f7f7",
    )

    add_arrow(ax, (0.29, 0.715), (0.38, 0.60))
    add_arrow(ax, (0.29, 0.405), (0.38, 0.54))
    add_arrow(ax, (0.63, 0.58), (0.72, 0.66))
    add_arrow(ax, (0.63, 0.50), (0.72, 0.34))

    ax.text(
        0.5,
        0.11,
        "The figure emphasizes that the chapter is not framed as a thesis adaptation: the central unit of analysis is the\nCamino de Lengerke as a documented heritage-route system in Santander.",
        ha="center",
        va="center",
        fontsize=8.8,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "figure_1_evidence_architecture.png"
    fig.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


def build_figure_two() -> Path:
    fig, ax = plt.subplots(figsize=(10.5, 6.6), dpi=180)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.95,
        "Documentary Schematic of the Camino de Lengerke System",
        ha="center",
        va="top",
        fontsize=15,
        weight="bold",
    )
    ax.text(
        0.5,
        0.91,
        "This is a documentary route system, not a georeferenced map",
        ha="center",
        va="top",
        fontsize=9.5,
    )

    main_nodes = [
        ("Los Santos", 0.13),
        ("Jordan", 0.27),
        ("Barichara", 0.41),
        ("Guane", 0.55),
        ("Zapatoca", 0.69),
        ("Puenteruedas", 0.83),
    ]

    for index, (label, x_pos) in enumerate(main_nodes):
        y_pos = 0.52
        face = "#e8e8e8" if label in {"Barichara", "Guane"} else "#f7f7f7"
        rect = FancyBboxPatch(
            (x_pos - 0.055, y_pos - 0.04),
            0.11,
            0.08,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            linewidth=1.3,
            edgecolor="#222222",
            facecolor=face,
        )
        ax.add_patch(rect)
        ax.text(x_pos, y_pos, label, ha="center", va="center", fontsize=9.4, weight="bold")
        if index < len(main_nodes) - 1:
            add_arrow(ax, (x_pos + 0.055, y_pos), (main_nodes[index + 1][1] - 0.055, y_pos))

    add_box(
        ax,
        0.35,
        0.63,
        0.26,
        0.13,
        "Strongest audited segment",
        [
            "Barichara-Guane",
            "Protected by Resolution 0688/2015",
            "Registered by ICOMOS Colombia",
        ],
        facecolor="#dcdcdc",
    )
    add_arrow(ax, (0.48, 0.63), (0.48, 0.57))

    add_box(
        ax,
        0.05,
        0.73,
        0.18,
        0.11,
        "UIS route evidence",
        [
            "Cabrera-Barichara",
            "Los Santos-Jordan",
            "San Vicente-Zapatoca",
            "Zapatoca-Puenteruedas",
        ],
        facecolor="#f4f4f4",
    )
    add_arrow(ax, (0.23, 0.74), (0.36, 0.57), linestyle="--")
    add_arrow(ax, (0.23, 0.73), (0.69, 0.57), linestyle="--")

    add_box(
        ax,
        0.75,
        0.72,
        0.18,
        0.12,
        "Santander Travel sequence",
        [
            "Los Santos",
            "Jordan",
            "Barichara",
            "Guane",
            "Zapatoca",
        ],
        facecolor="#f4f4f4",
    )
    add_arrow(ax, (0.75, 0.73), (0.20, 0.57), linestyle="--")

    add_box(
        ax,
        0.06,
        0.20,
        0.20,
        0.11,
        "Context node",
        [
            "Cabrera",
            "Appears in UIS documentary network",
        ],
        facecolor="#fafafa",
    )
    add_arrow(ax, (0.26, 0.25), (0.38, 0.48), linestyle="--")

    add_box(
        ax,
        0.74,
        0.20,
        0.20,
        0.11,
        "Context node",
        [
            "San Vicente de Chucuri",
            "Appears in UIS documentary network",
        ],
        facecolor="#fafafa",
    )
    add_arrow(ax, (0.74, 0.25), (0.70, 0.48), linestyle="--")

    measurement = Rectangle((0.34, 0.10), 0.32, 0.09, linewidth=1.3, edgecolor="#222222", facecolor="#efefef")
    ax.add_patch(measurement)
    ax.text(
        0.50,
        0.145,
        "DANE tourism statistics portal:\nmeasurement architecture for later route-level indicators",
        ha="center",
        va="center",
        fontsize=9.1,
        weight="bold",
    )
    add_arrow(ax, (0.50, 0.19), (0.50, 0.46))

    ax.text(
        0.5,
        0.04,
        "Interpretive rule: only Barichara-Guane currently supports strong legal and heritage claims; the broader system is\nanalytically relevant but must be discussed with differentiated evidential strength.",
        ha="center",
        va="bottom",
        fontsize=8.7,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "figure_2_camino_documentary_system.png"
    fig.savefig(output_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return output_path


def main() -> int:
    article_rows = load_rows(ARTICLE_MATRIX)
    web_rows = load_rows(WEB_MATRIX)

    figure_one = build_figure_one(article_rows, web_rows)
    figure_two = build_figure_two()

    print(f"Generated {figure_one}")
    print(f"Generated {figure_two}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
