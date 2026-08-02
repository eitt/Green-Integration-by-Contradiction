from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "figures" / "EU-Mercosur_Negotiation_Timeline_polished_web.svg"
OUTPUT = ROOT / "figures" / "EU-Mercosur_Negotiation_Timeline_polished.svg"
ILLUSTRATOR_COPY = (
    ROOT / "figures" / "EU-Mercosur_Negotiation_Timeline_Illustrator.svg"
)

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
NS = {"svg": SVG}
ET.register_namespace("", SVG)


STYLES = {
    "bg": {"fill": "#FFFFFF"},
    "title": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "40px",
        "font-weight": "700",
        "fill": "#111111",
    },
    "subtitle": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "24px",
        "font-weight": "400",
        "fill": "#444444",
    },
    "section-label": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "18px",
        "font-weight": "700",
        "letter-spacing": "1.8px",
        "fill": "#444444",
    },
    "year": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "25px",
        "font-weight": "700",
        "fill": "#FFFFFF",
    },
    "card-title": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "23px",
        "font-weight": "700",
        "fill": "#111111",
    },
    "body": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "18px",
        "font-weight": "400",
        "fill": "#292929",
    },
    "body-small": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "16px",
        "font-weight": "400",
        "fill": "#292929",
    },
    "analysis-title": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "24px",
        "font-weight": "700",
        "fill": "#111111",
    },
    "analysis-body": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "18px",
        "font-weight": "400",
        "fill": "#292929",
    },
    "thesis": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "22px",
        "font-weight": "600",
        "fill": "#FFFFFF",
    },
    "legend": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "16px",
        "font-weight": "400",
        "fill": "#333333",
    },
    "source": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "14px",
        "font-weight": "400",
        "fill": "#444444",
    },
    "source-link": {
        "font-family": "Arial, Helvetica, sans-serif",
        "font-size": "14px",
        "font-weight": "400",
        "fill": "#111111",
        "text-decoration": "underline",
    },
    "card": {"fill": "#FFFFFF", "stroke": "#B8B8B8", "stroke-width": "1.5"},
    "trade": {"fill": "url(#trade-hatch)"},
    "regulation": {"fill": "url(#regulation-dots)"},
    "tension": {"fill": "url(#tension-grid)"},
    "connector": {"stroke": "#777777", "stroke-width": "3", "fill": "none"},
    "timeline": {
        "stroke": "#1A1A1A",
        "stroke-width": "9",
        "stroke-linecap": "round",
        "fill": "none",
    },
}


def strip_unsupported(root):
    root.set("version", "1.1")
    root.set("baseProfile", "full")
    for attribute in list(root.attrib):
        if attribute.startswith("aria-") or attribute == "role":
            del root.attrib[attribute]

    for element in root.iter():
        for attribute in list(element.attrib):
            if (
                attribute.startswith("aria-")
                or attribute == "role"
                or attribute == "target"
                or attribute == "filter"
                or attribute == f"{{{XLINK}}}href"
            ):
                del element.attrib[attribute]

        class_name = element.attrib.pop("class", None)
        if class_name:
            for name in class_name.split():
                for key, value in STYLES.get(name, {}).items():
                    element.set(key, value)

    defs = root.find("svg:defs", NS)
    if defs is not None:
        for child in list(defs):
            if child.tag in {f"{{{SVG}}}filter", f"{{{SVG}}}style", f"{{{SVG}}}marker"}:
                defs.remove(child)


def flatten_links(root):
    for parent in root.iter():
        children = list(parent)
        for index, child in enumerate(children):
            if child.tag != f"{{{SVG}}}a":
                continue
            insertion_index = list(parent).index(child)
            if child.text and child.text.strip():
                text_node = ET.Element(f"{{{SVG}}}tspan")
                text_node.text = child.text
                parent.insert(insertion_index, text_node)
                insertion_index += 1
            for grandchild in list(child):
                parent.insert(insertion_index, deepcopy(grandchild))
                insertion_index += 1
            parent.remove(child)


def replace_arrow_marker(root):
    timeline = None
    for element in root.iter(f"{{{SVG}}}line"):
        if element.get("marker-end"):
            timeline = element
            break
    if timeline is None:
        return
    timeline.attrib.pop("marker-end", None)
    timeline.set("x2", "1722")
    parent = next(parent for parent in root.iter() if timeline in list(parent))
    index = list(parent).index(timeline)
    arrow = ET.Element(
        f"{{{SVG}}}polygon",
        {
            "points": "1718,424 1785,460 1718,496",
            "fill": "#1A1A1A",
            "stroke": "none",
        },
    )
    parent.insert(index + 1, arrow)


def main():
    tree = ET.parse(SOURCE)
    root = tree.getroot()
    strip_unsupported(root)
    flatten_links(root)
    replace_arrow_marker(root)

    ET.indent(tree, space="  ")
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    ILLUSTRATOR_COPY.write_bytes(OUTPUT.read_bytes())

    check = ET.parse(OUTPUT).getroot()
    forbidden = {"style", "filter", "marker", "a"}
    found = {
        element.tag.rsplit("}", 1)[-1]
        for element in check.iter()
        if element.tag.rsplit("}", 1)[-1] in forbidden
    }
    if found:
        raise RuntimeError(f"Unsupported elements remain: {sorted(found)}")
    print(OUTPUT)
    print(ILLUSTRATOR_COPY)


if __name__ == "__main__":
    main()
