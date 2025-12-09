# YouTube Video Extractor

Extract all videos from a YouTube channel and export them to an Excel file.

## Features

- Extract video metadata (ID, title, description, URL) from any YouTube channel
- Export to Excel (.xlsx) format
- Videos sorted by newest first

## Requirements

- Python 3.11+
- uv (package manager)

## Installation

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone or navigate to the project directory
cd youtube-video-extractor

# Install dependencies
uv sync
```

## Usage

### Option 1: Direct URL

Extract videos from a single channel by providing the URL directly:

```bash
uv run yt-extractor "https://www.youtube.com/@AlexHormozi"
```

### Option 2: YAML Configuration File

For multiple channels or repeated extractions, use a YAML configuration file:

1. Create a configuration file (e.g., `channels.yaml`):

```yaml
channels:
  - name: "Alex Hormozi"
    url: "https://www.youtube.com/@AlexHormozi"
    enabled: true

  - name: "Another Channel"
    url: "https://www.youtube.com/@ChannelName"
    enabled: true

output:
  directory: "."
  filename_format: "{channel_name}_{date}.xlsx"
```

2. Run the extractor with the config file:

```bash
uv run yt-extractor --config channels.yaml
```

The script will process all enabled channels and create separate Excel files for each.

## Output Format

The Excel file contains the following columns:

- **ID**: YouTube video ID
- **Title**: Video title
- **Description**: Video description
- **URL**: Full video URL

Videos are sorted by upload date (newest first).

## Technical Stack

- **Python**: Core language
- **uv**: Package management
- **yt-dlp**: YouTube data extraction
- **openpyxl**: Excel file generation
