import json
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

def load_criteria():
    criteria_path = Path(__file__).parent / "scoring-criteria.json"
    with open(criteria_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def assess_competency(narrative: str, competency: dict) -> dict:
    """Use Claude to assess a single competency against the narrative."""

    comp_id = competency["id"]
    comp_name = competency["name"]
    definition = competency["definition"]
    levels = competency["levels"]

    # Build level descriptions for Claude
    level_descriptions = ""
    for level in levels:
        level_descriptions += f"\nLevel {level['level']}: {level['description']}\n"
        level_descriptions += "Indicators:\n"
        for indicator in level["indicators"]:
            level_descriptions += f"- {indicator}\n"

    prompt = f"""Analyze the following narrative and assess the competency "{comp_name}".

COMPETENCY DEFINITION:
{definition}

COMPETENCY LEVELS:
{level_descriptions}

NARRATIVE TO ANALYZE:
{narrative}

Based on the narrative provided, determine:
1. Which level (1-5) best matches the person's demonstrated competency
2. Provide the specific level number (1-5)
3. List which behavioral indicators from the narrative support this level
4. Extract 2-3 key quotes from the narrative as evidence
5. Provide a brief explanation for why this level was chosen

Format your response as JSON with these fields:
{{
  "achieved_level": <number 1-5>,
  "indicators_found": [<list of indicator descriptions found in narrative>],
  "evidence": [<list of 2-3 quotes from narrative>],
  "reasoning": "<explanation of why this level was assigned>",
  "strengths": "<what the narrative shows well>",
  "next_level_focus": "<what would be needed for the next level>"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text

    try:
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        assessment = json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        assessment = {
            "achieved_level": 2,
            "indicators_found": ["Unable to parse response"],
            "evidence": [],
            "reasoning": response_text[:200],
            "strengths": "See narrative",
            "next_level_focus": "Provide more detailed examples"
        }

    achieved_level = assessment.get("achieved_level", 2)
    level_desc = next((lv["description"] for lv in levels if lv["level"] == achieved_level), "")

    return {
        "id": comp_id,
        "name": comp_name,
        "definition": definition,
        "achieved_level": achieved_level,
        "indicators_found": assessment.get("indicators_found", []),
        "evidence": assessment.get("evidence", []),
        "reasoning": assessment.get("reasoning", ""),
        "strengths": assessment.get("strengths", ""),
        "next_level_focus": assessment.get("next_level_focus", ""),
        "level_description": level_desc,
        "all_levels": levels
    }

def assess_narrative(narrative: str) -> dict:
    """Assess all competencies in the narrative using Claude."""
    criteria = load_criteria()
    results = {}

    for competency in criteria["competencies"]:
        result = assess_competency(narrative, competency)
        results[competency["id"]] = result

    return results
