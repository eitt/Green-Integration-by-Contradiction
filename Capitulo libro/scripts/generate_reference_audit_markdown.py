from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_MATRIX = ROOT / "evidence" / "article_evidence_matrix.csv"
WEB_MATRIX = ROOT / "evidence" / "lengerke_web_matrix.csv"
BIB_FILE = ROOT / "output" / "doc" / "Capitulo libro ESSCA.bib"
NOTES_DIR = ROOT / "notes"


LITERATURE_ORDER = [
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_007",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_032",
    "CLUSTER_D_ROUTE_METHODOLOGY_043",
    "CLUSTER_A_CAMINO_ROUTES_001",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_005",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_009",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_008",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_024",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_023",
    "CLUSTER_A_CAMINO_ROUTES_019",
    "CLUSTER_A_CAMINO_ROUTES_016",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_034",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_030",
    "CLUSTER_A_CAMINO_ROUTES_018",
    "CLUSTER_E_HERITAGE_RURAL_GOVERNANCE_053",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_006",
    "CLUSTER_D_ROUTE_METHODOLOGY_041",
    "CLUSTER_A_CAMINO_ROUTES_003",
    "CLUSTER_A_CAMINO_ROUTES_011",
    "CLUSTER_A_CAMINO_ROUTES_020",
    "CLUSTER_D_ROUTE_METHODOLOGY_048",
]

OFFICIAL_ORDER = ["LGW001", "LGW002", "LGW003"]
REGIONAL_ORDER = ["LGW004", "LGW005"]


ARTICLE_INTERPRETATIONS = {
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_007": "Used as the governance benchmark showing that heritage conservation and tourism development are interdependent and require stakeholder collaboration rather than sectoral isolation.",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_032": "Read as evidence that route competitiveness depends on locally embedded firms, sustainability-oriented business models, and service integration instead of visitor counts alone.",
    "CLUSTER_D_ROUTE_METHODOLOGY_043": "Interpreted as support for treating GIS-based sequencing, congestion handling, and route efficiency as part of route operability and competitiveness.",
    "CLUSTER_A_CAMINO_ROUTES_001": "Used to show that contemporary pilgrimage-route demand is multi-motivational, so Santiago cannot be framed only through religion.",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_005": "Read as a caution that sustainability cannot be assumed rhetorically; it must be demonstrated through evidence and management practice.",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_008": "Used as a supporting technology-and-service-ecosystem source showing that digital disruption changes tourism structures, practices, and value creation conditions.",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_009": "Used to argue that digital visibility, information systems, and service design are part of destination competitiveness, including route-based tourism.",
    "REQUIRED_INCLUDE_056": "Functions as the Colombian methodological bridge, supporting the move from isolated attractions to structured route identification and design.",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_024": "Read as evidence that heritage landscapes can produce place-based economic value, which supports the regional-development framing of the chapter.",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_023": "Used to argue that coordinated protection-utilization systems outperform fragmented interventions and therefore matter for route governance.",
    "CLUSTER_A_CAMINO_ROUTES_019": "Interpreted as support for using digital reconstruction and documentary interfaces when route traces are incomplete, fragmented, or weakly documented.",
    "CLUSTER_A_CAMINO_ROUTES_016": "Used to extend the Santiago benchmark beyond religion toward wellbeing, identity, resilience, and community-seeking dimensions of route experience.",
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_034": "Read as evidence that digital infrastructure can enable tourism entrepreneurship and therefore matters for the Lengerke route's visibility and competitiveness gap.",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_030": "Used to show that sustainability implementation is constrained by resource gaps, policy gaps, and stakeholder-coordination problems.",
    "CLUSTER_A_CAMINO_ROUTES_018": "Interpreted as evidence that route sustainability requires explicit carrying-capacity management and daily-use thresholds rather than unconstrained growth.",
    "CLUSTER_E_HERITAGE_RURAL_GOVERNANCE_053": "Used to foreground residents as core stakeholders, supporting the chapter's argument that local control and empowerment cannot be secondary issues.",
    "CLUSTER_B_SUSTAINABLE_DEVELOPMENT_006": "Read as a conceptual warning against patchy and weak uses of sustainable-tourism language, helping frame the Lengerke case as a documented gap rather than a promotional success story.",
    "CLUSTER_D_ROUTE_METHODOLOGY_041": "Used to show that walkability can be operationalized through route optimization and pedestrian-network design, informing the future empirical agenda.",
    "CLUSTER_A_CAMINO_ROUTES_003": "Interpreted as resilience evidence showing how vulnerable pilgrimage systems are to external shocks and why mature routes are studied through more than demand growth.",
    "CLUSTER_A_CAMINO_ROUTES_011": "Used to support the claim that pilgrimage tourism can connect route activity with employment, income, and livelihood sustainability.",
    "CLUSTER_A_CAMINO_ROUTES_020": "Read as support for corridor-based planning in which nodes, lines, and clusters are managed as an integrated heritage system.",
    "CLUSTER_D_ROUTE_METHODOLOGY_048": "Used to argue that route planning needs explicit multi-indicator evaluation and optimization methods rather than intuitive pathfinding alone.",
}


WEB_REFERENCES = {
    "LGW001": {
        "citation": "Ministerio de Cultura de Colombia. (2015, March 20). Resolución 0688 de 2015.",
        "interpretation": "Treated as the strongest legal anchor for the Barichara-Guane segment because it formally approves the protection framework and defines an obligatory management scope.",
        "where_used": "Introduction; Results and Discussion A-B; Table 1; Table 2; Table 4",
    },
    "LGW002": {
        "citation": "ICOMOS Colombia. (n.d.). Camino Real de Barichara a Guane.",
        "interpretation": "Used as corroborative heritage-registry evidence confirming route identification, route location, and its linkage to Resolution 0688 of 2015.",
        "where_used": "Introduction; Results and Discussion A-B; Table 1; Table 2; Table 4",
    },
    "LGW003": {
        "citation": "DANE. (n.d.). Servicios: Turismo.",
        "interpretation": "Read as evidence that Colombia has an auditable national tourism-statistics architecture, while also showing that route-specific indicators for Camino de Lengerke are still missing.",
        "where_used": "Introduction; Results and Discussion A; Figure 2 discussion; Table 1; Table 2; Table 3; Table 4",
    },
    "LGW004": {
        "citation": "UIS Caminos de Santander. (n.d.). Caminos del comercio - Caminos de Lengerke.",
        "interpretation": "Used to frame the wider documentary network associated with Camino de Lengerke by naming route segments and preserving the broader corridor logic.",
        "where_used": "Introduction; Results and Discussion A; Table 1; Table 2; Figure 2 discussion",
    },
    "LGW005": {
        "citation": "Santander Travel. (n.d.). Los caminos de Geo Von Lengerke.",
        "interpretation": "Used only as contextual corroboration for route sequence and regional narrative, not as standalone proof for legal status or conservation claims.",
        "where_used": "Introduction; Results and Discussion A; Table 1; Table 2; Figure 2 discussion",
    },
}


ARTICLE_USE_OVERRIDES = {
    "CLUSTER_C_COMPETITIVENESS_VALUE_CREATION_008": "Potential support for Results and Discussion (digital/service ecosystem claim)",
}


def read_csv(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return {
            row.get("article_id") or row.get("source_id"): {k: (v or "").strip() for k, v in row.items()}
            for row in reader
        }


def read_bib_dois(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {match.group(1).strip().lower() for match in re.finditer(r"\bdoi\s*=\s*\{([^}]+)\}", text, re.I)}


def md(text: str) -> str:
    clean = " ".join(text.replace("\r", " ").replace("\n", " ").split())
    return clean.replace("|", "\\|")


def lit_table(rows: dict[str, dict[str, str]], bib_dois: set[str]) -> str:
    missing_from_bib = []
    header = [
        "# Reference Audit: Literature Review",
        "",
        "This table lists the scientific articles retained after checking `output/doc/Capitulo libro ESSCA.bib` against the auditable evidence matrix and the chapter's actual claim set.",
        "The `Exact text analyzed` column reproduces the traceable excerpt stored in `evidence/article_evidence_matrix.csv`.",
        "Selection rule for this version: keep only articles that are bibliography-backed, have an auditable excerpt, and fit a concrete chapter claim.",
        "",
        "Excluded from this bib-based table:",
        "- `Altinay et al. (2026)` because the AI-and-women-entrepreneurship focus is too peripheral to the current heritage-route argument.",
        "- `Duarte-Duarte et al. (2021)` because it remains methodologically relevant in the draft but is not currently present in `Capitulo libro ESSCA.bib`.",
        "",
        "| Reference retained for chapter claims | Exact text analyzed | Interpretation in the paper | Justification for inclusion | Main chapter use |",
        "| --- | --- | --- | --- | --- |",
    ]
    body = []
    for article_id in LITERATURE_ORDER:
        row = rows[article_id]
        doi = row["doi"].lower()
        if doi not in bib_dois:
            missing_from_bib.append(article_id)
            continue
        body.append(
            "| {reference} | {exact} | {interpretation} | {justification} | {where_used} |".format(
                reference=md(row["apa_reference"]),
                exact=md(row["exact_phrase"]),
                interpretation=md(ARTICLE_INTERPRETATIONS[article_id]),
                justification=md(row["why_it_matters_for_chapter"]),
                where_used=md(ARTICLE_USE_OVERRIDES.get(article_id, row["target_chapter_section"])),
            )
        )
    if missing_from_bib:
        raise ValueError(f"Expected bibliography-backed article(s) missing from .bib: {', '.join(missing_from_bib)}")
    return "\n".join(header + body) + "\n"


def web_table(rows: dict[str, dict[str, str]], order: list[str], title: str, intro: list[str]) -> str:
    header = [
        f"# {title}",
        "",
        *intro,
        "",
        "| Source used in chapter | Exact text analyzed | Interpretation in the paper | Justification for inclusion | Claim boundary | Main chapter use |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    body = []
    for source_id in order:
        row = rows[source_id]
        meta = WEB_REFERENCES[source_id]
        body.append(
            "| {reference} | {exact} | {interpretation} | {justification} | {claim_boundary} | {where_used} |".format(
                reference=md(meta["citation"]),
                exact=md(row["exact_excerpt"]),
                interpretation=md(meta["interpretation"]),
                justification=md(row["use_in_chapter"]),
                claim_boundary=md(f"{row['claim_status']}; {row['credibility_note']}"),
                where_used=md(meta["where_used"]),
            )
        )
    return "\n".join(header + body) + "\n"


def index_markdown() -> str:
    return "\n".join(
        [
            "# Reference Audit Index",
            "",
            "These markdown files explain how each source actually used in `draft/chapter_draft.md` was analyzed.",
            "",
            "## Files",
            "",
            "- `notes/reference_audit_literature_review.md`: scientific articles filtered against `output/doc/Capitulo libro ESSCA.bib`, with exact phrases, interpretation, and inclusion logic.",
            "- `notes/reference_audit_colombian_official_reports.md`: official Colombian institutional sources used for legal protection, route identification, and tourism-statistics context.",
            "- `notes/reference_audit_colombian_regional_context.md`: Colombian regional or contextual sources used to frame the broader Camino de Lengerke network and narrative.",
            "",
            "## Reading rule",
            "",
            "- `Exact text analyzed` reproduces the traceable excerpt stored in the evidence matrices.",
            "- `Interpretation in the paper` explains how the draft uses that excerpt analytically.",
            "- `Justification for inclusion` states why the source was retained in the argument.",
            "- `Claim boundary` clarifies whether the source supports strong claims, contextual framing, or only limited narrative support.",
            "",
        ]
    )


def main() -> None:
    article_rows = read_csv(ARTICLE_MATRIX)
    web_rows = read_csv(WEB_MATRIX)
    bib_dois = read_bib_dois(BIB_FILE)

    outputs = {
        NOTES_DIR / "reference_audit_index.md": index_markdown(),
        NOTES_DIR / "reference_audit_literature_review.md": lit_table(article_rows, bib_dois),
        NOTES_DIR / "reference_audit_colombian_official_reports.md": web_table(
            web_rows,
            OFFICIAL_ORDER,
            "Reference Audit: Colombian Official Reports",
            [
                "This table isolates the official Colombian sources cited in `draft/chapter_draft.md`.",
                "These sources carry the strongest documentary weight for the local case because they provide legal, registry, or official statistical support.",
            ],
        ),
        NOTES_DIR / "reference_audit_colombian_regional_context.md": web_table(
            web_rows,
            REGIONAL_ORDER,
            "Reference Audit: Colombian Regional and Context Sources",
            [
                "This table covers the non-official Colombian sources cited in `draft/chapter_draft.md`.",
                "They are useful for route framing and regional narrative, but they do not substitute for legal or registry evidence.",
            ],
        ),
    }

    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
