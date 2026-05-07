import hashlib
import numpy as np

VECTOR_DIM = 64  # fixed size (important)


def get_embedding(text: str):
    """
    Lightweight deterministic embedding using hashing.
    No external models, no downloads.
    """

    words = text.lower().split()
    vector = np.zeros(VECTOR_DIM)

    for word in words:
        hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
        index = hash_val % VECTOR_DIM
        vector[index] += 1.0

    return vector.astype("float32")