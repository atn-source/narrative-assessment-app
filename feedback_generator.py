def generate_feedback(scores: dict, narrative: str) -> str:
    feedback = "# 📋 Laporan Feedback Kompetensi\n\n"
    feedback += "---\n\n"

    for comp_id in sorted(scores.keys()):
        result = scores[comp_id]
        name = result["name"]
        level = result["achieved_level"]
        description = result["level_description"]
        indicators = result["indicators"]

        feedback += f"## {name} (Level {level}/5)\n\n"
        feedback += f"**Deskripsi Pencapaian:** {description}\n\n"

        feedback += "### Indikator Perilaku yang Ditunjukkan:\n"
        for i, indicator in enumerate(indicators, 1):
            feedback += f"- {indicator}\n"

        feedback += "\n"

        if level < 5:
            next_level = level + 1
            feedback += f"### Untuk Mencapai Level {next_level}:\n"
            feedback += "Fokus pada pengembangan aspek-aspek berikut:\n"

            if next_level == 2:
                feedback += f"- Mulai mengingatkan dan mengajak rekan kerja untuk menerapkan prinsip {name}\n"
                feedback += "- Tunjukkan inisiatif dalam menyebarkan nilai-nilai positif kepada tim\n"
            elif next_level == 3:
                feedback += f"- Memastikan semua orang yang Anda pimpin menerapkan {name} secara konsisten\n"
                feedback += "- Lakukan monitoring dan evaluasi rutin atas penerapannya\n"
            elif next_level == 4:
                feedback += f"- Ciptakan lingkungan kerja yang mendorong penerapan {name} secara organisatoris\n"
                feedback += "- Bangun sistem dan proses yang memfasilitasi pencapaian level ini\n"
            elif next_level == 5:
                feedback += f"- Jadilah role model dalam penerapan {name}\n"
                feedback += "- Buat kebijakan strategis yang berdampak di level instansi/nasional\n"

            feedback += "\n"

        feedback += "---\n\n"

    return feedback

def generate_summary_feedback(scores: dict) -> str:
    total_competencies = len(scores)
    avg_level = sum(s["achieved_level"] for s in scores.values()) / total_competencies

    summary = f"## Ringkasan Keseluruhan\n\n"
    summary += f"**Total Kompetensi:** {total_competencies}\n"
    summary += f"**Rata-rata Level Pencapaian:** {avg_level:.1f}/5\n\n"

    level_counts = {}
    for result in scores.values():
        level = result["achieved_level"]
        level_counts[level] = level_counts.get(level, 0) + 1

    summary += "### Distribusi Level:\n"
    for level in sorted(level_counts.keys()):
        count = level_counts[level]
        bar = "█" * count + "░" * (total_competencies - count)
        summary += f"Level {level}: {bar} ({count}/{total_competencies})\n"

    summary += "\n"
    return summary
