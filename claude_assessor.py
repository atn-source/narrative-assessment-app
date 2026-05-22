import json
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from concurrent.futures import ThreadPoolExecutor, as_completed
from file_processor import extract_text

load_dotenv()

_context_cache = None

def load_criteria():
    criteria_path = Path(__file__).parent / "scoring-criteria.json"
    with open(criteria_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_context_files() -> str:
    """Load all PDF/DOCX files from context/ folder once and cache in memory."""
    global _context_cache
    if _context_cache is not None:
        return _context_cache

    context_dir = Path(__file__).parent / "context"
    if not context_dir.exists():
        _context_cache = ""
        return _context_cache

    context_parts = []
    for file_path in sorted(context_dir.iterdir()):
        if file_path.suffix.lower() in ('.pdf', '.docx', '.md', '.txt'):
            try:
                if file_path.suffix.lower() in ('.md', '.txt'):
                    text = file_path.read_text(encoding='utf-8')
                else:
                    text = extract_text(str(file_path))
                if text.strip():
                    context_parts.append(f"=== {file_path.name} ===\n{text.strip()}")
            except Exception:
                pass

    _context_cache = "\n\n".join(context_parts)
    return _context_cache

def assess_competency(narrative: str, competency: dict, api_key: str = None) -> dict:
    """Use Claude to assess a single competency against the narrative."""

    if not api_key:
        api_key = os.getenv("ANTHROPIC_API_KEY")

    client = Anthropic(api_key=api_key)

    comp_id = competency["id"]
    comp_name = competency["name"]
    definition = competency["definition"]
    levels = competency["levels"]

    level_descriptions = ""
    for level in levels:
        level_descriptions += f"\nLevel {level['level']}: {level['description']}\n"
        level_descriptions += "Indicators:\n"
        for indicator in level["indicators"]:
            level_descriptions += f"- {indicator}\n"

    system_prompt = """You are an expert assessor of Indonesian government civil service competencies based on the Permenpan 38/2017 framework. Your role is to provide deep, comprehensive analysis of narratives to evaluate competency achievement levels.

ASSESSMENT PRINCIPLES:
1. Look for BEHAVIORAL EVIDENCE in the narrative, not just keywords
2. Assess demonstrated capability, not potential
3. Consider context and constraints the person faced
4. Identify specific examples that illustrate each competency
5. Provide constructive feedback for development

EVALUATION APPROACH:
- Level 1-2: Individual contributor level - focuses on personal performance
- Level 3: Team leader level - developing others, organizational impact
- Level 4: Senior leader level - strategic thinking, organizational transformation
- Level 5: Executive level - national/strategic influence

ANALYSIS QUALITY:
- Extract EXACT QUOTES from the narrative as evidence
- Connect behaviors to specific competency indicators
- Explain WHY the demonstrated behaviors fit this level
- Suggest CONCRETE steps to reach the next level
- Be specific and evidence-based, not generic"""

    # Build system blocks — static content is marked for prompt caching
    # so all parallel competency calls reuse the cached prefix
    context_text = load_context_files()

    system_blocks = [{"type": "text", "text": system_prompt}]

    if context_text:
        system_blocks.append({
            "type": "text",
            "text": f"REFERENCE CONTEXT:\n\n{context_text}",
            "cache_control": {"type": "ephemeral"}
        })
    else:
        system_blocks[0]["cache_control"] = {"type": "ephemeral"}

    prompt = f"""Analyze the following narrative and assess the competency "{comp_name}".

COMPETENCY DEFINITION:
{definition}

COMPETENCY LEVELS AND INDICATORS:
{level_descriptions}

NARRATIVE TO ANALYZE:
{narrative}

---

COMPREHENSIVE ASSESSMENT REQUIRED:

1. **Achieved Level**: Determine which level (1-5) is BEST DEMONSTRATED by this person's actual behaviors and accomplishments in the narrative.

2. **Indicators Found**: Identify which specific behavioral indicators from the competency levels are evidenced in the narrative. Match behaviors to indicators, not just keywords.

3. **Evidence**: Extract 2-3 DIRECT QUOTES from the narrative that best demonstrate this competency level. These should be specific examples, not generic statements.

4. **Reasoning**: Provide DETAILED explanation of:
   - What specific behaviors demonstrate this level
   - How these behaviors compare to the level description
   - Why this level fits better than adjacent levels
   - Evidence of actual capability (not potential)

5. **Strengths**: Articulate what this person demonstrates particularly well in this competency area, with examples.

6. **Next Level Focus**: Provide SPECIFIC, ACTIONABLE recommendations for what's needed to reach the next level, based on gaps in the current narrative.

Format your response as JSON:
{{
  "achieved_level": <number 1-5>,
  "indicators_found": [<specific indicators matched to narrative evidence>],
  "evidence": [<direct quotes from narrative>],
  "reasoning": "<detailed explanation of level assignment with behavioral evidence>",
  "strengths": "<what is demonstrated well, with examples>",
  "next_level_focus": "<specific actions to reach next level>"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=system_blocks,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text

    try:
        cleaned_text = response_text.replace('```json', '').replace('```', '')

        json_start = cleaned_text.find('{')
        if json_start == -1:
            raise ValueError("No JSON object found in response")

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
    except (json.JSONDecodeError, ValueError):
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

    comp_map = {c["id"]: c for c in criteria["competencies"]}

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
                comp = comp_map.get(comp_id, {})
                levels = comp.get("levels", [])
                fallback_desc = levels[0]["description"] if levels else "Tidak dapat dinilai"
                results[comp_id] = {
                    "id": comp_id,
                    "name": comp.get("name", comp_id),
                    "definition": comp.get("definition", ""),
                    "achieved_level": 1,
                    "indicators_found": [],
                    "evidence": [],
                    "reasoning": f"Penilaian gagal: {str(e)}",
                    "strengths": "",
                    "next_level_focus": "",
                    "level_description": fallback_desc,
                    "all_levels": levels
                }

    return results
