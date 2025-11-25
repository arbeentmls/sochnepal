from importlib import import_module

_transformers = import_module("transformers")
TextAnalysisPipeline = getattr(_transformers, "pipeline")


class EmotionAnalyzer:
    """
    Custom emotion detection system using pre-trained neural networks.
    Analyzes text sentiment across multiple emotional dimensions.
    """

    EMOTION_LABELS = [
        "anger",
        "disgust",
        "fear",
        "joy",
        "neutral",
        "sadness",
        "surprise",
    ]

    def __init__(self, model_id="j-hartmann/emotion-english-distilroberta-base"):
        """Initialize the emotion analysis model"""
        self._model_id = model_id
        self._pipeline = None
        self._initialize_model()

    def _initialize_model(self):
        """Load and configure the emotion classification model"""
        try:
            self._pipeline = TextAnalysisPipeline(
                "text-classification",
                model=self._model_id,
                return_all_scores=True,
            )
            print(f"Emotion analyzer initialized with model: {self._model_id}")
        except Exception as e:
            print(f"Failed to initialize emotion model: {e}")
            raise

    def _preprocess_text(self, text: str) -> str:
        """Clean and prepare text for analysis"""
        if not text:
            return ""
        # Remove extra whitespace
        text = " ".join(text.split())
        return text.strip()

    def analyze_single(self, text: str, top_k: int = 3) -> dict:
        """
        Analyze emotions in a single text passage

        Args:
            text: Input text to analyze
            top_k: Number of top emotions to return

        Returns:
            Dictionary with emotion scores and rankings
        """
        if not text or len(text.strip()) == 0:
            return {
                "text": text,
                "primary_emotion": "neutral",
                "confidence": 0.0,
                "emotion_distribution": {},
            }

        processed_text = self._preprocess_text(text)

        try:
            raw_scores = self._pipeline(processed_text)[0]

            sorted_emotions = sorted(raw_scores, key=lambda x: x["score"], reverse=True)

            primary = sorted_emotions[0]

            emotion_map = {
                emotion["label"]: round(emotion["score"], 3)
                for emotion in sorted_emotions[:top_k]
            }

            return {
                "text": text,
                "primary_emotion": primary["label"],
                "confidence": round(primary["score"], 3),
                "emotion_distribution": emotion_map,
                "all_scores": {
                    e["label"]: round(e["score"], 3) for e in sorted_emotions
                },
            }

        except Exception as e:
            print(f"Error analyzing emotion: {e}")
            return {
                "text": text,
                "primary_emotion": "unknown",
                "confidence": 0.0,
                "emotion_distribution": {},
                "error": str(e),
            }

    def analyze_batch(self, texts: list, include_all_scores: bool = False) -> list:
        """
        Analyze emotions in multiple texts efficiently

        Args:
            texts: List of text strings or report objects
            include_all_scores: Whether to include full emotion distribution

        Returns:
            List of emotion analysis results
        """
        results = []

        for item in texts:
            if hasattr(item, "content"):
                text = item.content
                original = item
            else:
                text = str(item)
                original = text

            analysis = self.analyze_single(text)

            result = {
                "text": original,
                "emotion": analysis["primary_emotion"],
                "score": analysis["confidence"],
            }

            if include_all_scores:
                result["all_emotions"] = analysis["emotion_distribution"]

            results.append(result)

        return results

    def get_emotional_context(self, texts: list) -> dict:
        """
        Analyze overall emotional context across multiple texts

        Returns aggregate statistics and dominant emotions
        """
        if not texts:
            return {"dominant_emotion": "neutral", "average_confidence": 0.0}

        analyses = self.analyze_batch(texts, include_all_scores=True)

        emotion_totals = {label: 0.0 for label in self.EMOTION_LABELS}

        for analysis in analyses:
            primary = analysis["emotion"]
            score = analysis["score"]
            emotion_totals[primary] += score

        dominant = max(emotion_totals.items(), key=lambda x: x[1])

        avg_confidence = sum(a["score"] for a in analyses) / len(analyses)

        return {
            "dominant_emotion": dominant[0],
            "dominant_score": round(dominant[1] / len(texts), 3),
            "average_confidence": round(avg_confidence, 3),
            "emotion_breakdown": {
                k: round(v / len(texts), 3) for k, v in emotion_totals.items()
            },
            "total_analyzed": len(texts),
        }


emotion_analyzer = EmotionAnalyzer()


def detect_emotions(reports):
    return emotion_analyzer.analyze_batch(reports, include_all_scores=True)
