# 📡 Monitoring Backend (Development Setup)

Backend ini dibangun menggunakan **FastAPI** sebagai API utama untuk sistem monitoring (Zabbix-style data + Grafana-style visualization).

Dokumen ini fokus pada:

* Menjalankan backend secara lokal (tanpa Docker)
* Dokumentasi endpoint lengkap
* Mapping ke kebutuhan UI multi-panel

---

# 🚀 Tujuan Sistem

Backend ini bertugas untuk:

* Menyediakan API data monitoring
* Mengelola data host & metrik
* Menyediakan data time-series
* Menyediakan summary harian & report periodik

---

# 🧱 Tech Stack

* FastAPI
* SQLAlchemy
* Alembic
* MySQL / PostgreSQL

---

# 📁 Struktur Project

```
monitoring-backend/
│
├── app/
│   ├── api/        # Endpoint API
│   ├── core/       # Konfigurasi aplikasi
│   ├── db/         # Koneksi database
│   ├── models/     # Model ORM
│   ├── schemas/    # Schema (Pydantic)
│   ├── service/    # Business logic
│   └── main.py     # Entry point
│
├── migrations/     # Alembic migration
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup Environment

## 1. Virtual Environment

```bash
python -m venv venv
```

## 2. Aktivasi

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

## 3. Install Dependency

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Buat file `.env`:

Copy isi file `.env.example` ke `.env`.

---

# 🗄️ Database Migration

## Jalankan Migration

```bash
alembic upgrade head
```

## Buat Migration Baru

```bash
alembic revision --autogenerate -m "your message"
```

---

# ▶️ Menjalankan Backend

```bash
uvicorn app.main:app --reload
```

Akses:

* API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# 📡 BASE URL

```
http://127.0.0.1:8000
```

---

# 🖥️ HOSTS API

## Get All Hosts

```
GET http://127.0.0.1:8000/api/hosts/
```

## Update Host Location

```
PUT http://127.0.0.1:8000/api/hosts/{host_id}/location
```

---

# 📊 ITEMS API

## Get Items By Host

```
GET http://127.0.0.1:8000/api/items/host/{host_id}
```

## Get Item History (Time-Series)

```
GET http://127.0.0.1:8000/api/items/{item_id}/history
```

## Get Last Value (Realtime)

```
GET http://127.0.0.1:8000/api/items/{item_id}/last
```

---

# 🔐 AUTH API

## Login

```
POST http://127.0.0.1:8000/api/auth/login
```

Body:

```json
{
  "username": "admin",
  "password": "admin"
}
```

---

# 📑 SUMMARY API

## Get Summary Report

```
GET http://127.0.0.1:8000/api/summary/report
```

Query:

* range=today
* range=7d
* start=YYYY-MM-DD
* end=YYYY-MM-DD

---

# 📊 RESPONSE FORMAT (SUMMARY)

```json
{
  "device": "server-01",
  "date": "2025-01-01",
  "cpu": {"min": 10, "max": 90, "avg": 45},
  "memory": {"min": 30, "max": 80, "avg": 60},
  "bandwidth": {"min": 100, "max": 900, "avg": 400}
}
```

---

# 🔁 DATA FLOW

```
Zabbix / Agent → Database → FastAPI → Frontend
```

---

# 🎯 MAPPING KE UI

| UI Component  | Endpoint                        |
| ------------- | ------------------------------- |
| Device List   | /api/hosts/                     |
| Metrics Panel | /api/items/host/{host_id}       |
| Chart         | /api/items/{item_id}/history    |
| Realtime      | /api/items/{item_id}/last       |
| Daily Summary | /api/summary/report?range=today |
| Report        | /api/summary/report             |

---

# ⚠️ CATATAN

* Database wajib aktif
* Migration harus sync
* Gunakan env (jangan hardcode)

---

# 👨‍💻 NOTES

Backend ini sudah siap untuk:

* Multi-panel UI
* Monitoring real-time
* Grafik historis
* Daily & monthly report

Langkah selanjutnya adalah integrasi frontend + dashboard aggregation API.
