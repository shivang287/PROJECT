import re
from collections import Counter
import math


class PDFRAG:

    def __init__(self):
        self.chunks = []


    # -------------------------------
    # SPLIT PDF TEXT INTO CHUNKS
    # -------------------------------

    def create_chunks(self, pages, chunk_size=1200, overlap=200):

        self.chunks = []

        for page_number, text in pages:

            text = text.strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = start + chunk_size

                chunk_text = text[start:end]

                self.chunks.append({
                    "page": page_number,
                    "text": chunk_text
                })

                if end >= len(text):
                    break

                start = end - overlap

        return self.chunks


    # -------------------------------
    # TOKENIZE TEXT
    # -------------------------------

    def tokenize(self, text):

        return re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower()
        )


    # -------------------------------
    # COSINE SIMILARITY
    # -------------------------------

    def similarity(self, question, text):

        question_words = Counter(
            self.tokenize(question)
        )

        text_words = Counter(
            self.tokenize(text)
        )

        common_words = (
            set(question_words) &
            set(text_words)
        )

        numerator = sum(
            question_words[word] * text_words[word]
            for word in common_words
        )

        question_length = math.sqrt(
            sum(value ** 2 for value in question_words.values())
        )

        text_length = math.sqrt(
            sum(value ** 2 for value in text_words.values())
        )

        denominator = question_length * text_length

        if denominator == 0:
            return 0

        return numerator / denominator


    # -------------------------------
    # FIND RELEVANT CHUNKS
    # -------------------------------

    def retrieve(self, question, top_k=5):

        scored_chunks = []

        for chunk in self.chunks:

            score = self.similarity(
                question,
                chunk["text"]
            )

            scored_chunks.append({
                "page": chunk["page"],
                "text": chunk["text"],
                "score": score
            })

        scored_chunks.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return scored_chunks[:top_k]