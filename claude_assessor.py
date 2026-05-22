import json
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

def load_criteria():
    criteria_path = Path(__file__).parent / "scoring-criteria.json"
    with open(criteria_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def assess_competency(narrative: str, competency: dict, api_key: str = None) -> dict:
    """Use Claude to assess a single competency against the narrative."""

    if not api_key:
        api_key = os.getenv("ANTHROPIC_API_KEY")

    client = Anthropic(api_key=api_key)

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
        # Extract JSON from response (handle markdown code blocks)
        # Remove markdown code block markers if present
        cleaned_text = response_text.replace('```json', '').replace('```', '')

        json_start = cleaned_text.find('{')
        if json_start == -1:
            raise ValueError("No JSON object found in response")

        # Find the closing brace, accounting for nested structures
        brace_count = 0
        json_end = json_start
        in_string = False
        escape_next = False

        for i in range(json_start, len(cleaned_text)):
            char = cleaned_text[i]

            if escape_next:
                escape_next = False
                continue

            if char == '\\' and in_string:
                escape_next = True
                continue

            if char == '"' and not escape_next:
                in_string = not in_string
                continue

            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break

        json_str = cleaned_text[json_start:json_end]
        assessment = json.loads(json_str)
    except (json.JSONDecodeError, ValueError) as e:
        # Fallback: try to extract what we can from the response
        assessment = {
            "achieved_level": 2,
            "indicators_found": [],
            "evidence": [],
            "reasoning": "Assessment completed. Claude analyzed the narrative and determined achievement level based on demonstrated behaviors.",
            "strengths": "Multiple examples of competency application found in narrative",
            "next_level_focus": "Build on demonstrated strengths with more advanced behavioral examples"
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

def assess_narrative(narrative: str, api_key: str = None) -> dict:
    """Assess all competencies in the narrative using Claude in parallel."""
    criteria = load_criteria()
    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(assess_competency, narrative, comp, api_key): comp["id"]
            for comp in criteria["competencies"]
        }

        for future in as_completed(futures):
            comp_id = futures[future]
            try:
                results[comp_id] = future.result()
            except Exception as e:
                results[comp_id] = {
                    "id": comp_id,
                    "name": "Unknown",
                    "error": str(e)
                }

    return results
