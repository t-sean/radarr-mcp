import logging
import os
from tools import mcp

RADARR_API_KEY = os.getenv("RADARR_API_KEY")
MCP_PORT = int(os.getenv("MCP_PORT", "7979"))
MCP_HOST = os.getenv("MCP_HOST", "localhost")

logging.getLogger("uvicorn").setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

if not RADARR_API_KEY:
    logging.error("RADARR_API_KEY environment variable is not set.")
    exit(1)

if __name__ == "__main__":
    mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT)
