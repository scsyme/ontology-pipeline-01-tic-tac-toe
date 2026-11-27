# Reading Stage 1 of the Ontology Pipeline

Reviewed 2026-11-25 against Jessica Talisman’s [Ontology Pipeline Studio](https://jesstalisman-ia.github.io/ontology-pipeline/), specifically Stage 1, sections 1–3, and the Studio guide. The evidence here comes from the published interface. The book itself was outside this reading.

## What Stage 1 asks us to do

First identify the decision the vocabulary will support and set its boundaries. Then identify where people use language relevant to that decision. Only then does the Studio invite candidate terms. Its guide connects terms to provenance and calls for definitions that identify a broader category and the feature that distinguishes the concept within it. The eventual vocabulary gives each concept a preferred term and can retain alternative labels. The style guide is optional. The chapter ends with a checklist. [Studio, Stage 1 and Guide](https://jesstalisman-ia.github.io/ontology-pipeline/)

For this experiment, the [proposed question about legal moves](../README.md#first-competency-question-proposed) gives source selection a practical test. A source might name the game accurately yet say too little about when play ends to support a decision about the next move. Its usefulness depends on the question we ask of it.

## Reading the three source fields

| Studio field | Evidence in Stage 1, section 2 | Our interpretation |
| --- | --- | --- |
| Source | The example names an engineering wiki. | Identify the particular resource or collection supplying the language. |
| System | The example gives Confluence alongside the wiki. | Identify the platform or environment where that source is maintained or encountered. A publisher identifies who issued a resource. A URL locates it. Neither alone reliably identifies its system. |
| Kind | The prompt gives content, search log, interview, standard and schema as examples. | Describe what sort of evidence supplies the language. A search log can show what people type, while a standard can show prescribed usage. Either could be held in the same system. |

These readings follow the examples in the [Studio source-entry panel](https://jesstalisman-ia.github.io/ontology-pipeline/). The panel leaves open how finely to name a system, what to record for a printed work, and whether a project should impose a closed list of kinds.

## Applying the distinction to our register

Consider [S005, the MIT OpenCourseWare assignment](sources/S005.md). The assignment is the resource. MIT OpenCourseWare is a plausible system because it is the identifiable collection through which we access the assignment. The assignment supplies instructional content. PDF describes its delivery format. “Content” and the more specific “programming assignment” would answer the kind question at different levels of detail. Choosing the useful level is a local decision.

[S003, the deferred book](sources/S003.md), tests the limits of that reading. We have a bibliographic reference but have yet to verify the relevant passage or record how we accessed it. Assigning a system from the author names would invent provenance.

## Experiment decision, 2026-11-25

Record the source genre in a required `kind` field on each atomic source record. Use a short, specific label and reuse it for other sources of the same kind. The labels are local editorial judgements and the list is open. For example, the dictionary entry in S004 can help with naming, while the programming assignment in S005 can help with move restrictions. The selection rationale explains why each item matters to our question. S003 can be identified as a book from its citation while its passage remains unverified.

Whether a separate `system` field improves traceability remains open.

## Concept-by-concept comparison, 2026-11-27

For each suspected concept, assess every agreed source before proposing a grouping. Record source wording and passage locators in atomic candidate-term files. Repeated wording adds evidence to its existing record. Record access gaps, scope differences and absence of relevant wording in the concept review. Then compare referents and test substitutions in context. Equivalence is a review conclusion. Apply this approach to future comparisons as well as the board-location trial.
