import os
import json
import numpy as np
from sklearn.cluster import KMeans
from document_ingestion.ocr_utils import sanitize_name

def load_chunks_and_embeddings(book_folder: str) -> tuple[list[str], np.ndarray]:
    chunks = []
    embeddings = []

    for fname in os.listdir(book_folder):
        if fname.endswith('.json'):
            with open(os.path.join(book_folder, fname), 'r', encoding='utf-8') as f:
                data = json.load(f)
                chunks.append(data['text'])
                embeddings.append(np.array(data['vector'], dtype=np.float32))

    return chunks, np.array(embeddings)

def get_central_chunks(chunks_path: str) -> str:
    book_folder = chunks_path
    book_name = os.path.basename(book_folder)

    # if already summarized, skip
    if os.path.exists(os.path.join(book_folder, 'central_chunks.txt')):
        return os.path.join(book_folder, 'central_chunks.txt')

    if not os.path.exists(book_folder):
        return f"Book folder '{book_folder}' does not exist."

    chunks, embeddings = load_chunks_and_embeddings(book_folder)
    num_chunks = len(chunks)

    if num_chunks == 0:
        return ""

    num_clusters = min(max(num_chunks // 10, 1), 15)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)

    closest_indices = []
    for center in kmeans.cluster_centers_:
        distances = np.linalg.norm(embeddings - center, axis=1)
        closest_indices.append(np.argmin(distances))

    summary_chunks = [chunks[i] for i in closest_indices]

    summary_path = os.path.join(book_folder, 'central_chunks.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        for chunk in summary_chunks:
            f.write(chunk + "\n\n")

    return summary_path

