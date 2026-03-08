import logging
import requests
import os

RADARR_URL = os.getenv("RADARR_URL", "http://localhost:7878")
RADARR_API_KEY = os.getenv("RADARR_API_KEY")


def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    """Make API request with consistent error handling."""
    try:
        response = requests.request(
            method,
            f"{RADARR_URL}/api/v3/{endpoint}",
            headers={"X-Api-Key": RADARR_API_KEY},
            **kwargs
        )
        response.raise_for_status()
        
        # Handle empty responses (e.g., DELETE returning 200/204)
        if response.status_code == 204 or not response.content:
            return {"success": True}
        
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg}

def lookup_movie(title: str) -> list[dict] | dict:
    """Search for a movie by title. Returns a list of candidates with key fields to help identify the correct movie, including whether it's already in the Radarr library."""
    logging.info(f"Looking up movie '{title}'...")
    result = _make_api_request("movie/lookup", params={"term": title})
    
    if isinstance(result, dict) and "error" in result:
        return result
    
    if not result:
        logging.info(f"No results found for '{title}'.")
        return []
    
    logging.info(f"Found {len(result)} result(s) for '{title}'.")
    return [
        {
            "radarrId": m.get("id"),
            "tmdbId": m.get("tmdbId"),
            "title": m.get("title"),
            "year": m.get("year"),
            "inLibrary": m.get("id") is not None,
            "movieFileId": m.get("movieFile", {}).get("id") if m.get("movieFile") else None
        }
        for m in result[:10]
    ]

def search_movie(radarr_id: int) -> dict:
    """Trigger a search for a movie in Radarr by its Radarr ID. This is useful for replacing movies"""
    logging.info(f"Triggering search for movie ID '{radarr_id}'...")
    response = _make_api_request(f"command", method="POST", json={
        "name": "MoviesSearch",
        "movieIds": [radarr_id]
    })
    status = f"Search command {response.get('id', 'unknown')} for movie ID {radarr_id} is {response.get('status', 'unknown')}"
    logging.info(status)
    return {"status": status}

def get_download_queue() -> list[dict]:
    """Get the current download queue from Radarr. Use this to find broken or stalled downloads."""
    logging.info("Fetching download queue...")
    queue = _make_api_request("queue")
    records = queue.get("records", [])
    logging.info(f"Found {len(records)} item(s) in the download queue.")
    return [
        {
            "queueId": r.get("id"),
            "movieId": r.get("movieId"),
            "title": r.get("title"),
            "status": r.get("status"),
            "trackedDownloadStatus": r.get("trackedDownloadStatus"),
            "errorMessage": r.get("errorMessage"),
        }
        for r in records
    ]

def delete_queue_item(queue_id: int) -> dict:
    """Delete an item from the Radarr download queue by its Queue ID."""
    logging.info(f"Deleting queue item ID '{queue_id}'...")
    status = _make_api_request(f"queue/{queue_id}", method="DELETE",
        params={"removeFromClient": True, "blocklist": True}
        )
    return status

def lookup_movie_file(moviefile_id: int) -> dict:
    """Lookup a MovieFile in Radarr by its MovieFile ID."""
    logging.info(f"Looking up MovieFile ID '{moviefile_id}'...")
    moviefile = _make_api_request(f"moviefile/{moviefile_id}")
    return moviefile

def delete_movie_file(moviefile_id: int) -> dict:
    """Delete a MovieFile from Radarr by its MovieFile ID."""
    logging.info(f"Deleting MovieFile ID '{moviefile_id}'...")
    status = _make_api_request(f"moviefile/{moviefile_id}",method="DELETE")
    return status

def get_quality_profiles() -> list[dict]:
    """Get all quality profiles from Radarr."""
    logging.info("Fetching quality profiles...")
    profiles = _make_api_request("qualityprofile")
    return [
        {
            "id": p.get("id"),
            "name": p.get("name"),
            "cutoff": p.get("cutoff"),
            "upgradeAllowed": p.get("upgradeAllowed"),
        }
        for p in profiles
    ]

def update_movie_quality(radarr_id: int, quality_profile_id: int) -> dict:
    """Update the quality profile of a movie in Radarr."""
    logging.info(f"Updating quality profile for movie ID '{radarr_id}' to profile ID '{quality_profile_id}'...")
    movie = _make_api_request(f"movie/{radarr_id}")
    if "error" in movie:
        return movie
    
    movie["qualityProfileId"] = quality_profile_id
    updated_movie = _make_api_request(f"movie/{radarr_id}", method="PUT", json=movie)
    return updated_movie