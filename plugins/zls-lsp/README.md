# zls-lsp

A Claude Code plugin that wires [ZLS](https://github.com/zigtools/zls) — the
Zig Language Server — into Claude Code as a native LSP server. Gives Claude
real-time diagnostics, go-to-definition, references, and hover info on `.zig`
and `.zon` files.

## Prerequisites

`zls` must be on `PATH`:

```bash
brew install zls            # macOS
# or build from source: https://github.com/zigtools/zls
```

## Install

```
/plugin install zls-lsp@lithammer-ai
```

## Per-project tuning

The plugin intentionally ships no `initializationOptions` — all ZLS knobs are
deferred to the project's own [`zls.json`](https://zigtools.org/zls/configure/zls-json/).
Run `zls env` to find where it lives. The toggle most often worth enabling for
agent workflows is build-on-save (real build diagnostics instead of parse-only):

```json
{
  "enable_build_on_save": true
}
```
