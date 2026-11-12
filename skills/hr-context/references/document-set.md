# HR context — document set, templates and review prompt

Contents: 1. The set · 2. Templates · 3. Project pack · 4. Weekly review prompt

## 1. The set

```
HR-CONTEXT-FOR-AI/
├── README.md               Map of the workspace: what lives where, how to work here
├── ai-usage-policy.md      Rules, read before every task (pointer to the policy if it lives elsewhere)
├── company/
│   ├── README.md
│   ├── org-basics.md       Size, locations, teams, ownership, how decisions get made
│   ├── hr-calendar.md      Review cycles, survey cadence, comp review dates, planning
│   ├── decision-log.md     HR decisions with dates and reasons
│   └── policies-index.md   Pointers to policies where they live — never copies
├── processes/
│   ├── README.md
│   └── <one per process actually run>.md   e.g. review-cycle, hiring, onboarding
├── OUTPUTS/
│   └── README.md           Deliverables, one subfolder per project
└── logs/
    ├── README.md
    ├── context-log.md      What changed in the workspace, and when
    ├── feedback-log.md     What the AI got wrong, and what's true
    └── context-reviews/    Weekly review output, one file per review (YYYY-MM-DD.md)
```

Why each part exists:

- **READMEs** answer three questions: what lives here, when to read it, when to write here. An AI
  reads the top README first, then the folder README, then the file it needs.
- **`company/` vs `processes/`** — facts change rarely and are looked up often; processes are what
  the AI follows when working. Separating them keeps both short.
- **`policies-index`** keeps one source of truth for each policy.
- **`decision-log`** stops the AI reopening settled questions.
- **`logs/`** record changes and corrections, which feed the weekly review.

In Effy AI knowledge, each file becomes one knowledge document titled `HR context — <path>`
(e.g. `HR context — company/decision-log`). `OUTPUTS/` and `context-reviews/` stay in a folder if
the user has one; otherwise skip them.

## 2. Templates

Fill only what the evidence supports. Mark inferred lines `[CONFIRMED]` / `[GUESS: verify]`.

### README.md (top level)

```markdown
# HR context — <Company>

Context for AI sessions and agents working on <Company>'s HR. Read this first.

## What lives where
- `ai-usage-policy` — the rules. Read before every task.
- `company/` — facts that rarely change: org, calendar, decisions, where policies live.
- `processes/` — how each HR process actually runs. Follow these when doing the work.
- `logs/` — what changed and what the AI got wrong. Check `feedback-log` before repeating a task.

## How to work here
- Never put employee names, salaries or personal details in these documents.
- Link to policies and templates; never copy them.
- If something here contradicts what you find elsewhere, say so — don't silently pick one.

Owner: <role>. Last updated: <date>.
```

### Folder README (company/, processes/, logs/)

```markdown
# <folder>

What lives here: <one line>.
Read it when: <one line>.
Write here when: <one line>.
```

### company/org-basics.md

```markdown
# Org basics

- Headcount: <n, as of date> [CONFIRMED]
- Locations / countries with employees: <…>
- Entities or employer-of-record: <…>
- Teams and reporting lines: <functions, heads by role>
- Ownership and stage: <bootstrapped / VC-backed / …>
- How decisions get made and communicated: <…>
- Tools — source of truth for what: <HRIS, payroll, ATS, reviews, chat, docs>
- HR team: <roles; who owns which process>
```

### company/hr-calendar.md

```markdown
# HR calendar

| When | What | Owner | Notes |
| --- | --- | --- | --- |
| <Jan–Feb> | <Annual review cycle> | <HR lead> | <self → manager → calibration> |
| <Quarterly> | <Engagement pulse> | … | … |
```

### company/decision-log.md

```markdown
# Decision log

Settled decisions. Don't reopen these without the owner.

- <YYYY-MM-DD> — <decision>. Why: <reason>. Owner: <role>.
```

Example: `2026-03-02 — Contractors are excluded from review cycles. Why: no line manager and
fixed-scope contracts. Owner: Head of People.`

### company/policies-index.md

```markdown
# Policies index

| Policy | Where it lives (link) | Owner | Last reviewed |
| --- | --- | --- | --- |
| Employee handbook | <link> | <role> | <date> |
```

### processes/<process>.md

```markdown
# <Process> — how it actually runs

Trigger: <what starts it>. Owner: <role>. Cadence: <…>. Tools: <…>.

## Steps
1. <timing> — <owner> — <action> [CONFIRMED]
2. …

## Inputs and templates
- <name> — <link>

## Where it usually goes wrong
- <evidence-backed point>

## Decisions that apply
- See decision-log: <entry>
```

### logs/context-log.md

```markdown
# Context log

- <YYYY-MM-DD> — <what changed in the workspace>.
```

### logs/feedback-log.md

```markdown
# Feedback log

One dated line per non-trivial correction: what the AI got wrong, and what's true.

- <YYYY-MM-DD> — Said the review cycle runs in January. True: it runs in July. Fix: hr-calendar.
```

## 3. Project pack

```markdown
# Project pack — <job, e.g. Review Cycle>

Project name: <…>
Instructions to paste: <job-specific rules, e.g. "Remove names before analysis", "Answer only from the named policies">
Upload each cycle: <current evidence: exports, forms, candidate files>
Facts for project memory (3–5): <rating scale; cycle timing; who calibrates; …>
```

Rooms to offer, only for jobs the user actually runs: Review Cycle, Handbook & Policy, Pay,
Hiring, Onboarding, Surveys, HR Helpdesk.

## 4. Weekly review prompt

For a scheduled weekly task (in the Claude desktop app: Settings → Scheduled tasks → New):

```
Review the HR context workspace.
1. Read the READMEs and work from the actual structure.
2. Find the last review in logs/context-reviews/ and cover the period since then — or the last
   7 days if there is none.
3. Read the feedback log, the context log, new deliverables in OUTPUTS/, the context documents,
   and relevant email and calendar for the period.
4. Answer four questions in under 400 words:
   - Corrections: what was corrected, and which document should have prevented it.
   - Gaps: up to 5, ranked by what they cost.
   - Drift: where a document no longer matches reality — quote both sides.
   - Bloat: documents over 2,000 words, or never referenced.
Propose edits with exact wording; don't make them. "Nothing this week" is a valid answer.
No employee names. Save as logs/context-reviews/YYYY-MM-DD.md.
```

The review can't see past conversations unless the session has memory or chat search, so
corrections only count once they're in the feedback log.
