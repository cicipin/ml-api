import pandas as pd
import tensorflow as tf

def rekomendasi_rule_based(df, jenis_pilihan, top_n=10, w_rating=0.7, w_review=0.3):
    # Filter hanya yang sesuai jenis
    df_filtered = df[df["jenis"].str.lower() == jenis_pilihan.lower()].copy()

    if df_filtered.empty:
        print("Jenis makanan tidak ditemukan.")
        return pd.DataFrame()

    # Normalisasi rating dan review
    rating = tf.constant(df_filtered["Rating"].values, dtype=tf.float32)
    review = tf.constant(df_filtered["Review"].values, dtype=tf.float32)

    rating_norm = (rating - tf.reduce_min(rating)) / (tf.reduce_max(rating) - tf.reduce_min(rating))
    review_norm = (review - tf.reduce_min(review)) / (tf.reduce_max(review) - tf.reduce_min(review))

    # Hitung skor akhir
    skor = (w_rating * rating_norm) + (w_review * review_norm)

    df_filtered["skor"] = skor.numpy()
    df_sorted = df_filtered.sort_values(by="skor", ascending=False).head(top_n)

    return df_sorted.reset_index(drop=True)