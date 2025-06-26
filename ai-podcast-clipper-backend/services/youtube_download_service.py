import yt_dlp
import os
from fastapi import HTTPException

class YouTubeDownloadService:
    def __init__(self):
        print("YouTube download service initialized.")

    def download_video(self, youtube_url: str, output_path: str) -> str:
        """Download video from YouTube using yt-dlp"""
        print(f"Downloading video from YouTube: {youtube_url}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',  # Prefer mp4, fallback to best available
            'outtmpl': output_path,
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
            'ignoreerrors': True,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'quiet': True,  # Reduce console output
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first for validation and logging
                info = self._get_video_info(ydl, youtube_url)
                
                # Validate video duration (optional - prevent very long videos)
                duration = info.get('duration', 0)
                if duration > 7200:  # 2 hours limit
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Video too long ({duration//60} minutes). Maximum allowed: 120 minutes."
                    )
                
                # Download the video
                print(f"Starting download: {info.get('title', 'Unknown title')}")
                ydl.download([youtube_url])
                
            # Verify file was downloaded
            if not os.path.exists(output_path):
                raise HTTPException(
                    status_code=500, 
                    detail="Video download completed but file not found"
                )
                
            file_size = os.path.getsize(output_path)
            print(f"Successfully downloaded video to: {output_path} ({file_size / (1024*1024):.1f} MB)")
            
            return output_path
            
        except yt_dlp.DownloadError as e:
            print(f"yt-dlp download error: {e}")
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to download video: {str(e)}"
            )
        except Exception as e:
            print(f"Unexpected error during download: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Video download failed: {str(e)}"
            )

    def _get_video_info(self, ydl, youtube_url: str) -> dict:
        """Extract video information without downloading"""
        try:
            info = ydl.extract_info(youtube_url, download=False)
            
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')
            view_count = info.get('view_count', 0)
            
            print(f"Video Info:")
            print(f"  Title: {title}")
            print(f"  Duration: {duration} seconds ({duration//60}:{duration%60:02d})")
            print(f"  Uploader: {uploader}")
            print(f"  Views: {view_count:,}")
            
            return info
            
        except Exception as e:
            print(f"Error extracting video info: {e}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid YouTube URL or video not accessible: {str(e)}"
            )

    def validate_youtube_url(self, url: str) -> bool:
        """Validate if the URL is a valid YouTube URL"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]+)',
        ]
        
        import re
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False

    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        import re
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise HTTPException(status_code=400, detail="Could not extract video ID from URL")