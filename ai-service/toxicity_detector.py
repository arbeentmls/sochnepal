import os
import pickle
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from .custom_toxicity_classifier import CustomToxicityClassifier

BASE_DIR = Path(__file__).parent


class ToxicityDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.profanity_words = self._load_profanity_words()
        self._load_or_train_model()

    def _load_profanity_words(self):
        """Basic profanity word list"""
        return {
            "fuck",
            "shit",
            "damn",
            "bitch",
            "asshole",
            "stupid",
            "idiot",
            "hate",
            "kill",
            "die",
            "retard",
            "gay",
            "fag",
            "nigger",
        }

    def _preprocess_text(self, text):
        """Clean text"""
        text = text.lower().strip()
        text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special chars
        text = re.sub(r"\s+", " ", text)  # Remove extra spaces
        return text

    def _load_or_train_model(self):
        """Load existing model or train new one"""
        model_path = os.path.join(BASE_DIR, "toxicity_model.pkl")

        if os.path.exists(model_path):
            try:
                with open(model_path, "rb") as f:
                    save_data = pickle.load(f)

                # Handle both old and new save formats
                if isinstance(save_data, tuple):
                    # Old format: (model, vectorizer)
                    self.model, self.vectorizer = save_data
                    self.category_models = {}
                    self.toxicity_categories = []
                else:
                    # New format: dictionary
                    self.model = save_data.get("model")
                    self.vectorizer = save_data.get("vectorizer")
                    self.category_models = save_data.get("category_models", {})
                    self.toxicity_categories = save_data.get("toxicity_categories", [])

                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                self._train_model()
        else:
            self._train_model()

    def _train_model(self):
        """Train model using Kaggle dataset"""
        try:
            # Load the Kaggle dataset
            csv_path = os.path.join(BASE_DIR, "data", "train.csv")
            df = pd.read_csv(csv_path)

            print(f"Dataset shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")

            # Check if we have the full Kaggle dataset with toxicity categories
            toxicity_columns = [
                "toxic",
                "severe_toxic",
                "obscene",
                "threat",
                "insult",
                "identity_hate",
            ]
            has_toxicity_labels = all(col in df.columns for col in toxicity_columns)

            if has_toxicity_labels:
                # Use the full dataset with category labels
                texts = df["comment_text"].values
                labels = df[toxicity_columns].values
                self.toxicity_categories = toxicity_columns

                # For training, use any toxicity as positive label
                binary_labels = (df[toxicity_columns].sum(axis=1) > 0).astype(int)
                print(f"Found toxicity categories: {toxicity_columns}")

            else:
                # Fallback logic for datasets without categories
                text_column = "comment_text" if "comment_text" in df.columns else None
                label_column = "toxic" if "toxic" in df.columns else None

                if text_column is None or label_column is None:
                    raise ValueError(
                        f"Required columns not found. Available: {list(df.columns)}"
                    )

                texts = df[text_column].values
                binary_labels = df[label_column].values
                self.toxicity_categories = []

            # Rest of preprocessing...
            mask = pd.notna(texts)
            texts = texts[mask]
            binary_labels = binary_labels[mask]

            if has_toxicity_labels:
                labels = labels[mask]

            texts = [self._preprocess_text(str(text)) for text in texts]

            # Use subset for faster training
            if len(texts) > 50000:
                texts = texts[:50000]
                binary_labels = binary_labels[:50000]
                if has_toxicity_labels:
                    labels = labels[:50000]

            print(f"Training with {len(texts)} samples")

            # Check class distribution before splitting
            unique_labels, counts = np.unique(binary_labels, return_counts=True)
            print(f"Label distribution: {dict(zip(unique_labels, counts))}")

            # Only use stratify if we have enough samples per class
            min_class_size = min(counts)
            use_stratify = min_class_size >= 2

            if not use_stratify:
                print(
                    "Warning: Insufficient samples for stratified split. Using random split."
                )

            # Train multiple models if we have categories
            if has_toxicity_labels:
                self.category_models = {}

                # Initialize vectorizer once
                self.vectorizer = TfidfVectorizer(
                    max_features=10000,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.95,
                )

                for i, category in enumerate(toxicity_columns):
                    print(f"Training model for {category}...")
                    category_labels = labels[:, i]

                    # Check if this category has enough samples
                    unique_cat_labels, cat_counts = np.unique(
                        category_labels, return_counts=True
                    )
                    cat_min_size = min(cat_counts) if len(cat_counts) > 1 else 0

                    if cat_min_size < 2:
                        print(
                            f"Skipping {category} - insufficient samples ({cat_counts})"
                        )
                        continue

                    # Split data for this category
                    try:
                        if cat_min_size >= 2:
                            X_train, X_test, y_train, y_test = train_test_split(
                                texts,
                                category_labels,
                                test_size=0.2,
                                random_state=42,
                                stratify=category_labels,
                            )
                        else:
                            X_train, X_test, y_train, y_test = train_test_split(
                                texts, category_labels, test_size=0.2, random_state=42
                            )
                    except ValueError as e:
                        print(f"Error splitting data for {category}: {e}")
                        continue

                    # Vectorize (fit on first model, transform on others)
                    if i == 0:
                        X_train_vec = self.vectorizer.fit_transform(X_train)
                    else:
                        X_train_vec = self.vectorizer.transform(X_train)

                    # Train category-specific model
                    model = CustomToxicityClassifier(random_state=42, max_iter=1000)
                    model.fit(X_train_vec, y_train)

                    self.category_models[category] = model

                    # Evaluate
                    X_test_vec = self.vectorizer.transform(X_test)
                    accuracy = model.score(X_test_vec, y_test)
                    print(f"{category} model accuracy: {accuracy:.3f}")

                # Also train general toxicity model
                try:
                    if use_stratify:
                        X_train, X_test, y_train, y_test = train_test_split(
                            texts,
                            binary_labels,
                            test_size=0.2,
                            random_state=42,
                            stratify=binary_labels,
                        )
                    else:
                        X_train, X_test, y_train, y_test = train_test_split(
                            texts, binary_labels, test_size=0.2, random_state=42
                        )

                    X_train_vec = self.vectorizer.transform(X_train)
                    self.model = CustomToxicityClassifier(
                        random_state=42, max_iter=1000
                    )
                    self.model.fit(X_train_vec, y_train)

                    # Evaluate general model
                    X_test_vec = self.vectorizer.transform(X_test)
                    accuracy = self.model.score(X_test_vec, y_test)
                    print(f"General toxicity model accuracy: {accuracy:.3f}")

                except Exception as e:
                    print(f"Error training general model: {e}")

            else:
                # Train single model as before
                try:
                    if use_stratify:
                        X_train, X_test, y_train, y_test = train_test_split(
                            texts,
                            binary_labels,
                            test_size=0.2,
                            random_state=42,
                            stratify=binary_labels,
                        )
                    else:
                        X_train, X_test, y_train, y_test = train_test_split(
                            texts, binary_labels, test_size=0.2, random_state=42
                        )

                    self.vectorizer = TfidfVectorizer(
                        max_features=10000,
                        stop_words="english",
                        ngram_range=(1, 2),
                        min_df=2,
                        max_df=0.95,
                    )
                    X_train_vec = self.vectorizer.fit_transform(X_train)

                    self.model = CustomToxicityClassifier(
                        random_state=42, max_iter=1000
                    )
                    self.model.fit(X_train_vec, y_train)

                    # Evaluate
                    X_test_vec = self.vectorizer.transform(X_test)
                    accuracy = self.model.score(X_test_vec, y_test)
                    print(f"Model accuracy: {accuracy:.3f}")

                    self.category_models = {}

                except Exception as e:
                    print(f"Error in single model training: {e}")
                    raise

            # Save model
            os.makedirs(
                os.path.dirname(os.path.join(BASE_DIR, "toxicity_model.pkl")),
                exist_ok=True,
            )

            # Save both general model and category models
            save_data = {
                "model": self.model,
                "vectorizer": self.vectorizer,
                "category_models": getattr(self, "category_models", {}),
                "toxicity_categories": getattr(self, "toxicity_categories", []),
            }

            with open(os.path.join(BASE_DIR, "toxicity_model.pkl"), "wb") as f:
                pickle.dump(save_data, f)

            print("Model trained and saved successfully")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            print("Using synthetic data instead")
            self._train_synthetic_model()

    def _train_synthetic_model(self):
        """Fallback training with synthetic data"""
        # Synthetic data with balanced classes
        toxic_comments = [
            "you are so fucking stupid",
            "i hate you go kill yourself",
            "this is complete shit",
            "you're an idiot and a loser",
            "shut the fuck up bitch",
        ] * 200  # Increase to 1000 samples

        clean_comments = [
            "this is a great post thanks for sharing",
            "i really appreciate your help",
            "looking forward to more updates",
            "this is very informative",
            "great work keep it up",
        ] * 200  # Increase to 1000 samples

        texts = toxic_comments + clean_comments
        labels = [1] * len(toxic_comments) + [0] * len(clean_comments)
        texts = [self._preprocess_text(text) for text in texts]

        print(f"Training with synthetic data: {len(texts)} samples")

        # Split data with stratification (now we have enough samples)
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # Vectorize
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
        )
        X_train_vec = self.vectorizer.fit_transform(X_train)

        # Train model
        self.model = CustomToxicityClassifier(random_state=42, max_iter=1000)
        self.model.fit(X_train_vec, y_train)

        # Evaluate
        X_test_vec = self.vectorizer.transform(X_test)
        accuracy = self.model.score(X_test_vec, y_test)
        print(f"Synthetic model accuracy: {accuracy:.3f}")

        self.category_models = {}
        self.toxicity_categories = []

        # Save model
        save_data = {
            "model": self.model,
            "vectorizer": self.vectorizer,
            "category_models": {},
            "toxicity_categories": [],
        }

        with open(os.path.join(BASE_DIR, "toxicity_model.pkl"), "wb") as f:
            pickle.dump(save_data, f)

        print("Synthetic model trained and saved successfully")

    def detect_toxicity(self, text, threshold=0.5):
        """Main detection method with specific toxicity categories"""
        if not text or len(text.strip()) == 0:
            return False, 0.0, []

        processed_text = self._preprocess_text(text)

        # Rule-based check
        profanity_found = []
        words = processed_text.split()
        for word in words:
            if word in self.profanity_words:
                profanity_found.append(word)

        # ML predictions for categories
        detected_categories = {}
        category_scores = {}

        if hasattr(self, "category_models") and self.category_models:
            # Use category-specific models
            try:
                text_vec = self.vectorizer.transform([processed_text])

                for category, model in self.category_models.items():
                    score = model.predict_proba(text_vec)[0][1]
                    category_scores[category] = score

                    if score > threshold:
                        detected_categories[category] = score
            except:
                pass

        # General ML prediction
        ml_score = 0.0
        if self.model and self.vectorizer:
            try:
                text_vec = self.vectorizer.transform([processed_text])
                ml_score = self.model.predict_proba(text_vec)[0][1]
            except:
                ml_score = 0.0

        # Combine scores
        profanity_score = min(len(profanity_found) * 0.3, 1.0)
        final_score = max(profanity_score, ml_score)

        is_toxic = final_score >= threshold or len(detected_categories) > 0
        reasons = []

        # Add specific reasons based on detected categories
        if profanity_found:
            reasons.append(f"Contains profanity: {', '.join(profanity_found)}")

        if detected_categories:
            # Map categories to readable reasons
            category_map = {
                "toxic": "General toxicity",
                "severe_toxic": "Severe toxicity",
                "obscene": "Obscene language",
                "threat": "Threatening language",
                "insult": "Insulting content",
                "identity_hate": "Identity-based hate",
            }

            for category, score in detected_categories.items():
                readable_name = category_map.get(category, category)
                reasons.append(f"{readable_name} (confidence: {score:.2f})")

        elif ml_score > threshold:
            reasons.append(f"General toxicity detected (confidence: {ml_score:.2f})")

        return is_toxic, final_score, reasons


# Global instance
detector = ToxicityDetector()
