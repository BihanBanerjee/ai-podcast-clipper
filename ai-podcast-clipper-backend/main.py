import modal
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import os
import uuid
import pathlib
import shutil
import time
from typing import Optional

from config.modal_config import image, volume, mount_path
from services.transcription_service import TranscriptionService
from services.moment_identification_service import MomentIdentificationService
from services.clip_processing_service import ClipProcessingService
from services.youtube_download_service import YouTubeDownloadService
from utils.s3_utils import S3Utils

class ProcessVideoRequest(BaseModel):
    s3_key: Optional[str] = None
    youtube_url: Optional[str] = None
    mode: str = "question"

app = modal.App("ai-podcast-clipper", image=image)
auth_scheme = HTTPBearer()

@app.cls(gpu="L40S", timeout=900, retries=0, scaledown_window=20, 
         secrets=[modal.Secret.from_name("ai-podcast-clipper-secret")], 
         volumes={mount_path: volume})
class AiPodcastClipper:
    @modal.enter()
    def load_model(self):
        print("Loading models...")
        
        # Initialize services
        self.transcription_service = TranscriptionService()
        self.moment_identification_service = MomentIdentificationService()
        self.clip_processing_service = ClipProcessingService()
        self.youtube_download_service = YouTubeDownloadService()
        self.s3_utils = S3Utils()
        
        print("All services initialized successfully...")



    @modal.fastapi_endpoint(method="POST")
    def process_video(self, request: ProcessVideoRequest, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        if token.credentials != os.environ["AUTH_TOKEN"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect bearer token", headers={"WWW-Authenticate": "Bearer"})

        # Validate that either s3_key or youtube_url is provided
        if not request.s3_key and not request.youtube_url:
            raise HTTPException(status_code=400, detail="Either s3_key or youtube_url must be provided")
        
        if request.s3_key and request.youtube_url:
            raise HTTPException(status_code=400, detail="Provide either s3_key or youtube_url, not both")

        run_id = str(uuid.uuid4())
        base_dir = pathlib.Path("/tmp") / run_id
        base_dir.mkdir(parents=True, exist_ok=True)

        try:
            video_path = base_dir / "input.mp4"
            
            # Determine source and s3_key for clip uploads
            if request.youtube_url:
                # Validate YouTube URL
                if not self.youtube_download_service.validate_youtube_url(request.youtube_url):
                    raise HTTPException(status_code=400, detail="Invalid YouTube URL format")
                
                # Download from YouTube
                self.youtube_download_service.download_video(request.youtube_url, str(video_path))
                
                # Generate a unique s3_key for clip storage using video ID
                video_id = self.youtube_download_service.extract_video_id(request.youtube_url)
                s3_key = f"youtube/{video_id}_{run_id}/original.mp4"
            else:
                # Download from S3 (existing flow)
                self.s3_utils.download_file(request.s3_key, str(video_path))
                s3_key = request.s3_key

            # 1. Transcription
            transcript_segments = self.transcription_service.transcribe_video(base_dir, video_path)

            # 2. Identify moments for clips using the specified mode
            print(f"Identifying clip moments using {request.mode} mode")
            clip_moments = self.moment_identification_service.identify_moments(transcript_segments, request.mode)

            print(f"Found {len(clip_moments)} moments using {request.mode} mode: {clip_moments}")

            # 3. Process clips
            for index, moment in enumerate(clip_moments[:5]):
                if "start" in moment and "end" in moment:
                    print(f"Processing clip {index} from {moment['start']} to {moment['end']}")
                    self.clip_processing_service.process_clip(
                        base_dir, video_path, s3_key, 
                        moment["start"], moment["end"], index, transcript_segments
                    )

            # Return the folder prefix for frontend to track clips
            folder_prefix = s3_key.split("/")[0] if "/" in s3_key else s3_key
            return {"message": "Processing completed", "folder_prefix": folder_prefix}

        finally:
            if base_dir.exists():
                print(f"Cleaning up temp dir: {base_dir}")
                shutil.rmtree(base_dir, ignore_errors=True)

@app.local_entrypoint()
def main():
    import requests

    ai_podcast_clipper = AiPodcastClipper()
    url = ai_podcast_clipper.process_video.web_url

    # Test with S3
    payload_s3 = {
        "s3_key": "test1/mi65mins.mp4",
        "mode": "question"
    }

    # Test with YouTube
    payload_youtube = {
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "mode": "question"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 123123"
    }

    # Choose which test to run
    response = requests.post(url, json=payload_youtube, headers=headers)
    response.raise_for_status()
    result = response.json()
    print(result)