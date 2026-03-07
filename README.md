# Radarr MCP Server

A Model Context Protocol (MCP) server for managing Radarr via natural language interfaces.

## Features

- Search and lookup movies
- Manage quality profiles
- View and manage download queue
- Trigger movie searches
- Delete movie files
- View movie file details

## Environment Variables

### Required
- `RADARR_API_KEY` - Your Radarr API key

### Optional
- `RADARR_URL` - Radarr instance URL (default: `http://localhost:7878`)
- `MCP_HOST` - Host to bind server to (default: `localhost`)
- `MCP_PORT` - MCP server port (default: `7979`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

## Docker Usage

### Build the image

```bash
docker build -t radarr-mcp .
```

### Run the container

```bash
docker run --rm \
  -p 7979:7979 \
  -e RADARR_API_KEY=your_api_key_here \
  -e RADARR_URL=http://localhost:7878 \
  radarr-mcp
```

**Note:** Use `host.docker.internal` to access services running on your host machine from within the container.

### Run with environment file

Create a `.env` file:
```
RADARR_API_KEY=your_api_key_here
RADARR_URL=http://host.docker.internal:7878
MCP_PORT=7979
LOG_LEVEL=INFO
```

Run with:
```bash
docker run --rm -p 7979:7979 --env-file .env radarr-mcp
```

## Local Development

### Prerequisites
- Python 3.14+
- uv (recommended) or pip

### Setup

```bash
# Install dependencies
uv sync

# Set environment variables
export RADARR_API_KEY=your_api_key_here
export RADARR_URL=http://localhost:7878

# Run the server
uv run main.py
```

## Available Tools

- `lookup_movie` - Search for movies by title
- `search_movie` - Trigger a search for a movie
- `get_download_queue` - View current download queue
- `delete_queue_item` - Remove item from download queue
- `lookup_movie_file` - Get movie file details
- `delete_movie_file` - Delete a movie file
- `get_quality_profiles` - List available quality profiles
- `update_movie_quality` - Update movie quality profile

## License

GPL-3.0
