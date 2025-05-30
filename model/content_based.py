import pandas as pd
import tensorflow as tf
import numpy as np

def rekomendasi_content_based(df, toko_id, top_n=10):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Lookup layers
    type_lookup = tf.keras.layers.StringLookup(vocabulary=df["type"].unique(), output_mode="one_hot")
    jenis_lookup = tf.keras.layers.StringLookup(vocabulary=df["jenis"].unique(), output_mode="one_hot")

    # Encode kategori
    type_encoded = type_lookup(tf.constant(df["type"].values))
    jenis_encoded = jenis_lookup(tf.constant(df["jenis"].values))

    # Normalisasi rating dan review
    rating = tf.constant(df["rating"].values, dtype=tf.float32)
    review = tf.constant(df["review"].values, dtype=tf.float32)

    rating_norm = (rating - tf.reduce_min(rating)) / (tf.reduce_max(rating) - tf.reduce_min(rating))
    review_norm = (review - tf.reduce_min(review)) / (tf.reduce_max(review) - tf.reduce_min(review))

    # Casting kategori ke float32
    type_encoded = tf.cast(type_encoded, tf.float32)
    jenis_encoded = tf.cast(jenis_encoded, tf.float32)

    # Gabungkan semua fitur
    item_vectors = tf.concat([
        type_encoded,
        jenis_encoded,
        tf.expand_dims(rating_norm, axis=1),
        tf.expand_dims(review_norm, axis=1),
    ], axis=1)

    # Temukan index item referensi dari toko_id
    try:
        index = df[df["toko_id"] == toko_id].index[0]
    except IndexError:
        print("toko_id tidak ditemukan.")
        return []

    query_vector = tf.repeat(tf.expand_dims(item_vectors[index], axis=0), repeats=item_vectors.shape[0], axis=0)

    # Cosine similarity
    def cosine_similarity(a, b):
        a = tf.cast(a, tf.float32)
        b = tf.cast(b, tf.float32)
        dot = tf.reduce_sum(a * b, axis=1)
        norm_a = tf.norm(a, axis=1)
        norm_b = tf.norm(b, axis=1)
        return dot / (norm_a * norm_b)

    similarity = cosine_similarity(query_vector, item_vectors)

    # Urutkan dan ambil top_n (selain dirinya sendiri)
    sorted_indices = tf.argsort(similarity, direction="DESCENDING").numpy()
    top_indices = sorted_indices[:top_n]

    # Ubah code diatas persis menjadi dibawah ini jika ingin selain dirinya sendiri
    # top_indices = [i for i in sorted_indices if i != index][:top_n]

    hasil = df.iloc[top_indices].copy()
    hasil["similarity_score"] = [similarity[i].numpy() for i in top_indices]

    return hasil.reset_index(drop=True)