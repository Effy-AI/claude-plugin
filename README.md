# Effy AI · HR

Fifteen HR skills for people leaders and managers at companies of roughly 30 to 1,000 people:
onboarding, the employee handbook, an AI usage policy, 1-on-1s, performance reviews, career
frameworks, growth plans, goal audits and people analytics.

Each skill works from your company's own records — the email, calendar, documents, meeting
notes and HR tools you have connected to Claude — and asks you for what it can't find. Nothing
is invented: facts come from your data or your answers, and gaps are marked as gaps.

The skills work with any connected tools. If you also connect [Effy AI](https://effy.ai), they
read your employee directory, 1-on-1s, growth plans, career tracks and review reports there,
and can save results back to Effy after you approve them.

Built by [Effy AI](https://effy.ai).

## Skills

### Onboarding and policies

| Skill | What it does |
| --- | --- |
| `onboarding-process` | Works out how onboarding actually runs from email, calendar, task tools and a short interview, then writes it up as a checklist per owner: HR, hiring manager, buddy, IT, new hire. |
| `onboarding-plan` | Applies your documented onboarding process to one new hire: a task list with one owner and a date each, welcome email, first-week schedule, draft 30/60/90. Pushes it to your tools after you approve. If no process document exists, it offers to run `onboarding-process` first. |
| `employee-handbook` | Researches the company and interviews you, then writes a first usable handbook — every fact sourced, every gap marked, legal sections flagged per country. |
| `hr-ai-usage-policy` | Writes a one-page AI usage policy for the HR team, aligned with your existing policies and with where your employees and candidates are based. |
| `hr-context` | Sets up the company context future AI sessions run on: org basics, HR calendar, decision log, policies index, one file per HR process. |

### 1-on-1s

| Skill | What it does |
| --- | --- |
| `one-on-one-prep` | Prepares a manager for one 1-on-1: where things stand, open items, what to discuss, 4–6 questions, feedback in situation–behaviour–impact form. |
| `one-on-one-debrief` | Turns a recording, transcript or rough notes into structured notes: what was discussed, decided, and who owes what by when. |
| `one-on-one-analysis` | Reads months of 1-on-1s across a team and surfaces recurring topics, broken commitments, signals worth attention and coverage gaps. |

### Performance and growth

| Skill | What it does |
| --- | --- |
| `review-draft` | Drafts a self, manager, upward or peer review from your own meetings and tools, every claim cited. |
| `review-cycle-analysis` | Turns a review cycle's data into one calibration-ready report: rating patterns per manager, ratings without evidence, company-wide themes, comparison with last cycle. |
| `review-form-audit` | Audits your review forms against last cycle's answers and rewrites the questions. Includes a Python script that computes answer statistics from a CSV export. |
| `career-framework` | Builds or changes career tracks, levels and the competency matrix, and proposes who sits on which level. Every change is shown as a diff before anything is written. |
| `growth-plan` | Drafts a growth plan for one person from their career level, reviews, 1-on-1s and goals. |
| `goal-system-audit` | Audits how goals are set, scored and updated from your own trackers and review comments, and proposes what to change first. |
| `people-analytics-dashboard` | Builds a dashboard — headcount, attrition, engagement, performance, pay equity and more — with the formula under every chart. Builds a labelled sample if you have no data yet. |

Skills trigger from what you ask ("prep my 1:1 with Maria", "build a growth plan for Tom"), or
run one by name, for example `/effy-ai:onboarding-plan`.

## What the plugin reads and writes

This section lists everything the skills do outside the conversation.

**Reads.** Only through tools you have connected to Claude yourself: email, calendar, documents
and drives, meeting notes and transcripts, chat, task trackers, HR and review tools, and Effy AI — plus Claude's own memory and past chats, where your plan has them.
The skills say what they're about to search before searching. Several use web search for public
information about your company (its website, careers page, public profiles).

**Writes — only after you approve the exact content:**

- **Effy AI**, if connected:
  - knowledge documents — the onboarding process, employee handbook, AI usage policy and HR
    context files;
  - growth plans — from `growth-plan`, and a new hire's 30/60/90 from
    `onboarding-plan`, always created as **Draft**, which Effy keeps hidden from the employee;
  - 1-on-1 notes — from `one-on-one-debrief`. Effy shares these with both participants, and the
    skill tells you so before saving;
  - career tracks, levels, competencies and level assignments — from `career-framework`.
- **Your other tools**, if you ask: a document or page in your wiki or drive; tasks, calendar
  invites and document copies from `onboarding-plan`.

The skills never send email or messages, submit reviews, change a growth plan's status or
access, or contact employees on your behalf. The plugin has no server of its own and sends
data nowhere except the tools you connected.

## Requirements

- Claude with skills enabled (claude.ai, Claude Desktop, or Claude Code).
- Connected tools are optional but make the output specific to your company. Effy AI is
  optional; without it, every skill still runs and delivers its result as a document,
  spreadsheet or page.
- `review-form-audit` runs a Python script and needs Python 3 with pandas.

## Limits

These skills are not legal, tax or compensation advice. Sections that depend on employment or
data-protection law are marked for review by a qualified person, and no skill recommends pay
amounts. Flags about people — attrition risk, rating patterns, disengagement — are signals for
a human to look into, not conclusions.

## License

MIT — see [LICENSE](LICENSE).
