---
name: hr-context
description: Build the HR context documents that make every future AI session and agent useful without re-explaining the company — a workspace map, AI usage rules, org basics, HR calendar, decision log, policies index, one document per HR process, and correction logs — assembled from everything already reachable (connected email, calendar, drives, wiki, HR tools, Effy AI knowledge and records, Claude's memory and past chats), confirmed in a short interview, and saved to Effy AI's knowledge or a shared folder. Use whenever someone wants AI to "know" their company's HR, says "set up HR context", "build context files", "stop re-explaining our company to Claude", "prepare our HR knowledge for agents", "organize HR docs for AI", or asks how to get better HR answers from AI, even if they don't say "context".
---

# Build the HR context for AI

Build a small set of documents that lets any future AI session — a chat, a project, an agent,
another skill in this plugin — start with the company's HR already understood: how it's
organised, when things happen, what's already decided, where the real documents live, and how
each HR process actually runs.

**Why it's built this way.** An AI's attention is limited, so the goal is the *smallest set of
high-signal information* that does the job, not everything you can find. Structure is part of the
instruction: document names, an index that says what lives where, and short documents with one
purpose each let the AI find the right thing without reading everything. And context is not
records — so explain this to the user in two or three lines at the start, in your own words,
because the natural assumption is that you're about to copy their HRIS:

- It holds **patterns, cadences, decisions and pointers** — how the company works, not who works
  there. Employee data stays in the HR system.
- Policies and templates are **linked, never copied**. There's one master of each document, and
  it isn't here.
- It's what lets every later AI session skip the "let me explain our company" part.

The document set, templates and rules are in `references/document-set.md` — read it before Step 3.

## Step 0 — Where it will live

Check what's connected, then recommend one home (the two can be combined):

- **Effy AI knowledge** — if the Effy AI connector is available, recommend this. Each document
  becomes a knowledge document that Effy's agents and the other skills in this plugin read
  automatically, so the context works in every session without anyone attaching files. If the
  user uses Effy but the connector isn't connected, say so in one line: it's added in Claude's
  connector settings with `https://go.effy.ai/mcp` (on Team or Enterprise plans an admin enables
  it).
- **A shared folder** — a connected local folder (suggest the name `HR-CONTEXT-FOR-AI`), a drive
  folder, or a wiki space. Use this when there's no Effy, or as well as Effy if the user wants
  files they can open.

Ask once which they want. If neither is available, say the documents will exist only in this chat
and they'll need to copy them out — then continue. Don't block on it.

## Step 1 — Read everything already reachable

Say in one sentence what you're about to search, then read before asking anything. Sources, in
rough order of yield:

- **What already exists as context.** Effy AI's knowledge documents (search for context, process,
  policy, handbook, onboarding, review), and any existing context folder or wiki space. Update
  what's there rather than duplicating it.
- **Claude's memory and past chats**, if this session has them — what the user has already said
  about the company, its processes, decisions and preferences. Treat it as the user's own account
  (good evidence), but confirm anything that may be stale.
- **Effy AI records**, if connected — the employee directory (size, teams, locations — counts and
  structure only), career tracks, growth-plan periods, 1-on-1 activity cadence, review reports.
- **Email and calendar** — recurring HR events (review cycles, surveys, comp reviews, all-hands),
  announcements, the last few hires and exits (for the process, not the people).
- **Drives and wikis** — handbook, policies, process docs, templates, offer letters, review forms.
- **HR, ATS, payroll and task tools** — which tools are used for what, and the processes visible in
  them (hiring stages, onboarding checklists).

Collect facts with their source. Weigh them: a document or a recurring calendar event beats a
one-off email; what the user said beats what you inferred; nothing beats nothing — never fill a
gap with what "companies like this usually do".

## Step 2 — Interview, then show the plan

Start with four or five lines on what you found and where. Then ask **only what the evidence
couldn't answer**, one question at a time, up to ten. Focus on:

- What the user owns versus delegates, and who owns each HR process.
- Decisions already made that AI should never reopen (e.g. contractors excluded from review cycles).
- Which processes cause the most work — those get a process document first.
- Anything you found that contradicts something else. Quote both, ask which is right.

Then **show the plan before building**: the list of documents, one line each on what it will say
and what it rests on, and which ones are new versus updates. Wait for a yes.

## Step 3 — Build the documents

Use the set and templates in `references/document-set.md`: the workspace map, the AI usage rules
pointer, `company/` facts, one `processes/` document per process actually run, and the two logs.
Build only what the evidence and interview support — a process the company doesn't run gets no
document, and a section with nothing real in it is left out, not padded.

Rules for every document:

- **Short and high-signal.** Under 2,000 words; most well under. Patterns, not raw notes.
- **Pointers, not copies** for policies, templates and anything with a master elsewhere.
- **No employee names**, ever — roles only. No salaries, ID numbers, health or personal details.
- **Mark every inferred line** `[CONFIRMED]` or `[GUESS: verify]`. Anything the user stated or a
  document shows is confirmed; anything you deduced is a guess until they check it.
- **Route content by type.** Company facts go in `company/`; how a process runs goes in
  `processes/`; methods and playbooks are skills, not context; reference documents stay where they
  are and get indexed; current-cycle evidence (exports, candidate files) belongs in a project for
  that job, not here.

Where a dedicated skill does a process better, say so and offer it rather than writing a thinner
version here: `onboarding-process` for onboarding, `hr-ai-usage-policy` for the AI rules,
`employee-handbook` for the handbook.

## Step 4 — Save

Show the final list of documents to be created or updated, then save after an explicit yes.

- **To Effy AI knowledge** — one knowledge document per document in the set, titled with its path
  so they sort and read as a workspace: `HR context — README`, `HR context — company/org-basics`,
  `HR context — processes/review-cycle`, and so on. Search first and update a matching document
  rather than creating a second. Logs are documents too, so corrections stay with the context.
- **To a folder** — the same set as markdown files in the structure from the reference, with a
  `README.md` in every folder.

Then add the first line to the context log: today's date, what was created.

## Step 5 — Optional extras

Offer each in one line; build only on a yes.

- **Project packs** — for each HR job the user runs (review cycle, handbook and policy, pay,
  hiring, onboarding, surveys, HR helpdesk), a pack to set up a dedicated AI project: its name, the
  instructions to paste, what to upload each cycle, and 3–5 facts for the project's memory. One
  room per job, never one giant "HR" project — mixed context degrades every task it touches.
- **Weekly context review** — a scheduled task that reads the logs and recent outputs and proposes
  fixes. The prompt is in the reference. It proposes; it never edits on its own.

## Finish

Two or three lines: what was created or updated and where, how many `[GUESS: verify]` lines are
waiting for the user, and the one process document most worth writing properly next. Remind them
of the habit that keeps this alive: when they correct the AI on something non-trivial, add a dated
line to the feedback log.
