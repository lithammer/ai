---
name: research-codebase
description: "Map how the code a ticket touches works today, then name the next step: develop or grill-with-docs."
disable-model-invocation: true
---

# Research codebase

Map the code a ticket touches as it stands, so the next step starts from
facts instead of finding them again. The map describes; the next step
decides, so every choice stays open for the user.

## 1. Frame the questions

Read the ticket and the files it names before dispatching anything. Turn the
ticket into questions about the current code: where the relevant parts live,
how data and control flow through them, which callers, tests, and
configuration depend on them, and which patterns nearby code follows. Each
question asks how the code works now.

When the ticket names no area of code to change, there is nothing to map yet:
route to `grill-with-docs` and stop.

## 2. Investigate

Dispatch a sub-agent for each independent question, so the main context
holds the questions and findings, not the reading. Each sub-agent returns
observations with `path:line`.

The step is done when every question has an answer backed by `path:line`, or
is marked open with the places searched.

## 3. Write the map

Write one Markdown file:

```markdown
# <topic>

Ticket: <reference>
Commit: <short sha>

## Questions

<numbered, as framed in step 1>

## Findings

<per question: what exists, where, how it works, how parts connect>

## Open

<questions the code did not answer, with the places searched>
```

Write every finding as an observation of the current code. A gap or quirk is
a fact with a location like any other.

The map describes one commit and goes stale as the change lands. Save it where
the repository keeps working notes for tasks; when it has none, under
`.research/` at the repository root, with `.research/` listed in
`.git/info/exclude` to keep it out of commits.

## 4. Route

Before naming the route, open the cited lines for each fact it rests on.
Reply with a short summary of the map, its path, and one route:

- **`develop`** when the ticket and the map leave one reasonable way to make
  the change: no open choice alters observable behavior or an interface.
- **`grill-with-docs`** when a choice remains that is the user's to make.
  List each choice in one line.

The user starts the next step, often in a fresh session given the map's path.
