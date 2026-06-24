# Concept Set Editor — Design Document

## Overview

A standalone versioned concept set editor for OHDSI/OMOP clinical research. Addresses a gap in OHDSI Atlas: Atlas has no native versioning, provenance, or review workflow. This tool wraps the standard OHDSI concept set JSON expression with version control, curation metadata, and a structured reviewer approval process — while remaining fully interoperable with Atlas (import/export).

**GitHub:** https://github.com/stephanieshong/concept-set-editor  
**Tech stack:** See [architecure.md](./architecure.md)  
**OHDSI concept set schema:** https://raw.githubusercontent.com/ohdsi/tab/main/docs/schemas/concept-set-schema.json

---

## Pages / Navigation

The app has two main views:

1. **Browse UI** — library of all concept sets and their versions
2. **Edit/Diff View** — create or edit a draft version with live comparison

---

## 1. Browse UI (Library View)

### Level 1 — Concept Set Library

Displays all named concept sets with search and filter.

| Column | Notes |
|---|---|
| Concept Set Name | Clickable, drills to Level 2 |
| Domain | Drug / Condition / Measurement / etc. |
| # Versions | Count of all versions (draft + final) |
| Latest Status | Badge: Draft / In Review / Final |

- Search bar by name
- Filter by Domain, Status
- Click a row → opens Level 2 version history

### Level 2 — Version History (one concept set)

Displays all versions under a named concept set.

| Column | Notes |
|---|---|
| Version # | Assigned only at finalization; blank for drafts |
| Version Name | Descriptive label e.g. "Mono Therapy Only" |
| Status | 📝 Draft \| 🔍 In Review \| ✅ Final |
| Based On | Which finalized version it branched from |
| Author | Free-text name (Phase 1) |
| Date | created_at |

- Finalized versions listed first, drafts below
- Per-row actions: **[View]** **[Compare]**
- **[+ New Version]** button → opens branch selector → navigates to Edit/Diff View

---

## 2. Version Lifecycle

```
DRAFT ──────────────► IN REVIEW ──────────────► FINAL
  ▲                       │                    (immutable)
  │     (any reviewer     │
  └─────  rejects)  ──────┘
         with notes
```

| State | Editable | Version # |
|---|---|---|
| Draft | Yes, by author | Not yet assigned |
| In Review | No (reviewer adds notes only) | Not yet assigned |
| Final | Never | Assigned at approval |

- **Multiple drafts** of the same concept set can exist simultaneously
- **To modify a Final version:** create a new draft branching from any prior finalized version
- **Version numbers** assigned only at finalization to avoid numbering conflicts between parallel drafts
- For v2: only v1 is available as branch source. For v3+: any prior finalized version is available.

---

## 3. Edit / Diff View

### Layout

```
┌──────────────────────┬────────────────────────────────────────┐
│  METADATA PANEL      │                                        │
│  (collapsible)       │        Venn Diagram (live)             │
│                      │                                        │
│  Version Name*       ├────────────────────────────────────────┤
│  Based on: v1 🔒     │                                        │
│  Rationale*          │   Concept Hierarchy Diff Tree          │
│  Scope Notes         │                                        │
│  Author*             │   Diabetes mellitus       ⬜ both      │
│  Reviewers*          │     Type 2 diabetes       ⬜ both      │
│  + Add Reviewer      │     Insulin-dep DM   🔵  [+ Add]      │
│  Study ID            │     Drug-induced DM  🟢  [- Remove]   │
│                      │                                        │
│  [Save Draft]        │   🔍 Search to add new concept...      │
│  [Submit for Review] │                                        │
└──────────────────────┴────────────────────────────────────────┘
```

# Concept Set Editor Layout

| Metadata Panel (Collapsible) | Concept Set Visualization       |
| ---------------------------- | ------------------------------- |
| **Version Name***            | **Venn Diagram (Live Preview)** |
| Based on: `v1` 🔒            |                                 |
| **Rationale***               |                                 |
| Scope Notes                  |                                 |
| **Author***                  |                                 |
| **Reviewers***               |                                 |
| + Add Reviewer               |                                 |
| Study ID                     |                                 |
| **Actions**                  |                                 |
| [Save Draft]                 |                                 |
| [Submit for Review]          |                                 |

---

## Concept Hierarchy Diff Tree

```text
Diabetes mellitus                    ⬜ both
├── Type 2 diabetes                  ⬜ both
├── Insulin-dependent diabetes       🔵 [+ Add]
└── Drug-induced diabetes            🟢 [- Remove]
```

### Search and Add Concepts

```text
🔍 Search to add new concept...
```

### Legend

| Icon       | Meaning                                  |
| ---------- | ---------------------------------------- |
| ⬜          | Present in both concept sets             |
| 🔵         | New concept added in current version     |
| 🟢         | Concept removed from current version     |
| 🔒         | Read-only / inherited from prior version |
| [+ Add]    | Include concept in concept set           |
| [- Remove] | Exclude concept from concept set         |

```
```

- Metadata panel **collapses** to give full width to Venn + diff tree during editing
- Venn diagram updates **live** as concepts are added/removed

### Metadata Panel Fields

| Field | Required to submit? | Notes |
|---|---|---|
| Version Name | Yes | Descriptive e.g. "ACE Inhibitors Mono Therapy" |
| Based On | Locked | Set at draft creation, cannot change |
| Rationale | Yes | Why this version was created |
| Scope Notes | No | Constraints, limitations |
| Author Name | Yes | Free-text in Phase 1 |
| Reviewers | Yes (≥1) | Each has: Name, Email, Role |
| Study ID | No | Optional research study linkage |

### Venn Diagram (top of right panel)

- Shows **overlap magnitude**: A only | shared | B only (with counts)
- Defaults to comparing current draft vs. its parent version
- **Version picker** to override and compare any two versions
- Updates live as user edits

### Concept Hierarchy Diff Tree (below Venn)

Built from OMOP `concept_ancestor` table. Differences cluster under parent concept nodes.

| Color | Meaning | Action button |
|---|---|---|
| 🔵 Blue | In left/parent version only | [+ Add to draft] |
| 🟢 Green | In draft only | [- Remove] |
| ⬜ Neutral | In both versions | [- Remove from draft] |
| 🟡 Amber | In both but a flag changed (e.g. includeDescendants toggled) | — |


- Each `[+ Add]` / `[- Remove]` click updates Venn instantly via clientside callback (no server round-trip)
### Search and Add Concepts

```text
🔍 Search to add new concept...
```
---

## 4. Reviewer Workflow

- Author assigns **1 or more reviewers** when submitting for review
- Each reviewer has: **Name** (free-text), **Email**, **Role** (SME / Informatician / Clinician / Domain Expert)
- **ALL assigned reviewers must approve** before version moves to Final
- Any single rejection → version returns to Draft; rejection notes visible to author
- Author may be listed as a reviewer (no hard block) but a warning is shown: *"Author and reviewer are the same person — independent review recommended"*

### Email Notifications

| Trigger | Recipients |
|---|---|
| Author submits for review | All assigned reviewers |
| Reviewer approves | Author |
| Reviewer rejects | Author |

---

## 5. Import / Export

### Import — Option A: Atlas JSON File Upload

1. User exports concept set from OHDSI Atlas
2. Uploads `.json` file to this tool
3. Tool parses OHDSI-compliant JSON → creates Draft v1

### Import — Option B: Zenodo DOI

1. User pastes a Zenodo DOI (e.g. `10.5281/zenodo.XXXXXXX`)
2. Tool fetches JSON via Zenodo public REST API (no authentication needed):
   ```
   GET https://zenodo.org/api/records/{record_id}
   ```
3. Parses OHDSI-compliant concept set JSON → creates new draft (v1 or branch from existing version)
4. Source DOI stored on the imported version

### Export

- Any version can be exported as Atlas-compatible OHDSI JSON
- The `ohdsi_expression` stored per version is the exact round-trippable JSON blob
- Our provenance metadata is placed in the OHDSI `metadata` extension field (see JSON format below)

---

## 6. OHDSI JSON Format & Provenance Strategy

The exported JSON is **fully OHDSI-schema-compliant** per the TAB specification.  
Our provenance layer uses the official OHDSI `metadata` extension field — no custom fields break the schema.

```json
{
  "id": 2,
  "name": "ACE Inhibitors",
  "version": "2.0.0",
  "description": "ACE inhibitor ingredients approved for use in the US",
  "createdBy": "Jane Smith",
  "createdDate": "2026-06-24T00:00:00Z",
  "createdByTool": "concept-set-editor v1.0",
  "modifiedByTool": "concept-set-editor v1.0",
  "tags": ["cardiovascular", "mono-therapy"],

  "metadata": {
    "rationale": "Excludes combination therapy products",
    "scope_notes": "Mono therapy only — combination drugs removed",
    "research_study_id": "R01-HL-XXXXX",
    "parent_version": "1.0.0",
    "reviewers": [
      {"name": "John Doe",  "email": "john@institution.edu", "role": "SME",          "decision": "approved"},
      {"name": "Mary Lee",  "email": "mary@institution.edu", "role": "Informatician", "decision": "approved"}
    ]
  },

  "expression": {
    "items": [
      {
        "concept": {
          "conceptId": 1308216,
          "conceptName": "lisinopril",
          "domainId": "Drug",
          "vocabularyId": "RxNorm",
          "conceptClassId": "Ingredient",
          "standardConcept": "S",
          "conceptCode": "29046",
          "invalidReason": null
        },
        "isExcluded": false,
        "includeDescendants": true,
        "includeMapped": false
      }
    ]
  }
}
```

**Field constraints (from OHDSI schema):**
- `standardConcept`: `"S"` (Standard), `"C"` (Classification), or `null` only
- `invalidReason`: `"D"` (deleted), `"U"` (updated), or `null` only
- `version` uses semver format `"X.0.0"` mapped from our integer version number

---

## 7. Database Schema

Informed by the N3C Palantir Foundry concept set editor implementation.  
Reference tables: `concept_set_members`, `code_sets`, `zenodo_doi` (N3C).

### `concept_set`

| Column | Type | Notes |
|---|---|---|
| id | INT PK | Surrogate key |
| concept_set_name | VARCHAR UNIQUE | Logical identifier e.g. "ACE Inhibitors" |
| description | TEXT | |
| domain_id | VARCHAR | Drug / Condition / etc. |
| project_id | VARCHAR | Optional project linkage |
| doi | VARCHAR | Zenodo DOI; set on import or after publishing |
| created_by | VARCHAR | |
| created_at | TIMESTAMP | |
| modified_at | TIMESTAMP | |

### `concept_set_version`

| Column | Type | Notes |
|---|---|---|
| version_id | INT PK | Integer version identifier |
| concept_set_id | FK → concept_set.id | |
| version_number | INT NULLABLE | Assigned at finalization only |
| version_name | VARCHAR | Descriptive label |
| status | VARCHAR | `draft` / `in_review` / `final` |
| parent_version_id | FK → self | Which finalized version this branched from |
| ohdsi_expression | JSON | Full Atlas-compatible JSON blob |
| rationale | TEXT | Why this version was created |
| scope_notes | TEXT | Constraints / limitations |
| author_name | VARCHAR | Free-text in Phase 1 |
| research_study_id | VARCHAR | Optional |
| created_at | TIMESTAMP | |
| modified_at | TIMESTAMP | |

### `reviewer`

| Column | Type | Notes |
|---|---|---|
| id | INT PK | |
| version_id | FK → concept_set_version.version_id | |
| name | VARCHAR | Free-text in Phase 1 |
| email | VARCHAR | Used for notifications |
| role | VARCHAR | SME / Informatician / Clinician / Domain Expert |
| decision | VARCHAR | `pending` / `approved` / `rejected` |
| notes | TEXT | Visible to author on rejection |
| decided_at | TIMESTAMP | |

### `concept_set_member`

Follows the exact OHDSI TAB concept set schema (snake_case in DB, camelCase in JSON).

| Column | Type | Required | Source |
|---|---|---|---|
| id | INT PK | | |
| version_id | FK | | |
| concept_id | INT | Yes | OHDSI `conceptId` |
| concept_name | VARCHAR(255) | No | OHDSI `conceptName` |
| domain_id | VARCHAR(20) | No | OHDSI `domainId` |
| vocabulary_id | VARCHAR(20) | No | OHDSI `vocabularyId` |
| concept_class_id | VARCHAR(20) | No | OHDSI `conceptClassId` |
| standard_concept | VARCHAR | No | OHDSI `standardConcept` — enum: `"S"`, `"C"`, `null` |
| concept_code | VARCHAR(50) | No | OHDSI `conceptCode` (e.g. ICD10 source code) |
| valid_start_date | DATE | No | OHDSI `validStartDate` |
| valid_end_date | DATE | No | OHDSI `validEndDate` |
| invalid_reason | VARCHAR | No | OHDSI `invalidReason` — enum: `"D"`, `"U"`, `null` |
| is_excluded | BOOLEAN | Yes | OHDSI `isExcluded` |
| include_descendants | BOOLEAN | Yes | OHDSI `includeDescendants` |
| include_mapped | BOOLEAN | Yes | OHDSI `includeMapped` |
| descendant_count | INT NULLABLE | No | N3C addition; Phase 2 via WebAPI |
| review_status | VARCHAR | No | N3C/curation; member-level review flag |
| review_comment | TEXT | No | N3C/curation; reviewer comment on specific concept |
| created_by | VARCHAR | No | |
| created_at | TIMESTAMP | No | |
| modified_at | TIMESTAMP | No | |

---

## 8. N3C Alignment

This tool is modeled after the N3C concept set curation workflow built in Palantir Foundry.

| N3C Metadata Field | Our Design |
|---|---|
| Concept Set Name | `concept_set.concept_set_name` |
| Concept Set ID | `concept_set.id` (surrogate) |
| Version | `concept_set_version.version_number` |
| Status | `concept_set_version.status` |
| SME | `reviewer` row with `role = "SME"` |
| Informatician | `reviewer` row with `role = "Informatician"` |
| DOI | `concept_set.doi` |
| Description | `concept_set.description` |
| Project | `concept_set.project_id` |

| N3C Member Field | Our DB Column |
|---|---|
| Concept ID | `concept_id` |
| Concept Name | `concept_name` |
| Domain | `domain_id` |
| Vocabulary | `vocabulary_id` |
| Standard Concept | `standard_concept` |
| Excluded | `is_excluded` |
| Descendants | `include_descendants` |
| Mapped | `include_mapped` |
| Descendant Count | `descendant_count` |

---

## 9. Concept Set Size Considerations

From the OHDSI Phenotype Library (1,104 cohort definitions, 3,161 concept sets):

| Metric | Value |
|---|---|
| Median authored items per set | 3 |
| p90 | 45 |
| p99 | 285 |
| Max | 4,650 |
| % with includeDescendants | 29% → resolved counts 10–100x larger |
| % with isExcluded | 17% — "branch minus exceptions" is common |

The UI must handle both tiny (median = 3) and very large (resolved potentially 50,000+) concept sets. This is why Dash with `dash-cytoscape` (GPU-composited) and clientside callbacks (no server round-trip on node click) was chosen over Streamlit.

---

## 10. Phase 2 Items (Deferred)

- **User login / authentication** — replace free-text author/reviewer with real accounts; enforce reviewer ≠ author
- **Role-based permissions** — read-only vs. edit per concept set
- **WebAPI integration** — show record counts per concept (like Atlas "Included Concepts" tab); connects to institution's OHDSI WebAPI instance
- **Configuration settings UI tab** — admin UI to manage WebAPI URL, auth type, CDM source key (Phase 1 uses `.env` file)
- **Zenodo publishing workflow** — submit finalized concept set to Zenodo and store returned DOI (import FROM Zenodo is Phase 1; publishing TO Zenodo is Phase 2)
- **`descendant_count` population** — via WebAPI `/conceptset/{id}/resolve`
- **Multi-institution support**
- **Audit trail** wired to real user accounts
