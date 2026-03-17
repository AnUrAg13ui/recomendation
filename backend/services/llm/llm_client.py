import json
import logging
import requests
import google.generativeai as genai
from backend.config_settings import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.provider = settings.MODEL_PROVIDER.lower()
        if self.provider == "api":
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Using flash model for fast and structured responses
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        elif self.provider == "local":
            self.local_url = settings.LOCAL_MODEL_URL
            self.local_model_name = settings.LOCAL_MODEL_NAME
        else:
            raise ValueError(f"Unsupported MODEL_PROVIDER: {self.provider}")
            
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generates text using the configured LLM provider.
        """
        if self.provider == "api":
            return self._generate_api(prompt, system_prompt)
        elif self.provider == "local":
            return self._generate_local(prompt, system_prompt)

    def _generate_api(self, prompt: str, system_prompt: str) -> str:
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise
            
    def _generate_local(self, prompt: str, system_prompt: str) -> str:
        try:
            # Assuming Ollama style API
            payload = {
                "model": self.local_model_name,
                "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
                "stream": False,
                "format": "json"
            }
            response = requests.post(self.local_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling local LLM API: {e}")
            raise

llm_client = LLMClient()
