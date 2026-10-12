# HTML report

Render the ranked candidates as one self-contained HTML file. Write it to
`$TMPDIR`, falling back to `/tmp`, as `refactor-<repo>-<timestamp>.html`,
so nothing lands in the repository and each run gets a fresh file. Open it
with `xdg-open` or `open`.

The diagrams show each proposal; the step 4 fields carry its evidence. Keep
every field complete, written as short labelled lists.

## Layout

- **Header:** repository, commit, scope, a legend for the diagram marks,
  and the ranked candidate titles linking to their cards.
- **One card per candidate,** in rank order:
  1. A title naming the move, such as "Let `Checkout` own the paid-state
     invariant".
  2. Badges: expected size, and the step 2 questions that surfaced it.
  3. The before/after diagrams, side by side.
  4. The step 4 fields, with evidence as a monospace `path:line` list.
  5. An amber callout for each change to accepted external behavior.
- **Coverage:** what you explored and what remains unread.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Refactor candidates: {repo}</title>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true, theme: "neutral" });
</script>
<style>
  :root { --ink: #1c1917; --muted: #78716c; --line: #e7e5e4; --warn: #b45309; }
  body { margin: 0; background: #fafaf9; color: var(--ink); font: 16px/1.5 system-ui, sans-serif; }
  main { max-width: 64rem; margin: 0 auto; padding: 3rem 1rem; }
  h1, h2 { font-family: Georgia, serif; }
  article { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 1.5rem; margin: 2.5rem 0; }
  .badge { display: inline-block; padding: 0 .5rem; border-radius: 999px; background: var(--line); font-size: .75rem; text-transform: uppercase; letter-spacing: .05em; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; }
  .pair figure { margin: 0; padding: 1rem; border: 1px solid var(--line); border-radius: 6px; }
  .pair figcaption { color: var(--muted); font-size: .75rem; text-transform: uppercase; letter-spacing: .05em; }
  code, .evidence { font-family: ui-monospace, monospace; font-size: .9em; }
  .callout { border-left: 4px solid var(--warn); background: #fffbeb; padding: .5rem 1rem; }
  @media (max-width: 48rem) { .pair { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<main>
  <header>…</header>
  <article id="c1">
    <h2>1. Let <code>Checkout</code> own the paid-state invariant</h2>
    <p><span class="badge">small</span> <span class="badge">Invariant ownership</span></p>
    <div class="pair">
      <figure><figcaption>Before</figcaption><pre class="mermaid">…</pre></figure>
      <figure><figcaption>After</figcaption><pre class="mermaid">…</pre></figure>
    </div>
    <ul class="evidence">…</ul>
    …
    <p class="callout">…</p>
  </article>
  <section id="coverage">…</section>
</main>
</body>
</html>
```

## Diagrams

Draw before and after with the same node names and positions, so the eye
catches what moved. In the before diagram, mark the burden red: each
caller's repeated check, release, or sync. In the after diagram, draw its
owner as one heavy box and leave the callers bare. When a diagram needs a
paragraph to read, redraw it.

```text
flowchart LR
  api["api/pay.go"] --> paid{"paid?"}
  job["jobs/refund.go"] --> paid2{"paid?"}
  class paid,paid2 burden
  classDef burden stroke:#dc2626,stroke-width:2px

flowchart LR
  api["api/pay.go"] --> co["Checkout"]
  job["jobs/refund.go"] --> co
  class co owner
  classDef owner stroke:#1c1917,stroke-width:4px
```

Pick the shape from the burden; the step 2 question is a hint:

| Question | Before → after |
|---|---|
| Invariant ownership | Flowchart: callers each checking the rule → callers pointing at the one owner |
| Lifecycle ownership | Sequence: each caller acquires, uses, and releases → one scoped call |
| Representation | Code side by side: primitive, flags, and naming convention → one type |
| Derivability | Flowchart: two stores joined by a red sync edge → one source and a derived view |
| Least capability | The wide handle with unused methods greyed → the narrow handle the caller needs |
| Altitude | Special cases stacked in callers → the rule inside the mechanism that lacked it |
| Deep modules | Nested call boxes → one box, the now-internal calls faded inside |

Reach for inline SVG when Mermaid's layout fights the point, such as faded
internals inside one heavy box.

Mermaid draws a syntax error in place of the diagram, so quote every
flowchart node label (`a["Cart.total()"]`), and write `<`, `>`, and `"`
inside labels as `#lt;`, `#gt;`, and `#quot;`.
