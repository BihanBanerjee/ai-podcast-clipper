import subprocess
import shutil
import time
import pickle
import os
from video_processing.vertical_video_creator import create_vertical_video
from video_processing.subtitle_generator import create_subtitles_with_ffmpeg
from utils.s3_utils import S3Utils

class ClipProcessingService:
    def __init__(self):
        self.s3_utils = S3Utils()

    def process_clip(self, base_dir, original_video_path, s3_key, start_time, end_time, clip_index, transcript_segments):
        """Process a single clip from the original video"""
        clip_name = f"clip_{clip_index}"
        s3_key_dir = os.path.dirname(s3_key)
        output_s3_key = f"{s3_key_dir}/{clip_name}.mp4"
        print(f"Output S3 key: {output_s3_key}")

        clip_dir = base_dir / clip_name
        clip_dir.mkdir(parents=True, exist_ok=True)

        clip_segment_path = clip_dir / f"{clip_name}_segment.mp4"
        vertical_mp4_path = clip_dir / "pyavi" / "video_out_vertical.mp4"
        subtitle_output_path = clip_dir / "pyavi" / "video_with_subtitles.mp4"

        # Create directory structure
        (clip_dir / "pywork").mkdir(exist_ok=True)
        pyframes_path = clip_dir / "pyframes"
        pyavi_path = clip_dir / "pyavi"
        audio_path = clip_dir / "pyavi" / "audio.wav"

        pyframes_path.mkdir(exist_ok=True)
        pyavi_path.mkdir(exist_ok=True)

        try:
            # Extract clip segment
            self._extract_clip_segment(original_video_path, start_time, end_time, clip_segment_path)
            
            # Extract audio
            self._extract_audio(clip_segment_path, audio_path)
            
            # Copy clip for Columbia processing
            shutil.copy(clip_segment_path, base_dir / f"{clip_name}.mp4")

            # Run Columbia script for speaker detection
            self._run_columbia_script(clip_name, base_dir)

            # Load tracks and scores
            tracks, scores = self._load_processing_results(clip_dir)

            # Create vertical video
            self._create_vertical_video(tracks, scores, pyframes_path, pyavi_path, audio_path, vertical_mp4_path)

            # Add subtitles
            create_subtitles_with_ffmpeg(
                transcript_segments, start_time, end_time, 
                vertical_mp4_path, subtitle_output_path, max_words=5
            )

            # Upload to S3
            self.s3_utils.upload_file(subtitle_output_path, output_s3_key)
            
        except Exception as e:
            print(f"Error processing clip {clip_index}: {e}")
            raise

    def _extract_clip_segment(self, original_video_path, start_time, end_time, output_path):
        """Extract a segment from the original video"""
        duration = end_time - start_time
        cut_command = (f"ffmpeg -i {original_video_path} -ss {start_time} -t {duration} "
                       f"{output_path}")
        subprocess.run(cut_command, shell=True, check=True, capture_output=True, text=True)

    def _extract_audio(self, video_path, audio_path):
        """Extract audio from video"""
        extract_cmd = f"ffmpeg -i {video_path} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_path}"
        subprocess.run(extract_cmd, shell=True, check=True, capture_output=True)

    def _run_columbia_script(self, clip_name, base_dir):
        """Run Columbia script for speaker detection"""
        columbia_command = (f"python Columbia_test.py --videoName {clip_name} "
                            f"--videoFolder {str(base_dir)} "
                            f"--pretrainModel weight/finetuning_TalkSet.model")

        columbia_start_time = time.time()
        subprocess.run(columbia_command, cwd="/asd", shell=True)
        columbia_end_time = time.time()
        print(f"Columbia script completed in {columbia_end_time - columbia_start_time:.2f} seconds")

    def _load_processing_results(self, clip_dir):
        """Load tracks and scores from Columbia processing"""
        tracks_path = clip_dir / "pywork" / "tracks.pckl"
        scores_path = clip_dir / "pywork" / "scores.pckl"
        
        if not tracks_path.exists() or not scores_path.exists():
            raise FileNotFoundError("Tracks or scores not found for clip")

        with open(tracks_path, "rb") as f:
            tracks = pickle.load(f)

        with open(scores_path, "rb") as f:
            scores = pickle.load(f)

        return tracks, scores

    def _create_vertical_video(self, tracks, scores, pyframes_path, pyavi_path, audio_path, output_path):
        """Create vertical video with speaker tracking"""
        cvv_start_time = time.time()
        create_vertical_video(tracks, scores, pyframes_path, pyavi_path, audio_path, output_path)
        cvv_end_time = time.time()
        print(f"Vertical video creation time: {cvv_end_time - cvv_start_time:.2f} seconds")