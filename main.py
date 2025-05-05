from fastapi import FastAPI, Request, Depends
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from stock_price_server import mcp
from api_key_auth import ensure_valid_api_key
import uvicorn

# Create FastAPI application with metadata
app = FastAPI(
    title="FastAPI MCP SSE",
    description="A demonstration of Server-Sent Events with Model Context "
    "Protocol integration",
    version="0.1.0",
)

# Create SSE transport instance for handling server-sent events
sse = SseServerTransport("/messages/")

# Mount the /messages path to handle SSE message posting
app.router.routes.append(Mount("/messages", app=sse.handle_post_message))

@app.get("/sse", tags=["MCP"])
async def handle_sse(request: Request, _: str = Depends(ensure_valid_api_key)):
    
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        init_options = mcp._mcp_server.create_initialization_options()

        try:
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                init_options,
            )
        except RuntimeError as e:
            return {"error": str(e)}

@app.get("/", tags=["Health"])
async def root():
    return {"message": "MCP Stock Skill is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
