import requests

BASE = "http://127.0.0.1:8000/mcp"

# 1. Initialize
res = requests.post(BASE, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
})

session_id = res.headers.get("mcp-session-id")
print("Session:", session_id)

# 2. Call tool
res = requests.post(
    BASE,
    headers={"mcp-session-id": session_id},
    json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_article_summary",
            "arguments": {"query": "Python programming"}
        }
    }
)

print(res.text)
