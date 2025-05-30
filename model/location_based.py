import numpy as np
import pandas as pd
import tensorflow as tf

def hitung_jarak(lat1, lon1, lat2_array, lon2_array):
    R = 6371  # Radius bumi dalam kilometer
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2_array)
    lon2 = np.radians(lon2_array)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def rekomendasi_location_based(df, user_lat, user_lon, radius_km=1.0, top_n=10, w_rating=0.7, w_review=0.3):
    # Hitung jarak dari user ke semua toko
    jarak_km = hitung_jarak(user_lat, user_lon, df["Latitude"].values, df["Longitude"].values)
    df = df.copy()
    df["jarak_km"] = jarak_km

    # Filter toko dalam radius tertentu
    df_dalam_radius = df[df["jarak_km"] <= radius_km].copy()

    if df_dalam_radius.empty:
        print(f"Tidak ada toko dalam radius {radius_km} km.")
        return pd.DataFrame()

    # Normalisasi rating dan review
    rating = tf.constant(df_dalam_radius["Rating"].values, dtype=tf.float32)
    review = tf.constant(df_dalam_radius["Review"].values, dtype=tf.float32)

    rating_norm = (rating - tf.reduce_min(rating)) / (tf.reduce_max(rating) - tf.reduce_min(rating))
    review_norm = (review - tf.reduce_min(review)) / (tf.reduce_max(review) - tf.reduce_min(review))

    skor = (w_rating * rating_norm) + (w_review * review_norm)
    df_dalam_radius["skor"] = skor.numpy()

    # Urutkan berdasarkan skor
    rekomendasi = df_dalam_radius.sort_values(by="skor", ascending=False).head(top_n)

    return rekomendasi.reset_index(drop=True)