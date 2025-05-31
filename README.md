# 🚀 API Rekomendasi Kuliner Kota Jogja

API ini menyediakan tiga endpoint rekomendasi kuliner berbasis:
- **Content-Based**
- **Rule-Based**
- **Location-Based**

API ini dikembangkan menggunakan **Flask** dan memanfaatkan **TensorFlow** untuk pembuatan model machine learning.

---

## 📦 Cara Instalasi & Menjalankan Server

1. **Clone repositori ini**
   ```bash
   git clone https://github.com/cicipin/ml-api.git
   cd ml-api
   ```

2. **(Opsional) Buat virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan server**
   ```bash
   python main.py
   ```
   Server berjalan di: [http://localhost:5000](http://localhost:5000)

---

## 🔥 Contoh Request API

Semua endpoint menggunakan metode **POST** dengan format **JSON**.

---

### 📌 1. Content-Based Recommendation
**Endpoint:**  
```
/rekomendasi/content
```

**Contoh Request (curl):**
```bash
curl -X POST http://localhost:5000/rekomendasi/content \
     -H "Content-Type: application/json" \
     -d '{"toko_id": 12}'
```

**Contoh JSON Request:**
```json
{
  "toko_id": 12
}
```

**Contoh Response:**
```json
[
  {
    "toko_id": 15,
    "title": "Sate Pak Bondan",
    "type": "berat",
    "jenis": "sate",
    "rating": 4.7,
    "review": 230,
    "similarity_score": 0.935
  },
  {
    "toko_id": 23,
    "title": "Soto Ayam Bang Jali",
    "type": "berat",
    "jenis": "soto",
    "rating": 4.5,
    "review": 180,
    "similarity_score": 0.912
  }
]
```

---

### 📌 2. Rule-Based Recommendation
**Endpoint:**  
```
/rekomendasi/rule
```

**Contoh Request (curl):**
```bash
curl -X POST http://localhost:5000/rekomendasi/rule \
     -H "Content-Type: application/json" \
     -d '{"jenis": "soto"}'
```

**Contoh JSON Request:**
```json
{
  "jenis": "soto"
}
```

**Contoh Response:**
```json
[
  {
    "toko_id": 8,
    "title": "Soto Lamongan Cak Har",
    "type": "berat",
    "jenis": "soto",
    "rating": 4.8,
    "review": 250,
    "skor": 0.95
  },
  {
    "toko_id": 19,
    "title": "Soto Kudus Mbak Rini",
    "type": "berat",
    "jenis": "soto",
    "rating": 4.6,
    "review": 200,
    "skor": 0.92
  }
]
```

---

### 📌 3. Location-Based Recommendation
**Endpoint:**  
```
/rekomendasi/location
```

**Contoh Request (curl):**
```bash
curl -X POST http://localhost:5000/rekomendasi/location \
     -H "Content-Type: application/json" \
     -d '{"lat": -7.7705, "lon": 110.3775}'
```

**Contoh JSON Request:**
```json
{
  "lat": -7.7705,
  "lon": 110.3775
}
```

**Contoh Response:**
```json
[
  {
    "toko_id": 5,
    "title": "Bakso Pak Min",
    "type": "berat",
    "jenis": "bakso",
    "rating": 4.5,
    "review": 150,
    "jarak_km": 0.85,
    "skor": 0.91
  },
  {
    "toko_id": 12,
    "title": "Soto Bang Jali",
    "type": "berat",
    "jenis": "soto",
    "rating": 4.7,
    "review": 220,
    "jarak_km": 0.95,
    "skor": 0.89
  }
]
```

---

## 📎 File requirements.txt

```
flask
pandas
tensorflow
numpy
scikit-learn
```

---

## 📞 Kontak

Jika ada pertanyaan lebih lanjut, silakan hubungi:
- 📧 Email: mc008d5y2338@student.devacademy.id

---

Terima kasih telah menggunakan API ini! 🙌
