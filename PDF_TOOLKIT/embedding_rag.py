import os
import json
import uuid

import faiss
import numpy as np

from google import genai


class EmbeddingRAG:

    def __init__(self, storage_folder="vector_store"):

        self.client = genai.Client()

        self.storage_folder = storage_folder

        os.makedirs(
            self.storage_folder,
            exist_ok=True
        )


    # ==========================================
    # CREATE CHUNKS
    # ==========================================

    def create_chunks(
        self,
        pages,
        chunk_size=1200,
        overlap=200
    ):

        chunks = []

        for page_number, text in pages:

            text = text.strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = start + chunk_size

                chunk_text = text[start:end]

                chunks.append({
                    "page": page_number,
                    "text": chunk_text
                })

                if end >= len(text):
                    break

                start = end - overlap

        return chunks


    # ==========================================
    # CREATE EMBEDDING
    # ==========================================

    def get_embedding(self, text):

        result = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        vector = np.array(
            result.embeddings[0].values,
            dtype=np.float32
        )

        return vector

    def retrieve(self,document_id,question,top_k=5):

        index_path = os.path.join(self.storage_folder,f"{document_id}.index")

        metadata_path = os.path.join(self.storage_folder,f"{document_id}.json")


        if not os.path.exists(index_path):

            raise FileNotFoundError("Document index not found.")


        if not os.path.exists(metadata_path):

            raise FileNotFoundError("Document metadata not found.")


        # Load FAISS index

        index = faiss.read_index(index_path)


        # Load chunks

        with open(metadata_path,"r",encoding="utf-8") as file:

            chunks = json.load(file)


    # Create question embedding

        question_vector = self.get_embedding(question)


        question_vector = np.array([question_vector],dtype="float32")


        faiss.normalize_L2( question_vector)


    # Search vector index

        scores, indices = index.search(question_vector,top_k)


        results = []


        for score, index_number in zip(scores[0],indices[0]):

            if index_number == -1:
                continue


        chunk = chunks[
            int(index_number)
        ]


        results.append({

            "page":
                chunk["page"],

            "text":
                chunk["text"],

            "score":
                float(score)

        })


        return results


    # ==========================================
    # CREATE DOCUMENT INDEX
    # ==========================================

    def create_document_index(self, pages):

        chunks = self.create_chunks(pages)

        if not chunks:
            raise ValueError(
                "No readable text found in PDF."
            )

        embeddings = []

        print(
            f"Creating embeddings for "
            f"{len(chunks)} chunks..."
        )

        for number, chunk in enumerate(
            chunks,
            start=1
        ):

            print(
                f"Embedding "
                f"{number}/{len(chunks)}"
            )

            vector = self.get_embedding(
                chunk["text"]
            )

            embeddings.append(vector)


        # Convert list into NumPy matrix

        matrix = np.vstack(
            embeddings
        ).astype("float32")


        # Normalize vectors.
        #
        # Inner product on normalized vectors
        # behaves like cosine similarity.

        faiss.normalize_L2(matrix)


        dimension = matrix.shape[1]


        # Create FAISS index

        index = faiss.IndexFlatIP(
            dimension
        )


        # Add embeddings

        index.add(matrix)


        # Generate unique document ID

        document_id = str(
            uuid.uuid4()
        )


        # Paths

        index_path = os.path.join(
            self.storage_folder,
            f"{document_id}.index"
        )

        metadata_path = os.path.join(
            self.storage_folder,
            f"{document_id}.json"
        )


        # Save FAISS index

        faiss.write_index(
            index,
            index_path
        )


        # Save chunk text + page numbers

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chunks,
                file,
                ensure_ascii=False
            )


        print(
            "Vector index created:",
            document_id
        )


        return document_id