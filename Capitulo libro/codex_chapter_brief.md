# Codex Brief â€” Book Chapter Draft Based on the Master's Thesis and the Camino de Lengerke Case

## 1) Mission

Produce a **fully traceable, evidence-based draft of a book chapter in English** that adapts the master's thesis **â€œTurismo sostenible y pandemias, el caso del Camino de Santiagoâ€** into a chapter aligned with the UNAB call for chapters **â€œProductivity, Competitiveness, and Development: Perspectives from Economics and Business Management.â€**

The chapter must:

1. **Reuse the thesis only as a traceable source** for the original research design, interview logic, analytical categories, and the Camino de Santiago case background.
2. **Extend the discussion to the Camino de Lengerke (Santander, Colombia)** using **internet sources downloaded during this task**.
3. Be **strictly non-inventive**:
   - no fabricated citations,
   - no fabricated facts,
   - no fabricated interviews,
   - no fabricated data,
   - no fabricated DOI,
   - no fabricated claims about Scopus quartiles.
4. Build the argument from:
   - downloaded **Scopus Q1 literature**,
   - the attached master's thesis,
   - the attached call for chapters,
   - official or highly credible web sources on the Camino de Lengerke and tourism statistics in Colombia.

The final text must be polished enough to serve as a strong **first full draft** for later author revision.

---

## 2) Mandatory input files

Use these files as the starting point:

- `MEMORIA PFM LAURA JULIANA Para entregar.docx`
- `CALL-CHAPTERS-FACULTY-ECONOMICS-BUSINESS.pdf`

Treat the thesis as the **source for methodological adaptation**, not as a substitute for peer-reviewed literature.

---

## 3) Non-negotiable constraints

### 3.1 No invention
You must not invent:

- problem statement,
- objectives,
- theoretical claims,
- comparative findings,
- DOI,
- journal quartile,
- article metadata,
- empirical evidence for the Camino de Lengerke,
- any primary data not explicitly present in the thesis.

If something cannot be verified, write it down as **unverified** and exclude it from the chapter narrative.

### 3.2 Only cite what you have actually checked
Every cited paper must satisfy all of the following:

- identified in a Scopus-indexed journal,
- verified as **Q1** through an auditable source,
- downloaded and read at least in abstract/introduction/conclusion/method/results sections as needed,
- stored in the project folder,
- represented in the evidence matrix.

If a paper cannot be downloaded, do **not** cite it in the chapter.

### 3.3 No false empirical extension
Do **not** claim that fieldwork was conducted on the Camino de Lengerke unless such fieldwork exists in the supplied files.  
The chapter must therefore be framed as a **documentary-comparative and methodological adaptation study**, not as original primary-data fieldwork in Santander.

### 3.4 English only
Write the chapter in clear academic English.

### 3.5 Alignment with the call
The chapter must clearly fit the callâ€™s scope in **sustainability, regional development, competitiveness, and applied research**, especially the themes:

- **Innovation, Sustainability and Socioeconomic and Productive Transformation**
- **Internationalisation, Competitiveness and Regional Development**

The chapter must explicitly connect heritage walking routes and sustainable tourism with:

- regional development,
- local value creation,
- territorial competitiveness,
- sustainable management of heritage assets,
- small-scale local business opportunities.

Do not force â€œproductivityâ€ in an artificial way. Use it only where the evidence genuinely supports discussion of local service capacity, destination management efficiency, or value creation.

---

## 4) Required use of the skill for papers

Use the skill named **`sci papers downloader`** if available in the Codex environment.

### Paper acquisition target
Download **at least 30 peer-reviewed papers from Scopus Q1 journals**.

### If the skill is not available
Stop immediately and report:

- that the skill is unavailable,
- how far you got,
- what alternative evidence was collected,
- and which task remains blocked.

Do not silently replace this requirement with unverified browsing.

---

## 5) Literature acquisition protocol

## 5.1 Search focus

Build the literature corpus around these thematic clusters:

### Cluster A â€” Camino de Santiago / pilgrimage / heritage walking routes
Use combinations of terms such as:

- "Camino de Santiago"
- pilgrimage tourism
- pilgrimage route
- heritage trail
- cultural route
- walking tourism
- slow tourism
- route-based tourism

### Cluster B â€” Sustainable tourism and regional development
Use combinations of:

- sustainable tourism
- destination sustainability
- rural development
- local development
- territorial development
- community-based tourism
- resilience
- adaptation
- overtourism
- carrying capacity
- destination governance
- heritage management

### Cluster C â€” Business and development angle for call alignment
Use combinations of:

- regional competitiveness
- territorial competitiveness
- local value creation
- tourism entrepreneurship
- tourism-led development
- small business development
- service ecosystems
- place-based development
- inclusive development
- sustainable business models

## 5.2 Selection rule
Prefer literature that can help answer one or more of these questions:

1. How do heritage walking routes contribute to sustainable regional development?
2. How does pilgrimage or slow tourism differ from mass tourism?
3. What governance, sustainability, or resilience challenges affect walking-route tourism?
4. How can a qualitative framework from the Camino de Santiago be adapted to another historical route?
5. How can such routes be discussed in terms relevant to competitiveness and economic development?

## 5.3 Scopus Q1 verification
For every paper, verify Q1 status from an auditable source. Preferred order:

1. official Scopus source details / CiteScore-based source profile,
2. SCImago journal profile if Scopus source detail is inaccessible,
3. another clearly auditable source explicitly tied to Scopus quartile logic.

Record the verification source in the matrix.

If quartile cannot be verified, do not include that paper in the final 30-paper set.

---

## 6) Folder and file outputs

Create and populate the following outputs.

### 6.1 Literature folder
`/papers/`

Store the downloaded PDFs here using a consistent filename pattern:

`[FirstAuthorLastName]_[Year]_[ShortTitle].pdf`

### 6.2 Main evidence matrix
`/evidence/article_evidence_matrix.csv`

Mandatory columns:

- `article_id`
- `apa_reference`
- `doi`
- `journal`
- `year`
- `scopus_q1_verified` (Yes/No)
- `quartile_verification_source`
- `pdf_downloaded` (Yes/No)
- `exact_phrase`
- `page_or_section`
- `theme_code`
- `why_it_matters_for_chapter`
- `target_chapter_section`

### 6.3 Lengerke web evidence matrix
`/evidence/lengerke_web_matrix.csv`

Mandatory columns:

- `source_id`
- `institution_or_publisher`
- `url`
- `date_accessed`
- `source_type` (official / academic project / reputable media / tourism institution)
- `exact_excerpt`
- `use_in_chapter`
- `credibility_note`
- `claim_status` (usable / contextual only / do not use)

### 6.4 Thesis extraction memo
`/notes/thesis_method_extraction.md`

This memo must distill, in explicit steps, the thesis methodology into a transferable framework.

### 6.5 Call alignment memo
`/notes/call_alignment.md`

This memo must state exactly how the proposed chapter matches the call.

### 6.6 Draft chapter
`/draft/chapter_draft.md`

### 6.7 Gap log
`/notes/evidence_gaps.md`

List every missing or weak point that could not be verified.

---

## 7) How to read and extract the thesis

Read the thesis carefully and extract only what is explicitly supported by the text.

Focus on:

- research objective,
- research question,
- methodological approach,
- type of research,
- sampling logic,
- interview structure,
- analytical categories,
- key interpretive findings,
- aspects that can be generalized as a **replicable protocol**.

From the thesis, derive an explicit transferable methodology such as:

1. define the route-based tourism problem,
2. delimit sustainability and development categories,
3. identify stakeholders,
4. define the territorial unit,
5. use documentary context-building,
6. design qualitative instruments,
7. analyse economic, social, and environmental impacts,
8. derive management recommendations.

Do **not** claim that the thesis produced inferential statistical results.  
Treat it as a **qualitative, exploratory-descriptive, applied study**.

---

## 8) How to build the Lengerke case

The Lengerke section must rely on **downloaded internet sources** and must clearly distinguish:

- **official/legal heritage evidence**,
- **tourism/destination evidence**,
- **territorial/contextual evidence**,
- **media evidence used only as context**, not as sole proof for strong claims.

### 8.1 Priority sources for the Lengerke case

Prioritize and download evidence from sources such as:

1. **Ministry of Culture / official normogram**
   - ResoluciÃ³n 688 de 2015 MC on Barichara, Camino de Guane and protection framework.
   - Use this for heritage status, protection logic, sustainability/management language.

2. **ICOMOS Colombia**
   - For BIC identification and heritage record of the Camino Real Baricharaâ€“Guane.

3. **DANE tourism portal**
   - Use for national tourism statistics infrastructure and available tourism data instruments:
     - EGIT
     - ENH
     - EVI

4. **UIS / Caminos de Santander**
   - Use for the broader network logic and route-system framing.

5. **Santander regional tourism portals**
   - Use for route description and place positioning.

6. **High-quality regional media**
   - Use only to document current issues such as preservation challenges or route relevance.
   - These must never be the sole support for core theoretical claims.

### 8.2 Minimum factual base to verify for Lengerke
Try to verify, with auditable sources, facts such as:

- what the Camino de Lengerke are,
- which municipalities/segments are commonly associated with them,
- heritage relevance of the Baricharaâ€“Guane route,
- why these routes matter for local history and regional development,
- whether there are preservation, signage, or management concerns,
- whether official planning/protection language exists.

If you cannot verify a fact, do not use it.

---

## 9) Required source anchors already identified

Use these as starting points, but still inspect them directly before writing.

### 9.1 Call for chapters
The uploaded call requires:

- abstract,
- keywords,
- introduction,
- methodology,
- results and discussion,
- conclusions,
- references,
- author profiles,
- APA 7th,
- 12 to 18 pages,
- black-and-white tables/figures,
- at least 25 references recommended.

### 9.2 Thesis methodological anchor
The thesis provides a basis for extracting:

- a qualitative research approach,
- documentary review,
- non-probabilistic stakeholder-focused logic,
- interview-based data collection,
- analytical categories linked to sustainable tourism, local development, resilience, and social/environmental effects.

### 9.3 Web sources for Lengerke and context
The following types of sources have already been identified and should be checked directly:

- DANE tourism page for EGIT / ENH / EVI
- Mincultura normogram for ResoluciÃ³n 688 de 2015
- ICOMOS Colombia record for Camino Real de Barichara a Guane
- UIS â€œCaminos de Santanderâ€
- Santander regional tourism portal referring to the route network and its territorial significance

---

## 10) Required chapter logic

The chapter must **not** read like a simple summary of the thesis.  
It must become a new chapter with a stronger economic-and-regional-development framing.

## 10.1 Suggested working title
Use a title close to this logic:

**Sustainable Heritage Walking Routes, Local Value Creation, and Regional Development: Adapting a Qualitative Framework from the Camino de Santiago to the Camino de Lengerke in Santander, Colombia**

You may refine the title, but preserve the same meaning.

## 10.2 Core contribution
The chapter should contribute three things:

1. **A methodological contribution**  
   A replicable step-by-step framework extracted from the Santiago thesis.

2. **A comparative conceptual contribution**  
   A reasoned comparison between the Camino de Santiago and the Camino de Lengerke as heritage walking routes.

3. **A territorial development contribution**  
   An argument about how route-based sustainable tourism can support regional development and competitiveness when properly governed and preserved.

---

## 11) Required chapter structure

Write the chapter in markdown and organize it exactly in the following order.

### 11.1 Title

### 11.2 Abstract
Maximum 250 words.

### 11.3 Keywords
3 to 5 keywords.

### 11.4 Introduction
The introduction must do all of the following:

- define the broader problem of sustainable tourism and route-based heritage development,
- explain why walking routes matter for regional development and territorial competitiveness,
- show why the Camino de Santiago is a useful reference case,
- introduce the Camino de Lengerke as the second territorial case,
- explain the relevance of the chapter to the UNAB call,
- state the chapter objective,
- briefly preview the section structure.

Important:  
The problem statement and objective must be built from downloaded literature and verified territorial evidence.  
Do not copy the thesis objective verbatim unless it is explicitly reframed and justified.

### 11.5 Methodology
This section must clearly state that the chapter is based on:

- documentary analysis,
- structured literature review of downloaded Scopus Q1 papers,
- methodological extraction from the masterâ€™s thesis,
- comparative case adaptation,
- internet-based territorial evidence for the Camino de Lengerke.

This section must explicitly separate:

- the **original thesis fieldwork**,
- and the **present chapterâ€™s documentary-comparative method**.

Do not create the impression that you performed new interviews in Santander.

### 11.6 Results and Discussion
Organize this section into four subsections.

#### A. What the masterâ€™s thesis contributes as a transferable framework
Explain, in explicit steps, the methodology extracted from the Santiago thesis.

#### B. Replicable methodological protocol for another route context
Translate the thesis into a step-by-step protocol that could be applied to the Camino de Lengerke or similar heritage walking routes.

This subsection must be concrete and operational.  
For example, include a numbered sequence such as:

1. define the route and development problem,
2. identify analytical categories,
3. delimit territory,
4. identify stakeholders,
5. gather documentary and statistical baseline,
6. design data collection instruments,
7. classify impacts,
8. derive governance recommendations.

#### C. The Camino de Lengerke as an adaptation case
Use only verified web evidence to explain:

- route/historical significance,
- territorial location,
- heritage and protection framework,
- tourism and development relevance,
- management and preservation issues.

#### D. Comparative discussion
Compare Santiago and Lengerke on dimensions such as:

- scale,
- international visibility,
- heritage status,
- tourism pressure,
- rural/local development potential,
- governance maturity,
- sustainability risks,
- business and competitiveness implications.

All comparison points must be evidence-based and cautious.

### 11.7 Conclusions
The conclusion must include:

- what the adapted framework contributes,
- what the Lengerke case reveals,
- limits of the available evidence,
- recommendations for future research,
- practical implications for regional development and sustainable route governance.

### 11.8 References
Use only sources actually checked and cited.

### 11.9 Author profiles
Create a placeholder subsection if author details are not provided.

---

## 12) Evidence matrix rules

## 12.1 Article evidence matrix
For each Scopus Q1 article, extract at least one exact phrase that is genuinely useful for the chapter.

The phrase must support one of these functions:

- problem justification,
- conceptual definition,
- sustainable tourism argument,
- pilgrimage/route tourism framing,
- regional development logic,
- competitiveness/value creation logic,
- governance/resilience logic,
- methodological support.

The phrase must be copied exactly and associated with page number or section.

## 12.2 How the matrix should be used
The matrix is not a dump. It is the core audit trail for writing.

Every major paragraph of the chapter should be traceable to one or more rows in the matrix.

## 12.3 Recommended theme codes
Use consistent theme codes such as:

- `PROB` = problem framing
- `SUST` = sustainable tourism
- `PILG` = pilgrimage / route tourism
- `RDEV` = regional development
- `COMP` = competitiveness / value creation
- `GOV` = governance
- `RES` = resilience / adaptation
- `METH` = methodology
- `CASE` = case-specific relevance

---

## 13) Writing rules for the chapter

### 13.1 Tone
Write in formal academic prose.

### 13.2 Style
Avoid inflated language, generic claims, and unsupported assertions.

### 13.3 Chapter should feel publishable
The chapter must read as an integrated scholarly piece, not as notes.

### 13.4 No overclaiming
Be especially careful with claims such as:

- â€œthe Camino de Lengerke generate X economic impactâ€
- â€œthe route is already a consolidated tourism productâ€
- â€œthe method proves...â€
- â€œthe route functions exactly like the Camino de Santiagoâ€

Only make claims that are explicitly supported.

### 13.5 Comparative caution
The Camino de Santiago is a globally consolidated route; the Camino de Lengerke are not equivalent in scale.  
The comparison must therefore be framed as **methodological and conceptual adaptation**, not as a claim of identical tourism maturity.

### 13.6 Citation discipline
Each literature-dependent paragraph should cite relevant peer-reviewed sources from the downloaded set.  
Each Lengerke factual paragraph should cite its web evidence source(s).  
Do not cite sources you did not inspect.

---

## 14) What the chapter must explicitly deliver conceptually

The chapter must show, with evidence, that:

1. heritage walking routes can be analysed as more than cultural assets; they can also be discussed as territorial development assets;
2. the Santiago thesis offers a transferable qualitative logic;
3. a secondary-data/documentary adaptation can be responsibly built for the Camino de Lengerke without pretending new fieldwork;
4. route preservation, governance, and local business/ecosystem effects are central to any argument about development and competitiveness;
5. a stronger future study on Lengerke would require local fieldwork, stakeholder interviews, and route-level data.

---

## 15) Recommended internet sources to inspect first

Check and download these sources first if accessible.

### Official / institutional
- DANE tourism portal  
  `https://www.dane.gov.co/index.php/estadisticas-por-tema/servicios/turismo`

- Mincultura normogram â€” ResoluciÃ³n 688 de 2015  
  `https://normograma.mincultura.gov.co/compilacion/docs/resolucion_mincultura_0688_2015.htm`

- ICOMOS Colombia â€” Camino Real de Barichara a Guane  
  `https://www.icomoscolombia.org/bic/922`

### Regional / academic project
- Santander Travel / Lengerke route description  
  `https://www.santander.ccbserver.com/tesoros-15-m/6-los-caminos-de-geo-von-lengerke.htm`

- UIS / Caminos de Santander  
  `https://caminosdesantander.uis.edu.co/portfolio-filter/caminos-de-lengerke/`

### Contextual media (use with caution)
- Only after official sources have been processed.
- Use them mainly for preservation issues, public debates, or recent contextual developments.
- Mark them as â€œcontextualâ€ in the web matrix unless they are directly corroborated elsewhere.

---

## 16) Quality-control checklist before finishing

Do not finish the task until every item below is checked.

### Literature corpus
- [ ] At least 30 downloaded Q1 papers
- [ ] Every included paper has DOI or a clear note if unavailable
- [ ] Q1 verification recorded
- [ ] No undownloaded paper is cited in the chapter

### Evidence matrices
- [ ] Article evidence matrix completed
- [ ] Lengerke web matrix completed
- [ ] Exact phrases included
- [ ] Relevance explained row by row

### Chapter content
- [ ] English only
- [ ] Introduction aligned with the call
- [ ] Methodology clearly distinguishes thesis fieldwork from present documentary chapter method
- [ ] Results and discussion structured in four subsections
- [ ] Conclusions include limits and future research
- [ ] References are real and checked
- [ ] No fabricated evidence

### Formatting
- [ ] Markdown file created
- [ ] Chapter can be easily converted later to Arial 12, APA 7, black-and-white tables/figures
- [ ] Draft length is appropriate for a 12â€“18 page chapter once formatted

---

## 17) Final deliverables to return

Return the following:

1. `chapter_draft.md`
2. `article_evidence_matrix.csv`
3. `lengerke_web_matrix.csv`
4. `thesis_method_extraction.md`
5. `call_alignment.md`
6. `evidence_gaps.md`
7. the `/papers/` folder with downloaded articles

Also provide a concise final note stating:

- total number of Q1 papers downloaded,
- total number actually cited in the draft,
- any unresolved evidence gaps,
- any claim intentionally left out because it could not be verified.

---

## 18) Final warning

If you cannot verify something, exclude it.  
If you cannot download a paper, do not cite it.  
If the evidence is weak, say so explicitly.  
The priority is **auditability and scholarly credibility**, not rhetorical completeness.

