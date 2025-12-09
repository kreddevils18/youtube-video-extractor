"""Excel export functionality."""

from datetime import datetime
from pathlib import Path
from typing import Any
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from .config import EXCEL_COLUMNS


class ExcelExporter:
    """Exports video data to Excel format."""
    
    def __init__(self, videos: list[dict[str, Any]], channel_name: str) -> None:
        """Initialize the exporter with video data.
        
        Args:
            videos: List of video dictionaries
            channel_name: Name of the YouTube channel
        """
        self.videos = videos
        self.channel_name = channel_name
    
    def export(self, output_dir: Path | None = None, filename_format: str | None = None) -> Path:
        """Export videos to an Excel file.
        
        Args:
            output_dir: Directory to save the file (defaults to current directory)
            filename_format: Format string for filename (supports {channel_name} and {date})
            
        Returns:
            Path to the created Excel file
            
        Raises:
            Exception: If export fails
        """
        try:
            # Sort videos by upload_date (newest first)
            # Handle None values by using empty string as default
            sorted_videos = sorted(
                self.videos,
                key=lambda x: x.get("upload_date") or "",
                reverse=True
            )
            
            # Create workbook and worksheet
            wb = Workbook()
            ws = wb.active
            ws.title = "Videos"
            
            # Write header row
            ws.append(EXCEL_COLUMNS)
            
            # Style header row
            for cell in ws[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal="center")
            
            # Write video data
            for video in sorted_videos:
                ws.append([
                    video.get("id", ""),
                    video.get("title", ""),
                    video.get("description", ""),
                    video.get("url", ""),
                ])
            
            # Auto-adjust column widths
            self._adjust_column_widths(ws)
            
            # Determine output path
            if output_dir is None:
                output_dir = Path.cwd() / "outputs"
            else:
                output_dir = Path(output_dir)
            
            # Create output directory if it doesn't exist
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            if filename_format is None:
                filename_format = "{channel_name}_videos.xlsx"
            
            # Get current date
            current_date = datetime.now().strftime("%Y%m%d")
            
            # Sanitize channel name for filename
            safe_channel_name = self._sanitize_filename(self.channel_name)
            
            # Replace placeholders in filename format
            filename = filename_format.format(
                channel_name=safe_channel_name,
                date=current_date
            )
            
            output_path = output_dir / filename
            
            # Save workbook
            wb.save(output_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to export to Excel: {str(e)}") from e
    
    @staticmethod
    def _adjust_column_widths(ws) -> None:
        """Adjust column widths based on content."""
        # Set reasonable widths for each column
        ws.column_dimensions["A"].width = 15  # ID
        ws.column_dimensions["B"].width = 50  # Title
        ws.column_dimensions["C"].width = 80  # Description
        ws.column_dimensions["D"].width = 50  # URL
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Remove invalid characters from filename.
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename safe for filesystem use
        """
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(". ")
        
        # Limit length
        max_length = 100
        if len(filename) > max_length:
            filename = filename[:max_length]
        
        return filename or "channel"
