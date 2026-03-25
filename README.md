# wikipedia Readme file 

# how to run the server 

1. uv init wikipedia-mcp
2. cd wikipedia-mcp
3. uv venv
4. source .venv/bin/activate
5. uv add "mcp[cli]" wikipedia
6. python server.py
7. Sample server output
INFO:     Started server process [29519]
INFO:     Waiting for application startup.
INFO:mcp.server.streamable_http_manager:StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)  


# How to Test using wikipedia Server

 curl -s -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'



