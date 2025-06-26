import modal
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import os
import uuid
import pathlib
import shutil
import time

from config.modal_config import image, volume, mount_path
from services.transcription_service import TranscriptionService
from services.moment_identification_service import MomentIdentificationService
from services.clip_processing_service import ClipProcessingService
from utils.s3_utils import S3Utils

class ProcessVideoRequest(BaseModel):
    s3_key: str
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
        self.s3_utils = S3Utils()
        
        print("All services initialized successfully...")

    @modal.fastapi_endpoint(method="POST")
    def process_video(self, request: ProcessVideoRequest, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        s3_key = request.s3_key
        mode = request.mode

        if token.credentials != os.environ["AUTH_TOKEN"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect bearer token", headers={"WWW-Authenticate": "Bearer"})

        run_id = str(uuid.uuid4())
        base_dir = pathlib.Path("/tmp") / run_id
        base_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Download video file
            video_path = base_dir / "input.mp4"
            self.s3_utils.download_file(s3_key, str(video_path))

            # 1. Transcription
            transcript_segments = self.transcription_service.transcribe_video(base_dir, video_path)

            # 2. Identify moments for clips using the specified mode
            print(f"Identifying clip moments using {mode} mode")
            clip_moments = self.moment_identification_service.identify_moments(transcript_segments, mode)

            print(f"Found {len(clip_moments)} moments using {mode} mode: {clip_moments}")

            # 3. Process clips
            for index, moment in enumerate(clip_moments[:5]):
                if "start" in moment and "end" in moment:
                    print(f"Processing clip {index} from {moment['start']} to {moment['end']}")
                    self.clip_processing_service.process_clip(
                        base_dir, video_path, s3_key, 
                        moment["start"], moment["end"], index, transcript_segments
                    )

        finally:
            if base_dir.exists():
                print(f"Cleaning up temp dir: {base_dir}")
                shutil.rmtree(base_dir, ignore_errors=True)

@app.local_entrypoint()
def main():
    import requests

    ai_podcast_clipper = AiPodcastClipper()
    url = ai_podcast_clipper.process_video.web_url

    payload = {
        "s3_key": "test1/mi65mins.mp4",
        "mode": "question"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 123123"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    print(result)