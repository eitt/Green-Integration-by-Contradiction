from pathlib import Path
import json
import math

import networkx as nx
import pandas as pd
from plotly.offline.offline import get_plotlyjs

from generate_relational_figures import build_edge_table


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed" / "ejatlas_lng_database.csv"
FIG_DIR = ROOT / "figures"


GROUP_COLORS = {
    "Europe": "#1f5a91",
    "US East Coast (provisional)": "#d95d39",
    "Russia": "#7d5ba6",
    "Algeria": "#4c956c",
    "UAE (Abu Dhabi)": "#f0a202",
}


def build_graph_payload():
    df = pd.read_csv(DATA)
    core_df, edge_df = build_edge_table(df)

    graph = nx.Graph()
    for _, row in core_df.iterrows():
        graph.add_node(
            int(row["ejatlas_id"]),
            case_name=row["case_name"],
            country=row["country"],
            core_group=row["core_article_group"],
            relevance_to_core_argument=row["relevance_to_core_argument"],
            conflict_category=row["conflict_category"],
            infrastructure_type=row["infrastructure_type"],
            supply_chain_role=row["supply_chain_role"],
            link_to_eu=row["link_to_eu"],
            main_impacts=row["main_impacts"],
            affected_groups=row["affected_groups"],
            main_actors=row["main_actors"],
            status=row["status_standardized"],
            evidence_quality=row["evidence_quality"],
            article_use=row["article_use_recommendation"],
            province=row["province"],
            location=row["location"],
            raw_link=row["raw_link"],
            notes=row["notes"],
        )

    for _, row in edge_df.iterrows():
        graph.add_edge(
            int(row["source_id"]),
            int(row["target_id"]),
            weight=int(row["weight"]),
            reasons=row["relation_reasons"],
            source_case=row["source_case"],
            target_case=row["target_case"],
        )

    positions = nx.spring_layout(graph, seed=42, weight="weight", k=1.1 / math.sqrt(max(len(graph.nodes), 1)))

    nodes = []
    for node_id, attrs in graph.nodes(data=True):
        x, y = positions[node_id]
        degree = graph.degree(node_id)
        nodes.append(
            {
                "id": node_id,
                "x": float(x),
                "y": float(y),
                "size": 16 + degree * 2.4,
                "degree": int(degree),
                "color": GROUP_COLORS.get(attrs["core_group"], "#999999"),
                **attrs,
            }
        )

    edges = []
    for source, target, attrs in graph.edges(data=True):
        edges.append(
            {
                "source": int(source),
                "target": int(target),
                "weight": int(attrs["weight"]),
                "reasons": attrs["reasons"],
                "source_case": attrs["source_case"],
                "target_case": attrs["target_case"],
            }
        )

    return {
        "nodes": nodes,
        "edges": edges,
        "groups": sorted({node["core_group"] for node in nodes}),
        "countries": sorted({node["country"] for node in nodes}),
        "maxWeight": max(edge["weight"] for edge in edges) if edges else 1,
    }


def build_html(payload):
    plotly_js = get_plotlyjs()
    data_json = json.dumps(payload, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Interactive Core LNG Case Relation Network</title>
  <style>
    :root {{
      --bg: #f6f2e8;
      --panel: #fffdf8;
      --ink: #1f2933;
      --muted: #5d6a75;
      --line: #d9d1c0;
      --accent: #1f5a91;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(31,90,145,0.10), transparent 28%),
        radial-gradient(circle at bottom right, rgba(217,93,57,0.08), transparent 24%),
        var(--bg);
    }}
    .wrap {{
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr) 360px;
      min-height: 100vh;
      gap: 0;
    }}
    .panel {{
      background: rgba(255,253,248,0.96);
      border-right: 1px solid var(--line);
      padding: 22px 18px;
      overflow: auto;
    }}
    .panel.right {{
      border-right: 0;
      border-left: 1px solid var(--line);
    }}
    h1 {{
      font-size: 1.25rem;
      margin: 0 0 8px 0;
      line-height: 1.25;
    }}
    h2 {{
      font-size: 0.92rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin: 22px 0 8px 0;
    }}
    p, li {{
      font-size: 0.92rem;
      line-height: 1.45;
    }}
    .control {{
      margin-bottom: 14px;
    }}
    label {{
      display: block;
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    select, input {{
      width: 100%;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fff;
      color: var(--ink);
      font-size: 0.92rem;
    }}
    .range-row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: center;
    }}
    .metric-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-top: 16px;
    }}
    .metric {{
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px;
    }}
    .metric .k {{
      font-size: 0.72rem;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .metric .v {{
      font-size: 1.2rem;
      margin-top: 4px;
      font-weight: 700;
    }}
    .chart-area {{
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      min-width: 0;
    }}
    .chart-head {{
      padding: 18px 22px 0 22px;
    }}
    .chart-head p {{
      color: var(--muted);
      max-width: 78ch;
      margin-top: 6px;
    }}
    #graph {{
      width: 100%;
      height: calc(100vh - 110px);
    }}
    .detail-block {{
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
    }}
    .detail-title {{
      font-size: 1rem;
      margin: 0 0 6px 0;
    }}
    .pill {{
      display: inline-block;
      border-radius: 999px;
      background: #eef3f7;
      color: var(--accent);
      padding: 4px 10px;
      font-size: 0.75rem;
      margin: 4px 6px 0 0;
    }}
    .small {{
      color: var(--muted);
      font-size: 0.82rem;
    }}
    a {{
      color: var(--accent);
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <aside class="panel">
      <h1>Interactive Core LNG Relation Network</h1>
      <p>This standalone graph lets you filter the comparative core sample and inspect how cases are linked by shared coded traits.</p>

      <h2>Filters</h2>
      <div class="control">
        <label for="groupFilter">Core group</label>
        <select id="groupFilter"></select>
      </div>
      <div class="control">
        <label for="countryFilter">Country</label>
        <select id="countryFilter"></select>
      </div>
      <div class="control">
        <label for="searchFilter">Search case</label>
        <input id="searchFilter" type="text" placeholder="Type part of a case name">
      </div>
      <div class="control">
        <label for="weightFilter">Minimum edge weight</label>
        <div class="range-row">
          <input id="weightFilter" type="range" min="4" max="{payload['maxWeight']}" value="4" step="1">
          <strong id="weightValue">4</strong>
        </div>
      </div>

      <div class="metric-grid">
        <div class="metric"><div class="k">Visible nodes</div><div id="visibleNodes" class="v">0</div></div>
        <div class="metric"><div class="k">Visible edges</div><div id="visibleEdges" class="v">0</div></div>
        <div class="metric"><div class="k">Max weight</div><div id="maxWeight" class="v">{payload['maxWeight']}</div></div>
        <div class="metric"><div class="k">Core cases</div><div class="v">{len(payload['nodes'])}</div></div>
      </div>

      <h2>What Nodes And Arcs Mean</h2>
      <p><strong>Nodes</strong> represent individual LNG-related environmental conflict cases from EJAtlas.</p>
      <p><strong>Node color</strong> identifies the comparative group of the case.</p>
      <p><strong>Node size</strong> shows how many visible ties the case has under the current filters.</p>
      <p><strong>Arcs</strong> represent coded relationships between two cases.</p>
      <p><strong>Arc thickness</strong> reflects relation weight: thicker arcs mean more shared coded attributes.</p>
      <p class="small">Weights combine shared group, supply-chain role, infrastructure type, status, EU linkage, impacts, affected groups, and overlapping firms.</p>
    </aside>

    <main class="chart-area">
      <div class="chart-head">
        <h1>Core LNG Cases</h1>
        <p>Click a node to inspect the coded case profile. Click an edge to inspect the relation logic behind that pair. Double-click the canvas to reset the camera.</p>
      </div>
      <div id="graph"></div>
    </main>

    <aside class="panel right">
      <h1>Case / Link Detail</h1>
      <div id="detailPanel">
        <div class="detail-block">
          <p>Select a node or an edge in the graph to inspect its metadata and coded relations.</p>
        </div>
        <div class="detail-block">
          <p><strong>Node click:</strong> shows the main empirical fields for a case, following the coding table used in the article.</p>
          <p><strong>Arc click:</strong> shows why the two cases are connected and how the arc weight was built.</p>
        </div>
      </div>
    </aside>
  </div>

  <script>{plotly_js}</script>
  <script>
    const graphData = {data_json};
    const graphDiv = document.getElementById('graph');
    const detailPanel = document.getElementById('detailPanel');
    const groupFilter = document.getElementById('groupFilter');
    const countryFilter = document.getElementById('countryFilter');
    const searchFilter = document.getElementById('searchFilter');
    const weightFilter = document.getElementById('weightFilter');
    const weightValue = document.getElementById('weightValue');
    const visibleNodesEl = document.getElementById('visibleNodes');
    const visibleEdgesEl = document.getElementById('visibleEdges');

    function fillSelect(selectEl, values, labelAll) {{
      selectEl.innerHTML = '';
      const optAll = document.createElement('option');
      optAll.value = 'All';
      optAll.textContent = labelAll;
      selectEl.appendChild(optAll);
      values.forEach(value => {{
        const opt = document.createElement('option');
        opt.value = value;
        opt.textContent = value;
        selectEl.appendChild(opt);
      }});
    }}

    fillSelect(groupFilter, graphData.groups, 'All core groups');
    fillSelect(countryFilter, graphData.countries, 'All countries');

    function nl2br(text) {{
      return String(text || '').replace(/\\n/g, '<br>');
    }}

    function defaultDetailHtml(visibleNodes, visibleEdges) {{
      const countries = [...new Set(visibleNodes.map(node => node.country))];
      const groups = [...new Set(visibleNodes.map(node => node.core_group))];
      return `
        <div class="detail-block">
          <p><strong>Filtered selection</strong></p>
          <p>${{visibleNodes.length}} visible case(s) and ${{visibleEdges.length}} visible relation(s).</p>
        </div>
        <div class="detail-block">
          <p><strong>Countries in view:</strong> ${{countries.length ? countries.join('; ') : 'None'}}</p>
          <p><strong>Core groups in view:</strong> ${{groups.length ? groups.join('; ') : 'None'}}</p>
        </div>
        <div class="detail-block">
          <p>Click a node to inspect one case in detail. Click an arc to inspect the coded relation between two cases.</p>
        </div>
      `;
    }}

    function caseHtml(node) {{
      return `
        <div class="detail-block">
          <h3 class="detail-title">${{node.case_name}}</h3>
          <div class="pill">${{node.core_group}}</div>
          <div class="pill">${{node.country}}</div>
        </div>
        <div class="detail-block">
          <p><strong>Case name:</strong> ${{node.case_name}}</p>
          <p><strong>Country:</strong> ${{node.country}}</p>
          <p><strong>Region/city:</strong> ${{node.province}} | ${{node.location}}</p>
          <p><strong>Infrastructure type:</strong> ${{node.infrastructure_type}}</p>
          <p><strong>Supply-chain role:</strong> ${{node.supply_chain_role}}</p>
          <p><strong>Link to EU:</strong> ${{node.link_to_eu}}</p>
        </div>
        <div class="detail-block">
          <p><strong>Main impacts:</strong> ${{node.main_impacts}}</p>
          <p><strong>Conflict category:</strong> ${{node.conflict_category}}</p>
          <p><strong>Affected groups:</strong> ${{node.affected_groups}}</p>
          <p><strong>Main actors:</strong> ${{node.main_actors}}</p>
          <p><strong>Status:</strong> ${{node.status}}</p>
          <p><strong>Evidence quality:</strong> ${{node.evidence_quality}}</p>
        </div>
        <div class="detail-block">
          <p><strong>Relevance to core argument:</strong> ${{node.relevance_to_core_argument}}</p>
          <p><strong>Article use recommendation:</strong> ${{node.article_use}}</p>
          <p><strong>Notes:</strong> ${{node.notes}}</p>
          <p><a href="${{node.raw_link}}" target="_blank" rel="noopener">Open EJAtlas case</a></p>
        </div>
      `;
    }}

    function edgeHtml(edge) {{
      return `
        <div class="detail-block">
          <h3 class="detail-title">${{edge.source_case}} ↔ ${{edge.target_case}}</h3>
          <div class="pill">Weight ${{edge.weight}}</div>
        </div>
        <div class="detail-block">
          <p><strong>What this arc means:</strong> these two cases share multiple coded characteristics, so the graph displays a relational tie between them.</p>
          <p><strong>Relation reasons:</strong></p>
          <p>${{nl2br(edge.reasons.replaceAll('; ', '\\n'))}}</p>
        </div>
      `;
    }}

    function filteredData() {{
      const groupVal = groupFilter.value;
      const countryVal = countryFilter.value;
      const searchVal = searchFilter.value.trim().toLowerCase();
      const minWeight = Number(weightFilter.value);

      const visibleNodes = graphData.nodes.filter(node => {{
        const groupOk = groupVal === 'All' || node.core_group === groupVal;
        const countryOk = countryVal === 'All' || node.country === countryVal;
        const searchOk = !searchVal || node.case_name.toLowerCase().includes(searchVal);
        return groupOk && countryOk && searchOk;
      }});

      const visibleIds = new Set(visibleNodes.map(node => node.id));
      const visibleEdges = graphData.edges.filter(edge =>
        visibleIds.has(edge.source) &&
        visibleIds.has(edge.target) &&
        edge.weight >= minWeight
      );

      return {{ visibleNodes, visibleEdges }};
    }}

    function makeTraces(visibleNodes, visibleEdges) {{
      const nodeMap = new Map(visibleNodes.map(node => [node.id, node]));
      const connectedCounts = new Map(visibleNodes.map(node => [node.id, 0]));
      visibleEdges.forEach(edge => {{
        connectedCounts.set(edge.source, (connectedCounts.get(edge.source) || 0) + 1);
        connectedCounts.set(edge.target, (connectedCounts.get(edge.target) || 0) + 1);
      }});

      const traces = [];
      visibleEdges.forEach(edge => {{
        const source = nodeMap.get(edge.source);
        const target = nodeMap.get(edge.target);
        if (!source || !target) return;
        traces.push({{
          x: [source.x, target.x],
          y: [source.y, target.y],
          mode: 'lines',
          type: 'scatter',
          line: {{
            color: 'rgba(90, 106, 117, 0.42)',
            width: 0.8 + edge.weight * 0.7
          }},
          hovertemplate: `<b>${{source.case_name}}</b><br><b>${{target.case_name}}</b><br>Weight: ${{edge.weight}}<extra></extra>`,
          customdata: [{{ kind: 'edge', edge }} , {{ kind: 'edge', edge }}],
          showlegend: false
        }});
      }});

      traces.push({{
        x: visibleNodes.map(node => node.x),
        y: visibleNodes.map(node => node.y),
        mode: 'markers+text',
        type: 'scatter',
        text: visibleNodes.map(node => node.case_name.length > 26 ? node.case_name.slice(0, 23) + '...' : node.case_name),
        textposition: 'top center',
        textfont: {{ size: 10, color: '#22303c' }},
        marker: {{
          size: visibleNodes.map(node => 16 + (connectedCounts.get(node.id) || 0) * 2.4),
          color: visibleNodes.map(node => node.color),
          line: {{ color: '#ffffff', width: 1.1 }},
          opacity: 0.95
        }},
        hovertemplate: '<b>%{{customdata.case_name}}</b><br>%{{customdata.country}}<br>%{{customdata.core_group}}<extra></extra>',
        customdata: visibleNodes.map(node => ({{
          kind: 'node',
          ...node
        }})),
        showlegend: false
      }});

      return traces;
    }}

    function attachEvents() {{
      if (graphDiv.removeAllListeners) {{
        graphDiv.removeAllListeners('plotly_click');
      }}
      graphDiv.on('plotly_click', function(event) {{
        const point = event.points && event.points[0];
        if (!point || !point.customdata) return;
        if (point.customdata.kind === 'node') {{
          detailPanel.innerHTML = caseHtml(point.customdata);
        }} else if (point.customdata.kind === 'edge') {{
          detailPanel.innerHTML = edgeHtml(point.customdata.edge);
        }}
      }});
    }}

    function renderGraph() {{
      const {{ visibleNodes, visibleEdges }} = filteredData();
      visibleNodesEl.textContent = visibleNodes.length;
      visibleEdgesEl.textContent = visibleEdges.length;
      weightValue.textContent = weightFilter.value;

      const traces = makeTraces(visibleNodes, visibleEdges);
      const layout = {{
        margin: {{ l: 20, r: 20, t: 20, b: 20 }},
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {{ visible: false }},
        yaxis: {{ visible: false }},
        hoverlabel: {{
          bgcolor: '#fffdf8',
          bordercolor: '#cbbfa8',
          font: {{ color: '#1f2933' }}
        }}
      }};

      Plotly.newPlot(graphDiv, traces, layout, {{
        responsive: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
      }}).then(() => {{
        attachEvents();
        if (visibleNodes.length === 1) {{
          detailPanel.innerHTML = caseHtml(visibleNodes[0]);
        }} else {{
          detailPanel.innerHTML = defaultDetailHtml(visibleNodes, visibleEdges);
        }}
      }});
    }}

    [groupFilter, countryFilter, searchFilter, weightFilter].forEach(el => {{
      el.addEventListener('input', renderGraph);
      el.addEventListener('change', renderGraph);
    }});

    renderGraph();
  </script>
</body>
</html>"""


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_graph_payload()
    html = build_html(payload)
    output = FIG_DIR / "core_case_relation_network_interactive.html"
    output.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
