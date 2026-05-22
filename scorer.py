import json
import re
from pathlib import Path

def load_criteria():
    criteria_path = Path(__file__).parent / "scoring-criteria.json"
    with open(criteria_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def score_narrative(text: str) -> dict:
    criteria = load_criteria()
    results = {}

    text_lower = text.lower()

    for comp in criteria["competencies"]:
        comp_id = comp["id"]
        comp_name = comp["name"]
        comp_keywords = [comp_name.lower()] + [ind.lower() for level in comp["levels"] for ind in level["indicators"]]

        keyword_matches = sum(1 for keyword in comp_keywords if keyword in text_lower)
        relevance_score = min(keyword_matches / max(len(comp_keywords), 1), 1.0)

        level = 1
        for lv in comp["levels"]:
            indicators = [ind.lower() for ind in lv["indicators"]]
            indicator_matches = sum(1 for ind in indicators if ind in text_lower)
            indicator_coverage = indicator_matches / len(indicators) if indicators else 0

            if indicator_coverage >= 0.5 and relevance_score > 0.2:
                level = lv["level"]

        results[comp_id] = {
            "name": comp_name,
            "achieved_level": level,
            "level_description": comp["levels"][level - 1]["description"],
            "indicators": comp["levels"][level - 1]["indicators"],
            "relevance_score": relevance_score
        }

    return results

def format_score_summary(scores: dict) -> str:
    summary = "## 📊 Ringkasan Pencapaian Kompetensi\n\n"
    summary += "| Kompetensi | Level Pencapaian | Deskripsi |\n"
    summary += "|-----------|-----------------|----------|\n"

    for comp_id in sorted(scores.keys()):
        result = scores[comp_id]
        name = result["name"]
        level = result["achieved_level"]
        desc = result["level_description"]
        summary += f"| {name} | **Level {level}** | {desc} |\n"

    return summary
