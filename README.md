# Stock Assistant MCP Server

This project implements a simple Model Context Protocol (MCP) server that provides real-time stock data, historical analysis, and stock comparisons using the Yahoo Finance API.

This MCP server uses SSE transport and is authenticated with an API key.

## Running locally

Prerequisites:

* Python 3.13 or later
* [uv](https://docs.astral.sh/uv/getting-started/installation/)

Run the server locally:

```bash
uv venv
uv sync

# linux/macOS
export API_KEYS=<AN_API_KEY>
# windows
set API_KEYS=<AN_API_KEY>

uv run fastapi dev main.py
```

VS Code MCP configuration (mcp.json):

```json
{
    "inputs": [
        {
            "type": "promptString",
            "id": "my-api-key",
            "description": "Stock Assistant API Key",
            "password": true
        }
    ],
    "servers": {
        "stock-mcp-sse": {
            "type": "sse",
            "url": "http://localhost:8000/sse",
            "headers": {
                "x-api-key": "${input:my-api-key}"
            }
        }
    }
}
```

## Deploy to Azure Container Apps

```bash
az containerapp up -g <RESOURCE_GROUP_NAME> -n stock-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
```

If the deployment is successful, the Azure CLI returns the URL of the app. You can use this URL to connect to the server from Visual Studio Code.
