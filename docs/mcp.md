# MCP Integration (Transform-only)

## Purpose

iir can be used as a final, transform-only safety boundary before LLM outputs
are shared externally.

The MCP integration exposes a single operation only:

- text replacement using the active dictionary
- no read access to dictionary contents
- no write operations
- no reverse mapping

This design intentionally limits MCP to a final output boundary and preserves
the core safety assumptions of iir.

## Architecture

```text
LLM → MCP tool → iir (/mcp/replace) → transformed text
```

## Endpoint

```text
POST /mcp/replace
Authorization: Token <token>
```

Body (JSON):

```json
{
  "text": "..."
}
```

## Reference MCP Wrapper

A reference stdio-based MCP wrapper is provided under:

```text
tools/iir_mcp_wrapper.py
```

This wrapper is not imported by iir itself and is intended for local,
tool-based LLM environments such as LM Studio.

The wrapper acts as a thin adapter between MCP tool calls and the HTTP
endpoint provided by iir.

## Prompt Pattern (Recommended)

When using MCP with LLM tool execution, the text intended for external
publication should be explicitly marked.

A recommended pattern is:

```text
<<PUBLISH>>
Text intended for external sharing goes here.
<<END>>
```

Only the content inside this block should be passed to the MCP tool.

Instructions, prompts, or meta text must never be passed to the tool.

## Scope and Constraints

- MCP is optional and not required for normal iir usage
- MCP does not alter replacement rules or dictionary behavior
- MCP is intended for on-premise or self-hosted environments
- iir must remain safe even if the LLM behaves incorrectly

MCP integration exists to enforce structural safety at the final output
boundary, not to provide general-purpose access to iir internals.

