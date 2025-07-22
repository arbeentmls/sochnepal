from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
)


def detect_emotions(reports):
    # reports = [
    #     "This garbage problem is making me so angry.",
    #     "I feel really sad that nothing has changed in my ward.",
    #     "Thank you for the quick response!",
    #     "I'm scared the electric wires might fall down.",
    #     "Ward office is useless. Tired of complaining.",
    # ]
    results = []
    for report in reports:
        scores = emotion_classifier(report.content)[0]
        sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
        top_emotion = sorted_scores[0]
        results.append(
            {
                "text": report,
                "emotion": top_emotion["label"],
                "score": round(top_emotion["score"], 2),
                "all_emotions": {
                    e["label"]: round(e["score"], 3) for e in sorted_scores
                },
            }
        )

    return results
