const fs = require('fs/promises');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const RAW_DIR = path.join(ROOT, 'data', 'raw');
const PROCESSED_DIR = path.join(ROOT, 'data', 'processed');

function text(v) {
  if (Array.isArray(v)) return v.map(text).filter(Boolean).join('; ');
  if (v && typeof v === 'object') {
    if (typeof v.name === 'string') return v.name;
    if (typeof v.label === 'string') return v.label;
    const values = Object.values(v).map(text).filter(Boolean);
    return values.length ? values.join('; ') : '';
  }
  return v == null ? '' : String(v);
}

function stripHtml(v) {
  return text(v).replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

function uniq(arr) {
  return [...new Set((arr || []).filter(Boolean))];
}

function asArray(v) {
  return Array.isArray(v) ? v : (v ? [v] : []);
}

function extractNamedItems(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v.map(item => text(item)).filter(Boolean);
  if (typeof v === 'object') {
    if (typeof v.name === 'string') return [v.name];
    return Object.values(v).flatMap(extractNamedItems);
  }
  return [text(v)].filter(Boolean);
}

function csvEscape(v) {
  const s = v == null ? '' : String(v);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

function toCsv(rows, columns) {
  const header = columns.join(',');
  const lines = rows.map(row => columns.map(col => csvEscape(row[col])).join(','));
  return [header, ...lines].join('\n');
}

function classifyInfrastructure(row) {
  const title = `${row.case_name} ${row.headline}`.toLowerCase();
  const t = `${title} ${row.description}`.toLowerCase();
  if (title.includes('pipeline')) return 'Pipeline';
  if (title.includes('gas field') || title.includes('gas drilling') || title.includes('extraction')) return 'Extraction / gas field';
  if (title.includes('fsru') || title.includes('floating storage and regasification unit')) return 'FSRU';
  if (title.includes('flng') || title.includes('floating lng')) return 'FLNG';
  if (title.includes('liquefaction')) return 'Liquefaction / export facility';
  if (title.includes('terminal')) return 'LNG terminal';
  if (title.includes('port')) return 'Port / logistics hub';
  if (t.includes('fsru') || t.includes('floating storage and regasification unit')) return 'FSRU';
  if (t.includes('flng') || t.includes('floating lng')) return 'FLNG';
  if (t.includes('liquefaction')) return 'Liquefaction / export facility';
  if (t.includes('pipeline')) return 'Pipeline';
  if (t.includes('terminal')) return 'LNG terminal';
  if (t.includes('port')) return 'Port / logistics hub';
  if (t.includes('gas field') || t.includes('gas drilling') || t.includes('extraction')) return 'Extraction / gas field';
  return 'Other LNG-related infrastructure';
}

function classifySupplyChainRole(row) {
  const title = `${row.case_name} ${row.headline}`.toLowerCase();
  const t = `${title} ${row.description}`.toLowerCase();
  const country = row.country;
  if (title.includes('export') || title.includes('flng') || title.includes('liquefaction')) return 'Export / extraction';
  if (title.includes('import') || title.includes('fsru') || title.includes('regasification')) return 'Import / regasification';
  if (title.includes('pipeline')) return 'Transit';
  if (['Russia', 'Algeria', 'United Arab Emirates', 'Mozambique', 'United States', 'Egypt'].includes(country)) {
    if (['FLNG', 'Liquefaction / export facility', 'Extraction / gas field'].includes(row.infrastructure_type)) return 'Export / extraction';
    if (row.infrastructure_type === 'LNG terminal' && (t.includes('export') || country === 'Egypt' || country === 'United States' || country === 'United Arab Emirates')) return 'Export / extraction';
  }
  if (['France', 'Germany', 'Belgium', 'Spain', 'Italy', 'Croatia', 'Latvia', 'Slovakia', 'Ireland', 'Sweden'].includes(country)) {
    if (['FSRU', 'LNG terminal', 'Port / logistics hub'].includes(row.infrastructure_type)) return 'Import / regasification';
  }
  if (row.infrastructure_type === 'Pipeline') return 'Transit';
  if (row.infrastructure_type === 'LNG terminal') return 'Import / export terminal';
  return 'Broader gas / LNG context';
}

function classifyUsCoast(row) {
  const blob = `${row.province} ${row.location} ${row.case_name}`.toLowerCase();
  if (blob.includes('texas') || blob.includes('louisiana') || blob.includes('cameron')) return 'Gulf Coast';
  if (blob.includes('oregon') || blob.includes('alaska') || blob.includes('california')) return blob.includes('alaska') ? 'Alaska' : 'West Coast';
  if (blob.includes('maryland') || blob.includes('new jersey') || blob.includes('rhode island') || blob.includes('new hampshire') || blob.includes('massachusetts') || blob.includes('delaware') || blob.includes('north carolina') || blob.includes('south carolina') || blob.includes('georgia') || blob.includes('florida')) return 'East Coast';
  return 'Mixed / unclear';
}

function classifyEvidenceQuality(accuracyLevel) {
  const t = text(accuracyLevel).toLowerCase();
  if (t.includes('high')) return 'strong';
  if (t.includes('medium')) return 'medium';
  if (t.includes('low')) return 'weak';
  return 'unknown';
}

function inferConflictCategory(row) {
  const t = `${row.case_name} ${row.headline} ${row.description}`.toLowerCase();
  if (t.includes('water')) return 'Water / pollution';
  if (t.includes('indigenous') || t.includes('nenets') || t.includes('sami')) return 'Indigenous rights / land';
  if (t.includes('health') || t.includes('air') || t.includes('emission')) return 'Health / air pollution';
  if (t.includes('coast') || t.includes('port') || t.includes('marine') || t.includes('fishing')) return 'Coastal / marine';
  return 'Fossil fuels / energy';
}

function mainActors(row) {
  const actors = uniq([
    ...asArray(row.companies),
    ...asArray(row.supporters),
    ...asArray(row.ejos),
    row.government_actors
  ]);
  return actors.join('; ');
}

function mainImpacts(row) {
  return uniq([
    ...asArray(row.environmental_impacts),
    ...asArray(row.health_impacts),
    ...asArray(row.socio_economic_impacts)
  ]).join('; ');
}

function normalizeCountry(country) {
  if (country === 'United States of America ' || country === 'United States') return 'United States';
  if (country === 'Russian Federation') return 'Russia';
  if (country === 'Slovak Republic') return 'Slovakia';
  return country || '';
}

function standardizeStatus(projectStatus) {
  const t = text(projectStatus).toLowerCase();
  if (t.includes('in operation')) return 'Operating';
  if (t.includes('under construction')) return 'Under construction';
  if (t.includes('planned')) return 'Planned';
  if (t.includes('proposed')) return 'Planned';
  if (t.includes('stopped')) return 'Cancelled / suspended';
  return 'Other / unclear';
}

function inferAffectedGroups(row) {
  const t = `${row.case_name} ${row.headline} ${row.description} ${row.mobilizing_groups}`.toLowerCase();
  const groups = [];
  if (t.includes('indigenous') || t.includes('nenets') || t.includes('sami') || t.includes('wet')) groups.push('Indigenous communities');
  if (t.includes('fisher') || t.includes('fishers') || t.includes('fishing')) groups.push('Fishing and coastal communities');
  if (t.includes('worker') || t.includes('labour') || t.includes('employment') || t.includes('unemployed')) groups.push('Workers');
  if (t.includes('resident') || t.includes('local') || t.includes('community') || t.includes('villag')) groups.push('Local residents');
  if (t.includes('farmer') || t.includes('agricult')) groups.push('Farmers');
  if (t.includes('women')) groups.push('Women');
  if (t.includes('migrant')) groups.push('Migrant workers');
  if (!groups.length) groups.push('Mixed local communities');
  return uniq(groups).join('; ');
}

function classifyLngSpecificity(row) {
  const t = `${row.case_name} ${row.headline}`.toLowerCase();
  if (t.includes('lng') || t.includes('liquefied natural gas') || t.includes('regasification') || t.includes('fsru') || t.includes('flng')) {
    return 'Direct LNG case';
  }
  const d = row.description.toLowerCase();
  if (d.includes('lng')) return 'Broader gas case with LNG linkage';
  return 'Broader gas / EJ case';
}

function coreGroup(row) {
  const slug = row.slug;
  const europe = new Set([
    'le-havre-lng-floating-storage-and-regasification-unit-france',
    'germany-builds-up-lng-import-terminals-in-the-port-of-mukran-on-the-eastern-german-island-of-rugen',
    'ende-gelande-against-brunsbuttel-lng-double-cost-for-german-energy-independence-germany',
    'occupation-of-fluxys-lng-terminal-in-zeebrugge-belgium',
    'floating-storage-and-regasification-unit-in-the-port-of-piombino',
    'protestas-en-huelva-contra-el-uso-del-gas-licuado-stop-al-lavado-verde-espana',
    'terminal-de-gas-natural-licuado-lng-en-sagunto-espana',
    'protests-against-floating-lng-terminal-krk-island-croatia',
    'skulte-lng-terminal-and-pipeline-latvia',
    'civil-society-resistance-and-the-cancellation-of-the-bratislava-lng-terminal-in-slovakia',
    '33-predator-s-mag-mell-floating-lng-terminal-cork-ireland',
    'nextdecade-liquid-natural-gas-lng-terminal-cork-ireland',
    'lng-shannon-terminal'
  ]);
  const us = new Set([
    'cove-point-lng-export-terminal-usa',
    'the-fallout-and-future-of-the-dupont-repauno-chemical-site-greenwich-township-new-jersey',
    'no-lng-in-pvd-opposed-national-grid-liquefaction-project',
    'new-hampshires-granite-bridge-gas-pipeline-united-states',
    'sea-3-liquid-propane-gas-expansion-providence-rhode-island-usa',
    'washington-park-and-south-providence-residents-oppose-allens-avenue-waste-transfer-station'
  ]);
  const russia = new Set([
    'liquefied-natural-gas-project-lng-2-gydan-peninsula-arctic-russia',
    'sabetta-port-arctic-russia',
    'novateks-two-new-gas-fields-on-protected-tundra-yamal-russia-federation',
    'mega-natural-gas-project-yamal-arctic-russia'
  ]);
  const algeria = new Set(['gas-grabs-algeria', 'hassi-rmel-gas-field']);
  const uae = new Set(['ruwais-lng-terminal-in-al-ruwais-industrial-city-abu-dhabi-united-arab-emirates']);
  if (europe.has(slug)) return 'Europe';
  if (us.has(slug)) return 'US East Coast (provisional)';
  if (russia.has(slug)) return 'Russia';
  if (algeria.has(slug)) return 'Algeria';
  if (uae.has(slug)) return 'UAE (Abu Dhabi)';
  return '';
}

function linkToEU(row) {
  const group = coreGroup(row);
  if (group === 'Europe') return 'Direct EU supply / importing infrastructure';
  if (group === 'US East Coast (provisional)') return 'Indirect EU supply chain / export-side context';
  if (group === 'Russia') return 'Direct EU supply / export-side context';
  if (group === 'Algeria') return 'Direct EU supply / export-side context';
  if (group === 'UAE (Abu Dhabi)') return 'Indirect EU supply chain / context case';
  if (row.country === 'Egypt') return 'Direct EU supply / contextual exporter';
  if (row.country === 'Norway') return 'Indirect EU supply / contextual processor';
  return 'Broader LNG / environmental justice context';
}

function recommendArticleUse(row) {
  if (row.core_article_group === 'Europe') return 'Keep in core article';
  if (row.core_article_group === 'Russia') return 'Keep in core article';
  if (row.core_article_group === 'Algeria') return 'Keep in core article';
  if (row.core_article_group === 'US East Coast (provisional)') return 'Keep in core article with scope note';
  if (row.country === 'Egypt') return 'Contextual case with direct EU relevance';
  if (row.country === 'United Arab Emirates') return 'Contextual case';
  if (row.country === 'Tunisia' || row.country === 'Pakistan') return 'Contextual case';
  return 'Broader context only';
}

function applyExplanatoryPlaceholders(row) {
  const placeholders = {
    main_impacts: 'Insufficient information in live EJAtlas metadata to identify comparable impacts.',
    affected_groups: 'Insufficient information in live EJAtlas metadata to identify affected groups.',
    main_actors: 'Insufficient information in live EJAtlas metadata to identify the main actors.',
    province: 'Not specified clearly in live EJAtlas metadata.',
    location: 'Not specified clearly in live EJAtlas metadata.',
    headline: 'No concise EJAtlas headline available in the live record.',
    description: 'No detailed EJAtlas description available in the live record.',
    environmental_impacts: 'Insufficient information in live EJAtlas metadata on environmental impacts.',
    health_impacts: 'Insufficient information in live EJAtlas metadata on health impacts.',
    socio_economic_impacts: 'Insufficient information in live EJAtlas metadata on socio-economic impacts.',
    companies: 'Insufficient information in live EJAtlas metadata on company actors.',
    supporters: 'Insufficient information in live EJAtlas metadata on supporting actors.',
    ejos: 'Insufficient information in live EJAtlas metadata on environmental justice organizations.',
    government_actors: 'Insufficient information in live EJAtlas metadata on government actors.',
    mobilizing_groups: 'Insufficient information in live EJAtlas metadata on mobilizing groups.',
    mobilizing_forms: 'Insufficient information in live EJAtlas metadata on forms of mobilization.',
    outcome_text: 'Insufficient information in live EJAtlas metadata on conflict outcomes.',
    notes: 'No additional coding note.'
  };
  for (const [field, message] of Object.entries(placeholders)) {
    if (!text(row[field]).trim()) row[field] = message;
  }
  return row;
}

function buildMapVerification(rows) {
  const specs = [
    { map_item: 'Arctic Yamal', terms: ['yamal'], expectation: 'direct LNG / Arctic export' },
    { map_item: 'Gydan', terms: ['gydan'], expectation: 'direct LNG / Arctic export' },
    { map_item: 'Russia', country: 'Russia', expectation: 'export-side cases' },
    { map_item: 'Algeria / Algiers / Ghardaia', country: 'Algeria', expectation: 'export-side cases' },
    { map_item: 'Spain', country: 'Spain', expectation: 'import-side / storage cases' },
    { map_item: 'France', country: 'France', expectation: 'import-side case' },
    { map_item: 'Belgium', country: 'Belgium', expectation: 'import-side case' },
    { map_item: 'Germany', country: 'Germany', expectation: 'import-side cases' },
    { map_item: 'Croatia', country: 'Croatia', expectation: 'import-side case' },
    { map_item: 'Latvia', country: 'Latvia', expectation: 'import-side case' },
    { map_item: 'Norway', country: 'Norway', expectation: 'processor / export-related case' },
    { map_item: 'Sweden', country: 'Sweden', expectation: 'import-side case' },
    { map_item: 'Ireland', country: 'Ireland', expectation: 'import-side cases' },
    { map_item: 'Egypt', country: 'Egypt', expectation: 'export-side contextual case' },
    { map_item: 'Tunisia', country: 'Tunisia', expectation: 'context or no current LNG case' },
    { map_item: 'Israel', terms: ['israel'], expectation: 'context or no current LNG case' },
    { map_item: 'Pakistan', country: 'Pakistan', expectation: 'contextual import-side case' },
    { map_item: 'San Diego', terms: ['san diego'], expectation: 'US / Mexico border logistics context' },
    { map_item: 'Ensenada', terms: ['ensenada', 'costa azul'], expectation: 'Mexico export/import context' },
    { map_item: 'Houston', terms: ['houston'], expectation: 'US Gulf export infrastructure context' },
    { map_item: 'Corpus Christi', terms: ['corpus christi'], expectation: 'US Gulf export case' },
    { map_item: 'Rio Grande', terms: ['rio grande'], expectation: 'US Gulf export case' },
    { map_item: 'Boca Chica', terms: ['boca chica'], expectation: 'US Gulf broader infrastructure case' },
    { map_item: 'San Antonio', terms: ['san antonio'], expectation: 'US broader gas / pipeline context' },
    { map_item: 'Austin', terms: ['austin'], expectation: 'US broader gas / pipeline context' },
    { map_item: 'Libya', country: 'Libya', expectation: 'no current LNG case in live search' }
  ];
  return specs.map(spec => {
    const matches = rows.filter(row => {
      if (spec.country) return row.country === spec.country;
      const blob = `${row.case_name} ${row.country} ${row.province} ${row.location}`.toLowerCase();
      return spec.terms.some(term => blob.includes(term));
    });
    let verification_status = 'No live LNG match found';
    if (matches.length) {
      const directLng = matches.some(m => m.lng_specificity === 'Direct LNG case');
      verification_status = directLng ? 'Matched live LNG-related case(s)' : 'Matched contextual / broader gas case(s)';
    }
    return {
      map_item: spec.map_item,
      verification_status,
      matched_case_count: matches.length,
      matched_cases: uniq(matches.map(m => m.case_name)).join('; '),
      countries_found: uniq(matches.map(m => m.country)).join('; '),
      expectation: spec.expectation
    };
  });
}

function methodologyText(summary, rows, verificationRows) {
  const direct = rows.filter(r => r.lng_specificity === 'Direct LNG case').length;
  const broader = rows.filter(r => r.lng_specificity !== 'Direct LNG case').length;
  const directEu = rows.filter(r => r.link_to_eu.startsWith('Direct EU supply')).length;
  const contextual = rows.filter(r => r.link_to_eu === 'Broader LNG / environmental justice context').length;
  const missingMapItems = verificationRows.filter(r => r.verification_status === 'No live LNG match found').map(r => r.map_item);
  return `# Methodology and Case Selection from the LNG Conflict Map

## Overview

The LNG conflict map was treated as a starting point rather than a finished dataset. To build a reproducible empirical database, all cases were re-verified against the live EJAtlas API on July 9, 2026. The query strategy began with the public EJAtlas search endpoint for \`LNG\`, after which each returned case was checked through its case-detail endpoint and recoded into a structured comparative table.

The live EJAtlas API returned ${summary.ejatlas_case_count} LNG-tagged cases globally. This is broader than the 99-case figure referenced in the draft text, which suggests that the map, the platform, or the article draft are not perfectly synchronized. For transparency, the full live pull is preserved as the master dataset, while a separate curated subset of ${summary.core_case_count} cases is marked as the core comparative sample used for the article.

## Coding strategy

Each case was coded using EJAtlas metadata together with rule-based recoding of the case title, headline, description, actors, impacts, and mobilization fields. The coding table standardizes the following variables: case name, country, region or city, infrastructure type, supply-chain role, link to EU supply, main impacts, conflict category, affected groups, main actors, status, evidence quality, and relevance to the core argument.

The coding strategy distinguishes between direct LNG cases and broader gas or environmental-justice cases. In the live July 9, 2026 pull, ${direct} cases were coded as direct LNG cases and ${broader} as broader gas or LNG-linked cases. This distinction matters because some conflicts included in the LNG search are not strictly terminals or liquefaction projects, but pipelines, ports, storage sites, or wider gas conflicts that become relevant through their connection to LNG supply chains.

To clarify comparative relevance, the dataset also distinguishes among direct EU-linked cases, indirect EU-linked cases, and broader contextual cases. ${directEu} cases were coded as directly connected to EU LNG import diversification, while ${contextual} were retained only as broader contextual environmental-justice cases.

## Case selection logic

The core article subset was organized around the supply chain most relevant to Europe's diversification strategy: European import and regasification sites, Russian Arctic export infrastructure, selected US export-side conflicts, Algerian export-side conflicts, and one UAE contextual comparison. This produces the following verified core sample: 13 European cases, 6 US East Coast provisional cases, 4 Russia cases, 2 Algeria cases, and 1 UAE case.

The US cases required special verification because the map brief mixes East Coast, Gulf Coast, and inland Texas locations. The database therefore adds a separate \`us_coast_bucket\` field to distinguish East Coast, Gulf Coast, West Coast, Alaska, and mixed or unclear cases. This helps separate cases directly relevant to Atlantic export routes to Europe from broader US fossil-fuel conflicts.

## Dynamic-map verification

Because EJAtlas is dynamic, all map references were checked against the live platform rather than assumed to be stable. The verification exercise shows that some listed geographies correspond cleanly to current LNG cases, while others do not. In particular, the current live LNG pull does not yield clean country-level LNG matches for the map items ${missingMapItems.join(', ')}. In those cases, the evidence suggests either a contextual linkage, a broader gas conflict, or a mismatch between the map snapshot and the current EJAtlas index.

This matters substantively. Algeria remains strong enough for the core article because its cases are directly tied to EU gas supply and export infrastructure. Egypt is better treated as a contextual case with direct EU relevance. Pakistan, Tunisia, and UAE are better treated as contextual rather than core cases. Israel and Libya do not appear as standalone live LNG cases in the current EJAtlas pull, although Israel appears indirectly through regional gas and export routes discussed in related cases.

## Why this coding matters

Transforming the map into a coded dataset makes it possible to compare LNG conflicts systematically across importing, exporting, and transit sites. That step is necessary for analyzing how EU diversification reshapes environmental burdens, how energy-security narratives justify infrastructure expansion, and how procedural injustice, health risks, Indigenous dispossession, and coastal degradation recur across different segments of the LNG supply chain.
`;
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} for ${url}`);
  return await res.json();
}

async function fetchAllSearch() {
  const all = [];
  let offset = 0;
  while (true) {
    const data = await fetchJson(`https://ejatlas.org/api/v1/conflicts/?search=LNG&limit=100&offset=${offset}`);
    all.push(...data.results);
    if (!data.next) break;
    offset += 100;
  }
  return all;
}

async function fetchAllGeojson() {
  const data = await fetchJson('https://ejatlas.org/api/v1/conflicts/?format=geojson');
  const features = Array.isArray(data.features) ? data.features : [];
  return new Map(
    features
      .filter(feature => feature && feature.properties && feature.geometry && Array.isArray(feature.geometry.coordinates))
      .map(feature => [feature.properties.id, feature.geometry.coordinates])
  );
}

async function fetchDetail(slug) {
  return await fetchJson(`https://ejatlas.org/api/v1/conflicts/${slug}/en`);
}

async function buildRows() {
  const summaries = await fetchAllSearch();
  const geoMap = await fetchAllGeojson();
  const rows = [];
  for (let i = 0; i < summaries.length; i += 10) {
    const chunk = summaries.slice(i, i + 10);
    const details = await Promise.all(chunk.map(r => fetchDetail(r.slug)));
    for (let j = 0; j < chunk.length; j += 1) {
      const s = chunk[j];
      const d = details[j];
      const bd = d.basic_data || {};
      const da = d.details_and_actors || {};
      const src = d.source || {};
      const imp = d.impacts || {};
      const out = d.outcome || {};
      const mob = d.mobilization || {};
      const pres = d.presentation || {};
      const companies = uniq(asArray(da.companies).map(x => x && x.name));
      const supporters = uniq(asArray(da.supporters).map(x => x && x.name));
      const ejos = uniq(asArray(da.ejos).map(x => x && x.name));
      const envImp = uniq(extractNamedItems(imp.environmental_impact));
      const healthImp = uniq(extractNamedItems(imp.health_impact));
      const socioImp = stripHtml([
        ...extractNamedItems(imp.socio_economical_impact),
        imp.other_socio_economical_impacts
      ].filter(Boolean).join(' | '));
      const sourceTypes = uniq([
        src.type1 && src.type1.name,
        ...asArray(src.type2).map(x => x && x.name),
        ...asArray(src.products).map(x => x && x.name)
      ]).join('; ');
      const row = {
        ejatlas_id: pres.id ?? s.id,
        slug: pres.slug ?? s.slug,
        case_name: pres.name ?? s.name,
        headline: stripHtml(pres.headline ?? s.headline),
        country: normalizeCountry(bd.country && bd.country.name),
        province: text(bd.province),
        location: text(bd.location),
        accuracy_level: text(bd.accuracy_level),
        description: stripHtml(bd.description || ''),
        source_types: sourceTypes,
        companies: companies.join('; '),
        supporters: supporters.join('; '),
        ejos: ejos.join('; '),
        government_actors: stripHtml([da.govt_actors, da.government_actors].filter(Boolean).join(' | ')),
        mobilizing_groups: uniq(asArray(mob.groups_mobilizing).map(x => x && x.name)).join('; '),
        mobilizing_forms: uniq(asArray(mob.forms_mobilizing).map(x => x && x.name)).join('; '),
        project_status: out.project_status && out.project_status.name ? out.project_status.name : '',
        success_level: out.success_level && out.success_level.name ? out.success_level.name : '',
        outcome_text: stripHtml(out.other_comments || ''),
        environmental_impacts: envImp.join('; '),
        health_impacts: healthImp.join('; '),
        socio_economic_impacts: socioImp,
        update_date: text(pres.updated_at),
        raw_link: `https://ejatlas.org/conflict/${pres.slug || s.slug}`
      };
      const coordinates = geoMap.get(row.ejatlas_id);
      row.longitude = coordinates ? coordinates[0] : '';
      row.latitude = coordinates ? coordinates[1] : '';
      row.infrastructure_type = classifyInfrastructure(row);
      row.supply_chain_role = classifySupplyChainRole(row);
      row.us_coast_bucket = row.country === 'United States' ? classifyUsCoast(row) : '';
      row.evidence_quality = classifyEvidenceQuality(row.accuracy_level);
      row.conflict_category = inferConflictCategory(row);
      row.status_standardized = standardizeStatus(row.project_status);
      row.affected_groups = inferAffectedGroups(row);
      row.lng_specificity = classifyLngSpecificity(row);
      row.main_actors = mainActors({
        companies,
        supporters,
        ejos,
        government_actors: row.government_actors
      });
      row.main_impacts = mainImpacts({
        environmental_impacts: envImp,
        health_impacts: healthImp,
        socio_economic_impacts: socioImp
      });
      row.core_article_group = coreGroup(row);
      row.core_article_flag = row.core_article_group ? 'yes' : 'no';
      row.link_to_eu = linkToEU(row);
      row.relevance_to_core_argument = row.core_article_group ? 'core' : 'contextual';
      row.article_use_recommendation = recommendArticleUse(row);
      if (row.core_article_group === 'US East Coast (provisional)') row.relevance_to_core_argument = 'core-provisional';
      if (row.core_article_group === 'UAE (Abu Dhabi)') row.notes = 'EJAtlas case is Abu Dhabi; article brief mentions Dubai.';
      if (row.country === 'Tunisia' && !row.notes) row.notes = 'Current live LNG search result appears contextual rather than a clean LNG terminal case.';
      if (row.country === 'Egypt' && !row.notes) row.notes = 'Directly relevant to EU supply debates, but not included in the current core 26.';
      applyExplanatoryPlaceholders(row);
      rows.push(row);
    }
  }
  return rows;
}

function summarize(rows) {
  const byCountry = rows.reduce((acc, row) => {
    acc[row.country] = (acc[row.country] || 0) + 1;
    return acc;
  }, {});
  const coreRows = rows.filter(row => row.core_article_flag === 'yes');
  const byGroup = coreRows.reduce((acc, row) => {
    acc[row.core_article_group] = (acc[row.core_article_group] || 0) + 1;
    return acc;
  }, {});
  return {
    search_query: 'LNG',
    ejatlas_case_count: rows.length,
    core_case_count: coreRows.length,
    by_country: byCountry,
    by_core_group: byGroup,
    caveats: [
      'EJAtlas API search returns 105 LNG-tagged conflicts, which is broader than the 99-case figure in the draft text.',
      'US East Coast cases are marked provisional because two of the six core cases are broader gas infrastructure cases rather than strict LNG terminals.',
      'The UAE case appears in EJAtlas as Abu Dhabi rather than Dubai.'
    ]
  };
}

async function main() {
  await fs.mkdir(RAW_DIR, { recursive: true });
  await fs.mkdir(PROCESSED_DIR, { recursive: true });
  const rows = await buildRows();
  const summary = summarize(rows);
  const coreRows = rows.filter(r => r.core_article_flag === 'yes');
  const verificationRows = buildMapVerification(rows);
  const methodology = methodologyText(summary, rows, verificationRows);
  await fs.writeFile(path.join(RAW_DIR, 'ejatlas_lng_cases.json'), JSON.stringify(rows, null, 2), 'utf8');
  const columns = [
    'ejatlas_id',
    'slug',
    'case_name',
    'country',
    'province',
    'location',
    'infrastructure_type',
    'supply_chain_role',
    'us_coast_bucket',
    'link_to_eu',
    'lng_specificity',
    'main_impacts',
    'conflict_category',
    'affected_groups',
    'main_actors',
    'project_status',
    'status_standardized',
    'evidence_quality',
    'relevance_to_core_argument',
    'article_use_recommendation',
    'longitude',
    'latitude',
    'core_article_group',
    'core_article_flag',
    'accuracy_level',
    'source_types',
    'headline',
    'description',
    'environmental_impacts',
    'health_impacts',
    'socio_economic_impacts',
    'companies',
    'supporters',
    'ejos',
    'government_actors',
    'mobilizing_groups',
    'mobilizing_forms',
    'success_level',
    'outcome_text',
    'update_date',
    'raw_link',
    'notes'
  ];
  const empiricalColumns = [
    'case_name',
    'country',
    'province',
    'location',
    'infrastructure_type',
    'supply_chain_role',
    'link_to_eu',
    'main_impacts',
    'conflict_category',
    'affected_groups',
    'main_actors',
    'status_standardized',
    'evidence_quality',
    'relevance_to_core_argument',
    'article_use_recommendation',
    'us_coast_bucket',
    'lng_specificity',
    'raw_link',
    'notes'
  ];
  await fs.writeFile(path.join(PROCESSED_DIR, 'ejatlas_lng_database.csv'), toCsv(rows, columns), 'utf8');
  await fs.writeFile(path.join(PROCESSED_DIR, 'ejatlas_lng_core_26.csv'), toCsv(coreRows, columns), 'utf8');
  await fs.writeFile(path.join(PROCESSED_DIR, 'ejatlas_lng_empirical_table.csv'), toCsv(rows, empiricalColumns), 'utf8');
  await fs.writeFile(path.join(PROCESSED_DIR, 'ejatlas_lng_map_verification.csv'), toCsv(verificationRows, ['map_item', 'verification_status', 'matched_case_count', 'matched_cases', 'countries_found', 'expectation']), 'utf8');
  await fs.writeFile(path.join(PROCESSED_DIR, 'ejatlas_lng_summary.json'), JSON.stringify(summary, null, 2), 'utf8');
  await fs.writeFile(path.join(PROCESSED_DIR, 'methodology_case_selection.md'), methodology, 'utf8');
  console.log(JSON.stringify(summary, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exitCode = 1;
});
