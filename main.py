from flask import Flask, request, jsonify
from flask_cors import CORS  # Tambahkan ini
import pandas as pd
from model.content_based import rekomendasi_content_based
from model.rule_based import rekomendasi_rule_based
from model.location_based import rekomendasi_location_based

app = Flask(__name__)
CORS(app)

# Load DataFrame sekali saja
data = pd.read_csv("dataset/data_siap_model.csv")

@app.route("/rekomendasi/content", methods=["POST"])
def content_route():
    toko_id = request.json.get("toko_id")
    if toko_id is None:
        return jsonify({"error": "Parameter 'toko_id' harus disediakan"}), 400

    result = rekomendasi_content_based(data, toko_id)

    # Jika tidak ada hasil
    if isinstance(result, list) and len(result) == 0:
        return jsonify({"error": "toko_id tidak ditemukan"}), 404

    return jsonify(result.to_dict(orient="records"))

@app.route("/rekomendasi/rule", methods=["POST"])
def rule_route():
    jenis = request.json.get("jenis")
    if not jenis:
        return jsonify({"error": "Parameter 'jenis' harus disediakan"}), 400

    result = rekomendasi_rule_based(data, jenis)

    if result.empty:
        return jsonify({"error": "Jenis makanan tidak ditemukan"}), 404

    return jsonify(result.to_dict(orient="records"))

@app.route("/rekomendasi/location", methods=["POST"])
def location_route():
    try:
        lat = float(request.json.get("lat"))
        lon = float(request.json.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"error": "Parameter 'lat' dan 'lon' harus berupa angka"}), 400

    # Parameter opsional
    radius_km = float(request.json.get("radius_km", 2.0))
    top_n = int(request.json.get("top_n", 10))
    w_rating = float(request.json.get("w_rating", 0.7))
    w_review = float(request.json.get("w_review", 0.3))

    result = rekomendasi_location_based(data, lat, lon, radius_km=radius_km, top_n=top_n, w_rating=w_rating, w_review=w_review)

    if result.empty:
        return jsonify({"error": f"Tidak ada toko dalam radius {radius_km} km"}), 404

    return jsonify(result.to_dict(orient="records"))


if __name__ == "__main__":
    app.run()