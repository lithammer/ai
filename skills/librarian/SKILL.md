---
name: librarian
description: Clone or refresh a remote git repository into a shared local cache and return its path, so the source can be read with ordinary file tools instead of over the web. Use before cloning a repository yourself, before fetching repository files over the web, when a dependency's or upstream project's implementation needs reading, or when a repository URL or `owner/repo` reference names code the task must look at. Not for the repository already checked out as the working directory, nor for pull request or issue metadata that `gh` answers without a checkout.
---

# Librarian

Resolve the repository to a cached checkout, then search and read it with
ordinary file tools. `checkout.sh` sits in this skill's directory; run it from
there:

```bash
bash <skill-dir>/checkout.sh <repo>
```

`<repo>` is any reference to the repository: `owner/repo`, `host/org/repo`, an
HTTPS or SSH URL, or a deep link to a file, tree, or pull request. The command
prints the checkout path, cloning on first use and fast-forwarding a stale
checkout, so re-running it for a repository already resolved is cheap — call it
again rather than holding on to a path from earlier in the session.

Add `--force-update` when the checkout must reflect commits pushed minutes ago;
refreshes are throttled to five minutes otherwise.

A warning on stderr means the checkout could not be fast-forwarded and may be
behind origin. The path it prints is still the one to read.

## Working in a checkout

Checkouts live under `~/.cache/checkouts/<host>/<org>/<repo>` and are shared
across every session and task, so treat one as read-only. When a task needs to
modify the source, copy the checkout or add a worktree elsewhere and work there,
leaving a clean tree that the next fetch can fast-forward.
