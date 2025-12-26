#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error

IIR_HTTP_URL = os.environ.get("IIR_HTTP_URL", "http://127.0.0.1:8000/mcp/replace")
IIR_TOKEN = os.environ.get("IIR_TOKEN", "")

TOOL_NAME = "iir_replace"

def http_replace(text: str) -> str:
    if not IIR_TOKEN:
        raise RuntimeError("IIR_TOKEN is not set")

    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        IIR_HTTP_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Token {IIR_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            out = data.get("text")
            if not isinstance(out, str):
                raise RuntimeError(f"Unexpected response shape: {data}")
            return out
    except urllib.error.HTTPError as e:
        # Avoid leaking internal details; surface status only
        raise RuntimeError(f"HTTPError {e.code}") from e

def reply(_id, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": _id}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def mcp_error(code: int, message: str):
    return {"code": code, "message": message}

def handle(req: dict):
    _id = req.get("id")
    method = req.get("method")
    params = req.get("params") or {}

    # Minimal MCP surface: initialize, tools/list, tools/call
    if method == "initialize":
        # Minimal capabilities for a tools-only server
        return _id, {
            "protocolVersion": params.get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {
                "list": True,
                "call": True
            }},
            "serverInfo": {"name": "iir-mcp-wrapper", "version": "0.1.0"},
        }, None

    if method == "initialized":
        # notification, no response
        return None, None, None

    if method == "tools/list":
        return _id, {
            "tools": [
                {
                    "name": TOOL_NAME,
                    "description": "Transform-only replacement boundary (iir). Input text -> sanitized text.",
                    "inputSchema": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["text"],
                        "properties": {
                            "text": {"type": "string"}
                        },
                    },
                }
            ]
        }, None

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name != TOOL_NAME:
            return _id, None, mcp_error(-32602, "Unknown tool")

        text = arguments.get("text")
        if not isinstance(text, str):
            return _id, None, mcp_error(-32602, "Invalid arguments: text must be a string")

        try:
            out = http_replace(text)
        except Exception as e:
            return _id, None, mcp_error(-32000, f"Tool execution failed: {e}")

        # MCP tool result content (text only)
        return _id, {
            "content": [{"type": "text", "text": out}]
        }, None

    return _id, None, mcp_error(-32601, "Method not found")

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            _id, result, error = handle(req)
            if _id is None:
                continue
            reply(_id, result=result, error=error)
        except Exception as e:
            # If id is unknown, reply with null id per JSON-RPC convention
            reply(req.get("id") if isinstance(req, dict) else None, error=mcp_error(-32700, f"Parse/dispatch error: {e}"))

if __name__ == "__main__":
    main()

