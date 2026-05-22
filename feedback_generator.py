def generate_feedback(scores: dict) -> str:
    """Generate comprehensive AI-powered feedback."""
    feedback = "# 📋 LAPORAN PENILAIAN KOMPETENSI KOMPREHENSIF\n(Powered by Claude AI)\n\n"

    for comp_id in sorted(scores.keys()):
        result = scores[comp_id]
        name = result["name"]
        definition = result["definition"]
        level = result["achieved_level"]
        reasoning = result["reasoning"]
        strengths = result["strengths"]
        indicators_found = result["indicators_found"]
        evidence = result["evidence"]
        next_level_focus = result["next_level_focus"]
        all_levels = result["all_levels"]

        level_desc = next((lv["description"] for lv in all_levels if lv["level"] == level), "")

        feedback += f"## {name} (Level {level}/5)\n\n"
        feedback += f"**Definisi Kompetensi:**\n{definition}\n\n"
        feedback += f"**Deskripsi Level {level}:**\n{level_desc}\n\n"

        feedback += "### Analisis Komprehensif:\n\n"
        feedback += f"**Penilaian:** {reasoning}\n\n"
        feedback += f"**Kekuatan yang Ditunjukkan:** {strengths}\n\n"

        if indicators_found:
            feedback += "### Indikator Perilaku yang Teridentifikasi:\n"
            for i, indicator in enumerate(indicators_found[:5], 1):
                feedback += f"{i}. {indicator}\n"
            feedback += "\n"

        if evidence:
            feedback += "### Bukti dari Narasi:\n"
            for i, ev in enumerate(evidence[:3], 1):
                feedback += f"- \"{ev}\"\n"
            feedback += "\n"

        if level < 5:
            next_level = level + 1
            next_level_desc = next((lv["description"] for lv in all_levels if lv["level"] == next_level), "")

            feedback += f"### Untuk Mencapai Level {next_level}:\n"
            feedback += f"**Deskripsi Level {next_level}:** {next_level_desc}\n\n"
            feedback += f"**Fokus Pengembangan:** {next_level_focus}\n\n"

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
        bar = "█" * count + "░" * (total_competencies - count)
        summary += f"**Level {level}:** {bar} {count}/{total_competencies} ({percentage:.0f}%)\n"

    summary += "\n### Interpretasi Keseluruhan:\n"

    if avg_level >= 4.5:
        summary += "**Kinerja Luar Biasa (Exceptional)**\n"
        summary += "Menunjukkan kompetensi tinggi di semua area dengan kapabilitas untuk berperan sebagai role model dan agen perubahan di tingkat organisasi/nasional.\n"
    elif avg_level >= 3.5:
        summary += "**Kinerja Baik (Good)**\n"
        summary += "Menunjukkan kompetensi yang solid dengan inisiatif pengembangan yang jelas. Siap untuk peran kepemimpinan di tingkat unit kerja.\n"
    elif avg_level >= 2.5:
        summary += "**Kinerja Cukup (Adequate)**\n"
        summary += "Menunjukkan kompetensi dasar yang konsisten. Terdapat peluang pengembangan yang signifikan untuk mencapai tingkat yang lebih tinggi.\n"
    else:
        summary += "**Kinerja Perlu Ditingkatkan (Needs Improvement)**\n"
        summary += "Fokus pada penguatan kompetensi dasar dengan mentorship dan pengembangan berkelanjutan.\n"

    summary += "\n---\n"
    summary += "*Assessment powered by Claude AI - Sonnet 4.6*\n"
    return summary
