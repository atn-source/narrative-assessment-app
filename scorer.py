import json
import re
from pathlib import Path
from collections import defaultdict

def load_criteria():
    criteria_path = Path(__file__).parent / "scoring-criteria.json"
    with open(criteria_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_evidence(text: str, indicators: list) -> list:
    """Extract sentences from narrative that match behavioral indicators."""
    sentences = re.split(r'[.!?]+', text)
    evidence = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 20:
            continue

        for indicator in indicators:
            indicator_words = set(indicator.lower().split())
            sentence_words = set(sentence.lower().split())
            overlap = len(indicator_words & sentence_words)

            if overlap >= 2 and len(sentence) < 300:
                evidence.append(sentence)
                break

    return evidence[:3]

def score_narrative(text: str) -> dict:
    """Score narrative against competency framework with improved keyword matching."""
    criteria = load_criteria()
    results = {}
    text_lower = text.lower()

    for comp in criteria["competencies"]:
        comp_id = comp["id"]
        comp_name = comp["name"]
        definition = comp["definition"]

        achieved_level = 1
        evidence_by_level = {}

        for lv in comp["levels"]:
            level_num = lv["level"]
            indicators = lv["indicators"]
            description = lv["description"]

            indicator_matches = 0
            evidence = []

            for indicator in indicators:
                indicator_lower = indicator.lower()
                indicator_words = set(indicator_lower.split())

                matched = False
                for word in indicator_words:
                    if len(word) > 3 and word in text_lower:
                        matched = True
                        break

                if matched:
                    indicator_matches += 1
                    evidence.extend(extract_evidence(text, [indicator]))

            indicator_coverage = indicator_matches / len(indicators) if indicators else 0

            evidence_by_level[level_num] = {
                "description": description,
                "indicators": indicators,
                "matched": indicator_matches,
                "coverage": indicator_coverage,
                "evidence": list(set(evidence))
            }

            if indicator_coverage >= 0.33:
                achieved_level = level_num

        results[comp_id] = {
            "name": comp_name,
            "definition": definition,
            "achieved_level": achieved_level,
            "evidence_by_level": evidence_by_level,
            "level_description": evidence_by_level[achieved_level]["description"],
            "indicators": evidence_by_level[achieved_level]["indicators"],
            "evidence": evidence_by_level[achieved_level]["evidence"],
            "matched_count": evidence_by_level[achieved_level]["matched"],
            "total_indicators": len(evidence_by_level[achieved_level]["indicators"])
        }

    return results

def format_score_summary(scores: dict) -> str:
    """Format score summary table."""
    summary = "## 📊 Ringkasan Pencapaian Kompetensi\n\n"
    summary += "| No. | Kompetensi | Level | Deskripsi |\n"
    summary += "|-----|-----------|-------|----------|\n"

    for idx, comp_id in enumerate(sorted(scores.keys()), 1):
        result = scores[comp_id]
        name = result["name"]
        level = result["achieved_level"]
        desc = result["level_description"]
        summary += f"| {idx} | {name} | **{level}/5** | {desc} |\n"

    return summary
