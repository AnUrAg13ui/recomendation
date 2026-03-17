import json
import logging
from typing import Dict, Any
from backend.services.llm.llm_client import llm_client
from backend.schemas.schemas import UserProfileCreate, RoadmapData
from backend.config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

class RoadmapEngine:
    """
    Coordinates the roadmap generation pipeline:
    User Input -> Profile Analyzer -> Skill Gap Detector -> Prompt Builder -> LLM Client -> Roadmap Formatter
    """
    
    SYSTEM_PROMPT = SYSTEM_PROMPT
    USER_PROMPT_TEMPLATE = USER_PROMPT_TEMPLATE

    def analyze_profile(self, profile: UserProfileCreate) -> Dict[str, Any]:
        """
        Analyzes the user profile. In a more complex system, this might fetch 
        historical data or normalize skill names. For now, it passes through the data.
        """
        return profile.model_dump()

    def detect_skill_gaps(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detects skill gaps. The LLM handles the semantic gap detection in this architecture,
        so we just forward the profile data. We could augment this with a static knowledge graph later.
        """
        return profile_data

    def build_prompt(self, analyzed_data: Dict[str, Any]) -> str:
        """
        Builds the prompt using the template and analyzed data.
        """
        return self.USER_PROMPT_TEMPLATE.format(
            experience_level=analyzed_data.get("experience_level", "beginner"),
            current_skills=", ".join(analyzed_data.get("current_skills", [])),
            career_goal=analyzed_data.get("career_goal", "Software Developer"),
            preferred_stack=", ".join(analyzed_data.get("preferred_stack", [])),
            daily_study_hours=analyzed_data.get("daily_study_hours", 2),
            target_months=analyzed_data.get("target_months", 6)
        )

    def format_roadmap(self, llm_response: str) -> dict:
        """
        Parses and formats the LLM response into a structured dictionary.
        Handles potential JSON formatting errors from the LLM.
        """
        try:
            # Strip markdown code blocks if the LLM wrapped the JSON
            if llm_response.startswith("```json"):
                llm_response = llm_response[7:]
            if llm_response.endswith("```"):
                llm_response = llm_response[:-3]
                
            parsed_data = json.loads(llm_response.strip())
            
            # Basic validation
            if "phases" not in parsed_data:
                logger.warning("LLM response missing 'phases' key. Appending empty phases list.")
                parsed_data["phases"] = []
                
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response into JSON: {e}\nResponse: {llm_response}")
            raise ValueError("The generated roadmap could not be parsed as JSON.")

    def generate_roadmap(self, profile: UserProfileCreate) -> dict:
        """
        Executes the full pipeline to generate a roadmap.
        """
        logger.info("Starting roadmap generation pipeline.")
        analyzed_profile = self.analyze_profile(profile)
        gap_data = self.detect_skill_gaps(analyzed_profile)
        prompt = self.build_prompt(gap_data)
        
        logger.info("Calling LLM client.")
        llm_response = llm_client.generate(prompt=prompt, system_prompt=self.SYSTEM_PROMPT)
        
        logger.info("Formatting roadmap.")
        formatted_roadmap = self.format_roadmap(llm_response)
        
        return formatted_roadmap

roadmap_engine = RoadmapEngine()
