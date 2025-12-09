"""CLI entry point for YouTube video extractor."""

import sys
from pathlib import Path
from .extractor import VideoExtractor
from .exporter import ExcelExporter
from .config_loader import ConfigLoader


def main() -> None:
    """Main CLI function."""
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  yt-extractor <channel_url>              # Extract from a single channel")
        print("  yt-extractor --config <config.yaml>     # Extract from channels in config file")
        print("\nExamples:")
        print("  yt-extractor 'https://www.youtube.com/@AlexHormozi'")
        print("  yt-extractor --config channels.yaml")
        sys.exit(1)
    
    try:
        # Check if using config file
        if sys.argv[1] == "--config" or sys.argv[1] == "-c":
            if len(sys.argv) < 3:
                print("Error: Config file path required", file=sys.stderr)
                sys.exit(1)
            
            config_path = sys.argv[2]
            process_config_file(config_path)
        else:
            # Direct URL mode
            channel_url = sys.argv[1]
            process_single_channel(channel_url)
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def process_single_channel(channel_url: str, output_dir: Path | None = None, filename_format: str | None = None) -> None:
    """Process a single channel URL.
    
    Args:
        channel_url: YouTube channel URL
        output_dir: Optional output directory
        filename_format: Optional filename format string
    """
    print(f"Extracting videos from: {channel_url}")
    extractor = VideoExtractor(channel_url)
    videos, channel_name = extractor.extract()
    
    print(f"Found {len(videos)} videos from channel: {channel_name}")
    
    if not videos:
        print("No videos found!")
        return
    
    # Export to Excel
    print("Exporting to Excel...")
    exporter = ExcelExporter(videos, channel_name)
    output_path = exporter.export(output_dir, filename_format)
    
    print(f"✓ Successfully exported to: {output_path}")
    print(f"  Total videos: {len(videos)}")


def process_config_file(config_path: str) -> None:
    """Process channels from a YAML configuration file.
    
    Args:
        config_path: Path to YAML configuration file
    """
    print(f"Loading configuration from: {config_path}")
    
    # Load configuration
    loader = ConfigLoader(config_path)
    loader.load()
    
    channels = loader.get_enabled_channels()
    output_settings = loader.get_output_settings()
    
    print(f"Found {len(channels)} enabled channel(s)\n")
    
    # Process each channel
    for i, channel in enumerate(channels, 1):
        channel_name = channel.get("name", f"Channel {i}")
        channel_url = channel["url"]
        
        print(f"[{i}/{len(channels)}] Processing: {channel_name}")
        print(f"  URL: {channel_url}")
        
        try:
            # Extract videos
            extractor = VideoExtractor(channel_url)
            videos, extracted_name = extractor.extract()
            
            # Use extracted name if no name was provided in config
            if channel.get("name") == f"Channel {i}":
                channel_name = extracted_name
            
            print(f"  Found {len(videos)} videos")
            
            if not videos:
                print("  No videos found, skipping...\n")
                continue
            
            # Export to Excel
            output_dir = Path(output_settings["directory"])
            filename_format = output_settings.get("filename_format")
            exporter = ExcelExporter(videos, channel_name)
            output_path = exporter.export(output_dir, filename_format)
            
            print(f"  ✓ Exported to: {output_path}")
            print(f"  Total videos: {len(videos)}\n")
            
        except Exception as e:
            print(f"  ✗ Failed: {e}\n", file=sys.stderr)
            continue
    
    print("All channels processed!")


if __name__ == "__main__":
    main()

