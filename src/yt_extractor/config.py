"""Configuration constants for the YouTube extractor."""

# Excel column headers
EXCEL_COLUMNS = ["ID", "Title", "Description", "URL"]

# yt-dlp options for extracting video information
YT_DLP_OPTIONS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": "in_playlist",  # Extract video IDs without full metadata
    "skip_download": True,
    "no_check_certificates": True,  # Fix for SSL certificate issues on macOS
}
