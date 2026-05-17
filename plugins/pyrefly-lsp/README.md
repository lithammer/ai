# pyrefly-lsp

A Claude Code plugin that wires [Pyrefly](https://github.com/facebook/pyrefly) —
Meta's Rust-based Python type checker and language server — into Claude Code as
a native LSP server. Gives Claude real-time type diagnostics, go-to-definition,
references, and hover info on `.py` and `.pyi` files.

## Prerequisites

[`uv`](https://docs.astral.sh/uv/) must be on `PATH`. The plugin launches
Pyrefly via `uvx pyrefly@latest lsp`, which fetches and caches Pyrefly on first
use — no separate install step.

```bash
brew install uv             # macOS
# or: curl -LsSf https://astral.sh/uv/install.sh | sh
```

> The LSP binary runs in an isolated `uvx` cache, not your project's `.venv`.
> Pyrefly still resolves third-party imports against the workspace's configured
> Python interpreter, so type checking against your project's deps works as
> expected.

## Install

```
/plugin install pyrefly-lsp@lithammer-ai
```

## Per-project tuning

Ships no `initializationOptions`. Configure Pyrefly per-project via
`pyrefly.toml` or the `[tool.pyrefly]` table in `pyproject.toml`. See
[Pyrefly configuration docs](https://pyrefly.org/en/docs/configuration/).
