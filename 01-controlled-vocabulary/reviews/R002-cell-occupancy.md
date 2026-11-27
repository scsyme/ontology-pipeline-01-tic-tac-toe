---
id: "R002"
status: "proposed"
reviewed_on: "2026-11-27"
term_ids:
  - "T005"
  - "T006"
source_ids:
  - "S001"
  - "S002"
  - "S003"
  - "S004"
  - "S005"
  - "S006"
---

# Wording for cell occupancy

Scott approved the cell definition and asked how the assistant's descriptions empty and occupied align with source terminology. Those two labels were assistant paraphrases in the conversation. The following is a proposed interpretation for review.

## Source coverage

| Source | Finding and scope |
| --- | --- |
| [S001](../sources/S001.md) | The instructions use filled for a space that cannot be used again. Captured in [T006](../terms/T006.md). |
| [S002](../sources/S002.md) | The retrieved article describes placement of pieces. Its conventional-game description supplies no explicit pair of occupancy labels. |
| [S003](../sources/S003.md) | Deferred, relevant original passage unavailable. |
| [S004](../sources/S004.md) | Direct access returned HTTP 403 again. The definition retrieved during R001 describes writing marks in nine squares and supplies no explicit occupancy labels. This finding relies on that earlier retrieved definition. |
| [S005](../sources/S005.md) | The occupied-location restriction uses filled, captured in T006. The API comment on page 1 uses zero initially and values 1 and -1 for X and O. Those numbers belong to the assignment's representation. |
| [S006](../sources/S006.md) | The opening paragraph uses vacant cell, captured in [T005](../terms/T005.md). It also uses filled for a row, column or diagonal, and fill for the grid. Those latter occurrences concern larger structures. |

## Proposed alignment

For an individual cell, vacant aligns with the assistant's empty and filled aligns with occupied. The comparison depends on what is being described. A filled winning line in S006 means every cell in that line bears the same player's symbol.

There are two useful levels of description. Occupancy asks whether a cell has a mark, giving two possibilities. Contents distinguishes no mark, X and O, giving three possibilities. Thus the earlier two-state description concerns occupancy and leaves the mark's identity unspecified.

Vacancy alone does not establish that a move is legal. The stopping-rule evidence in S005 and S006 includes games that end with unmarked cells remaining.

## Review decision

Vacant and filled are source-attested candidates. The preferred wording for occupancy remains open to Scott's selection. The proposed alignment and distinction between occupancy and contents are interpretations for review. The recorded source-access limitations remain applicable.
