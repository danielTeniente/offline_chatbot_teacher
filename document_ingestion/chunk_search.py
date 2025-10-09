from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util
import torch

# Load the embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_chunks_by_similarity(question: str, chunks: List[Dict[str, Any]], top_k: int = 3) -> List[str]:
    """
    Ranks chunks by semantic similarity to the question using precomputed chunk embeddings.

    Args:
        question (str): The user's question.
        chunks (List[Dict[str, any]]): List of chunks, each with "text" and "vector".
        top_k (int): Number of top relevant chunks to return.

    Returns:
        List[str]: Top-k most relevant chunk texts.
    """
    # Encode the question
    question_embedding = embedding_model.encode(question, convert_to_tensor=True)

    # Convert chunk vectors to tensor
    chunk_embeddings = torch.tensor([chunk["vector"] for chunk in chunks])

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(question_embedding, chunk_embeddings)[0]

    # Get top-k indices
    top_indices = similarities.argsort(descending=True)[:top_k]

    # Return the corresponding chunk texts
    return [chunks[i]["text"] for i in top_indices]

    