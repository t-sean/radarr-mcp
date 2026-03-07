import logging
import os
from fastmcp import FastMCP
from tools import lookup_movie, delete_movie_file, search_movie, get_download_queue, delete_queue_item, lookup_movie_file, get_quality_profiles, update_movie_quality

RADARR_API_KEY = os.getenv("RADARR_API_KEY")
MCP_PORT = int(os.getenv("MCP_PORT", "7979"))
MCP_HOST = os.getenv("MCP_HOST", "localhost")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

level = getattr(logging, LOG_LEVEL, logging.INFO)
logging.basicConfig(
    level=level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.propagate = True
    logger.setLevel(logging.DEBUG)

if not RADARR_API_KEY:
    logging.error("RADARR_API_KEY environment variable is not set.")
    exit(1)

mcp = FastMCP("radarr-mcp")
mcp.tool()(lookup_movie)
mcp.tool()(delete_movie_file)
mcp.tool()(search_movie)
mcp.tool()(get_download_queue)
mcp.tool()(delete_queue_item)
mcp.tool()(lookup_movie_file)
mcp.tool()(get_quality_profiles)
mcp.tool()(update_movie_quality)

if __name__ == "__main__":
    mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT)
