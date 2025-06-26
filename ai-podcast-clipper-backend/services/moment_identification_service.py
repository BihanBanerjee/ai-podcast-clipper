import json
import os
from google import genai
from prompts.clip_mode_prompts import CLIP_MODES

class MomentIdentificationService:
    def __init__(self):
        print("Creating Gemini client...")
        self.gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        print("Gemini client created successfully.")

    def identify_moments(self, transcript_segments, mode="question"):
        """Identify moments in transcript based on specified mode"""
        # Get the prompt for the specified mode, default to question mode
        prompt = CLIP_MODES.get(mode, CLIP_MODES["question"])
        
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17", 
            contents=prompt + str(transcript_segments)
        )
        
        print(f"Identified moments response for {mode} mode: {response.text}")
        
        # Clean and parse the response
        cleaned_json_string = response.text.strip()
        if cleaned_json_string.startswith("```json"):
            cleaned_json_string = cleaned_json_string[len("```json"):].strip()
        if cleaned_json_string.endswith("```"):
            cleaned_json_string = cleaned_json_string[:-len("```")].strip()

        try:
            clip_moments = json.loads(cleaned_json_string)
            if not clip_moments or not isinstance(clip_moments, list):
                print("Error: Identified moments is not a list")
                return []
            return clip_moments
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return []