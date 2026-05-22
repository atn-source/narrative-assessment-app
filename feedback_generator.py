def generate_feedback(scores: dict) -> str:
    """Generate comprehensive feedback with evidence and indicators."""
    feedback = "# 📋 LAPORAN PENILAIAN KOMPETENSI KOMPREHENSIF\n\n"

    for comp_id in sorted(scores.keys()):
        result = scores[comp_id]
        name = result["name"]
        definition = result["definition"]
        level = result["achieved_level"]
        description = result["level_description"]
        indicators = result["indicators"]
        evidence = result["evidence"]
        matched = result["matched_count"]
        total = result["total_indicators"]

        feedback += f"## {name} (Level {level}/5)\n\n"
        feedback += f"**Definisi Kompetensi:**\n{definition}\n\n"
        feedback += f"**Deskripsi Level {level}:**\n{description}\n\n"
        feedback += f"**Tingkat Pencapaian Indikator:** {matched}/{total} indikator teridentifikasi ({int(matched/total*100)}%)\n\n"

        feedback += "### ✅ Indikator Perilaku yang Ditunjukkan:\n"
        for i, indicator in enumerate(indicators, 1):
            feedback += f"{i}. {indicator}\n"
        feedback += "\n"

        if evidence:
            feedback += "### 📌 Bukti dari Narasi:\n"
            for i, ev in enumerate(evidence[:3], 1):
                feedback += f"- \"{ev.strip()}\"\n"
            feedback += "\n"

        if level < 5:
            next_level = level + 1
            next_result = result["evidence_by_level"][next_level]
            next_description = next_result["description"]

            feedback += f"### 🎯 Untuk Mencapai Level {next_level}:\n"
            feedback += f"**Deskripsi Level {next_level}:** {next_description}\n\n"
            feedback += "**Indikator yang perlu dikembangkan:**\n"

            for indicator in next_result["indicators"]:
                feedback += f"- {indicator}\n"
            feedback += "\n"

        feedback += "---\n\n"

    return feedback

def generate_summary_feedback(scores: dict) -> str:
    """Generate overall summary and analysis."""
    total_competencies = len(scores)
    avg_level = sum(s["achieved_level"] for s in scores.values()) / total_competencies

    summary = "## 📈 RINGKASAN KESELURUHAN\n\n"
    summary += f"**Total Kompetensi Dinilai:** {total_competencies}\n"
    summary += f"**Rata-rata Level Pencapaian:** {avg_level:.1f}/5.0\n\n"

    level_counts = {}
    for result in scores.values():
        level = result["achieved_level"]
        level_counts[level] = level_counts.get(level, 0) + 1

    summary += "### Distribusi Pencapaian Level:\n"
    for level in sorted(level_counts.keys()):
        count = level_counts[level]
        percentage = (count / total_competencies) * 100
        bar_length = count
        bar = "█" * bar_length + "░" * (total_competencies - bar_length)
        summary += f"**Level {level}:** {bar} {count}/{total_competencies} ({percentage:.0f}%)\n"

    summary += "\n### 💡 Interpretasi:\n"

    if avg_level >= 4.5:
        summary += "- **Kinerja Luar Biasa:** Menunjukkan kompetensi tinggi di semua area dengan kapabilitas untuk berperan sebagai role model.\n"
    elif avg_level >= 3.5:
        summary += "- **Kinerja Baik:** Menunjukkan kompetensi solid dengan inisiatif pengembangan yang jelas ke level berikutnya.\n"
    elif avg_level >= 2.5:
        summary += "- **Kinerja Cukup:** Menunjukkan kompetensi dasar yang konsisten, dengan peluang pengembangan signifikan.\n"
    else:
        summary += "- **Kinerja Perlu Ditingkatkan:** Fokus pada penguatan kompetensi dasar untuk mencapai level yang lebih tinggi.\n"

    summary += "\n"
    return summary
