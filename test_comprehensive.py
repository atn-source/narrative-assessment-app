from scorer import score_narrative
from feedback_generator import generate_feedback, generate_summary_feedback

with open('sample_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

scores = score_narrative(text)
feedback = generate_feedback(scores)
summary = generate_summary_feedback(scores)

with open('comprehensive_output.txt', 'w', encoding='utf-8') as f:
    f.write(feedback)
    f.write("\n\n")
    f.write(summary)

print('Comprehensive feedback generated successfully!')
print('Total competencies assessed: ' + str(len(scores)))
for idx, (comp_id, score) in enumerate(list(scores.items())[:5], 1):
    name = score['name']
    level = score['achieved_level']
    matched = score['matched_count']
    total = score['total_indicators']
    print(str(idx) + '. ' + name + ': Level ' + str(level) + '/5 (' + str(matched) + '/' + str(total) + ' indicators)')
