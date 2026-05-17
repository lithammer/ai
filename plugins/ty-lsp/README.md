# ty-lsp

A Claude Code plugin that wires [ty](https://github.com/astral-sh/ty) — Astral's
Rust-based Python type checker and language server — into Claude Code as a
native LSP server. Gives Claude real-time type diagnostics, go-to-definition,
references, and hover info on `.py` and `.pyi` files.

> ty is in beta. See [the announcement](https://astral.sh/blog/ty).

## Prerequisites

[`uv`](https://docs.astral.sh/uv/) must be on `PATH`. The plugin launches ty
via `uvx ty@latest server`, which fetches and caches ty on first use — no
separate install step.

```bash
brew install uv             # macOS
# or: curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Install

```
/plugin install ty-lsp@lithammer-ai
```

## Per-project tuning

Ships no `initializationOptions`. Configure ty per-project via `ty.toml` or the
`[tool.ty]` table in `pyproject.toml`. See
[ty configuration docs](https://docs.astral.sh/ty/reference/configuration/).
