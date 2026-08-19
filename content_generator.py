import json
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent

class LinkedInContentGenerator:
    """
    Anti-slop Long-Form Post Generator for LinkedIn.
    Formats technical case studies & operational efficiency insights
    for high mobile readability and algorithmic dwell time.
    """

    def __init__(self, persona_file: str = "persona.json"):
        self.persona_path = BASE_DIR / persona_file
        with open(self.persona_path, "r", encoding="utf-8") as f:
            self.persona = json.load(f)

    def format_post(
        self,
        hook: str,
        problem_statement: str,
        solution_points: List[Dict[str, str]],
        metrics_impact: str,
        cta: str,
        hashtags: Optional[List[str]] = None
    ) -> str:
        """
        Assembles a high-conversion, skimmable LinkedIn post.
        """
        # 1. Hook (2-line opener crafted for '...see more' clicks)
        formatted_lines = [hook.strip(), ""]

        # 2. Context / Problem Statement
        if problem_statement:
            formatted_lines.extend([problem_statement.strip(), ""])

        # 3. Core Architecture / Solution Points
        for idx, pt in enumerate(solution_points, 1):
            title = pt.get("title", f"Point {idx}")
            desc = pt.get("desc", "")
            formatted_lines.append(f"📌 {idx}. {title}")
            formatted_lines.append(f"{desc.strip()}")
            formatted_lines.append("")

        # 4. Measurable Business / Engineering Impact
        if metrics_impact:
            formatted_lines.extend(["📊 Key Takeaway / Impact:", metrics_impact.strip(), ""])

        # 5. Call To Action
        formatted_lines.extend(["---", cta.strip()])

        # 6. Minimalist Hashtags (Max 3-4 focused tags)
        if hashtags:
            clean_tags = " ".join([f"#{t.replace('#', '').strip()}" for t in hashtags[:4]])
            formatted_lines.extend(["", clean_tags])

        raw_post = "\n".join(formatted_lines).strip()
        return self._sanitize_anti_slop(raw_post)

    def _sanitize_anti_slop(self, text: str) -> str:
        """Removes generic chatbot cliches and empty buzzwords."""
        banned_en = self.persona.get("anti_slop_rules", {}).get("banned_phrases_en", [])
        banned_id = self.persona.get("anti_slop_rules", {}).get("banned_phrases_id", [])

        for phrase in banned_en + banned_id:
            if phrase.lower() in text.lower():
                # Replace insensitive case
                text = text.replace(phrase, "")
                text = text.replace(phrase.capitalize(), "")

        # Clean double spaces caused by removal
        while "  " in text:
            text = text.replace("  ", " ")
        return text
