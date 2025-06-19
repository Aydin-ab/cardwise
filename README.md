# Cardwise

**Cardwise** helps you choose the best credit card for your purchases by evaluating rewards, cashback, or travel perks in real-time.

> ✨ Designed for couponers, travel hackers, and anyone looking to optimize their credit card usage.

---

## 🚀 Features

- 📊 Optimal card matching based on current bank offers and your card's reward system
- 💳 Support for multiple banks
- 🔍 Search for offers and cashback deals
- 🏷️ Support for couponing platforms (e.g., Ibotta, shop-specific) _(WIP)_
- 📈 Track cashback and points balances per card _(WIP)_

---

## 📦 Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/aydin-ab/cardwise.git
   cd cardwise
```

2. **Install dependencies, run tests, and configure pre-commit:**

```bash
   make
```

3. *Optional*: You can use the `.devcontainer/` snippet to spin up a dev container.

---

## 🧠 System Design Overview

### Ingestion

**Components:** GCS Bucket · Postgres · Supabase · GitHub Actions

Cardwise fetches bank offers (e.g., cashback, points, perks) by parsing manually uploaded HTML files stored in a GCS bucket. Since APIs are gated and scraping is disallowed, ingestion is manual for now.

Each run:
  * Flushes the DB
  * Parses HTML into `Offer` objects
  * Stores new offers in Postgres (hosted on Supabase)
  * A GitHub Actions cron job runs ingestion **monthly** (aligned with most bank offer cycles).

Configure it via `.env.ingestion` (see `.env.ingestion.example`):

```env
GCS_CREDENTIALS=ingestion/gcs/ingestion-bot-key.json
GCS_BUCKET_NAME=cardwise-01012025-bucket
DATABASE_URL=postgresql://...
LOG_LEVEL=INFO
```

---

### Backend

**Components:** FastAPI · Postgres · Render · cron-job.org

The backend exposes offer search via a FastAPI app, using fuzzy matching for partial or misspelled shop names.

* Hosted on [Render](https://render.com). See [render.yaml](render.yaml) for deployment config.
* Kept warm using [cron-job.org](https://cron-job.org) (free plan otherwise sleeps after 15 mins)

Docs:
* [Swagger UI](https://cardwise-backend-latest.onrender.com/docs)
* [ReDoc](https://cardwise-backend-latest.onrender.com/redoc)

`.env.backend` example:

```env
DATABASE_URL=postgresql://...
DEBUG=True
LOG_LEVEL=INFO
```

---

### Frontend

**Components:** Flutter · Dart · Android Studio

Cross-platform mobile app built with Flutter, designed for:
* Browsing matching offers for your purchases
* Search by shop name
* View all offers

Note: Currently tested only on Android (because that's my phone !), but Flutter ensures iOS compatibility.

---

### CLI

**Components:** Typer

The CLI offers:
* 🔍 **Search**: Query offers from the backend
* 🛠️ **Ingest**: Run the HTML-to-DB pipeline from GCS

Example `.env.cli`:

```env
BACKEND_API_URL=http://localhost:10000
GCS_CREDENTIALS=ingestion/gcs/ingestion-bot-key.json
GCS_BUCKET_NAME=cardwise-01012025-bucket
DATABASE_URL=postgresql://...
LOG_LEVEL=INFO
```

#### 🔎 Search for Offers

```bash
cardwise search adidas "shake shack"
```

✅ Fuzzy matching: `starbuck`, `starbuck's`, or `starbucks` — all work!

Sample output:

```bash
>> cardwise search adidas "shake shack"

🔍 Searching for: ['adidas', 'shake shak']
[Bank of America] Shake Shack: CASHBACK - 10% (no expiry date found)
[Capital One] adidas: POINTS - Up to 16X miles (no expiry date found)
[Chase] Shake Shack: CASHBACK - 10% cash back (no expiry date found)
```

#### 🧃 Ingest HTML Offers

```bash
cardwise ingest
```

Sample output:

```bash
>> cardwise ingest

2025-06-18 22:10:49 [INFO] offer_ingestion_pipeline.py:32 in run — 📝 Parsing html docs: bank_of_america using BankOfAmericaOfferParser
2025-06-18 22:10:50 [INFO] offer_ingestion_pipeline.py:34 in run — ✅ Parsed 40 offer(s) from bank_of_america
2025-06-18 22:10:50 [INFO] offer_ingestion_pipeline.py:32 in run — 📝 Parsing html docs: capital_one using CapitalOneOfferParser
2025-06-18 22:10:50 [INFO] offer_ingestion_pipeline.py:34 in run — ✅ Parsed 3557 offer(s) from capital_one
2025-06-18 22:10:50 [INFO] offer_ingestion_pipeline.py:32 in run — 📝 Parsing html docs: chase using ChaseOfferParser
2025-06-18 22:10:50 [INFO] offer_ingestion_pipeline.py:34 in run — ✅ Parsed 116 offer(s) from chase
2025-06-18 22:10:50 [INFO] offer_ingestion_pipeline.py:37 in run — 📦 Inserting 3713 offer(s) into the database...
2025-06-18 22:10:50 [INFO] repository.py:20 in delete_all — Deleting all existing offers from the database...
2025-06-18 22:10:51 [INFO] repository.py:23 in delete_all — All offers deleted.
2025-06-18 22:10:51 [INFO] repository.py:33 in insert_many — Inserting 3713 offer(s) into the database...
2025-06-18 22:10:51 [INFO] repository.py:37 in insert_many — Insert complete.
2025-06-18 22:10:51 [INFO] offer_ingestion_pipeline.py:41 in run — 🎉 Ingestion pipeline complete.
```

---

### 🐳 Docker Dev Example

```bash
make docker-dev
```

This starts the backend in a container and opens a shell to a CLI container ready to query or ingest.

---

## 🧪 Testing & Quality

Cardwise uses modern tools for code quality:

* `pytest` for testing
* `ruff` for linting & formatting
* `pyright` for static typing
* `pre-commit` for hooks

See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup.

---

## 🗂️ Directory Structure

```txt
cardwise/
├── backend/         # FastAPI backend server
├── cardwise/        # Core business logic
├── cli/             # Typer CLI
├── ingestion/       # HTML-to-DB ingestion
├── frontend/        # Flutter mobile app
├── tests/           # Unit and integration tests
```

---

## 🤝 Contributing

Contributions are welcome! ✨

* Read [CONTRIBUTING.md](CONTRIBUTING.md)
* Follow [Conventional Commits](https://www.conventionalcommits.org)

---

## 📄 License

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file.

---

## 🧠 Author

**Aydin Abiar**
GitHub: [@aydinabiar](https://github.com/aydin-ab)
Feel free to open an issue, suggest improvements, or share feedback!
