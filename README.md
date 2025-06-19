# Cardwise

**Cardwise** helps you choose the best credit card for your purchases by evaluating rewards, cashback, or travel perks in real-time.

> ✨ Designed for couponers, travel hackers, and anyone looking to optimize their credit card usage.

---

## 🚀 Features

- 📊 Optimal matching of purchases to your credit cards, based on your bank's current deals and your cards point system
- 💳 Support for multiple credit cards (WIP)
- 🏷️ Support for multiple couponing systems (shop-specific, ibotta etc) (WIP)
- 🔍 Search for offers and cashback deals (WIP)
- 📈 Track your cashback and points balance per card (WIP)

---

## 📦 Installation

Cardwise requires **Python 3.9+**.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aydin-ab/cardwise.git
   cd cardwise
    ```
    
2. **Run make** to install dependencies on a poetry virtual env, install pre-commit, and run the tests:
   ```bash
   make
   ```

Or you can do it manually:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/aydin-ab/cardwise.git
   cd cardwise
    ```

2. **Install dependencies** with [Poetry](https://python-poetry.org/docs/#installation):

   ```bash
   poetry install
   ```

3. **Verify installation (optional)**:

    You can verify the installation with:
    ```bash
    poetry run search_offers -h
    ```

    You can run a prod docker container via Docker:

   ```bash
   docker compose up prod
   ```

   You also have a `.devcontainer/` snippet folder if you prefer using dev containers

   Remember to populate `htmls/` with your own data if you want to use the default parameters of `search_offers`


---

## Usage
### Search for offers
```bash
>> poetry run search_offers -h

usage: search_offer "starbucks" "mcdonalds" [--save results.json] [--bofa-html path.html] [--capone-html path.html] [--chase-html path.html] [-v | -vv | -vvv] [--log-level INFO] [--enable-email-logs]

Find the best offers for one or more companies.

positional arguments:
  queries               Company names to search for

options:
  -h, --help            show this help message and exit
  -s [SAVE], --save [SAVE]
                        Save results to a JSON file (default: results.json)
  --bofa-html BOFA_HTML
                        Custom HTML file for Bank of America
  --capone-html CAPONE_HTML
                        Custom HTML file for Capital One
  --chase-html CHASE_HTML
                        Custom HTML file for Chase
  -v, --verbose         Increase verbosity (-v, -vv, -vvv)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Manually set log level
  --enable-email-logs   Enable SMTP logging for critical errors
```

Default HTML files are provided for Bank of America, Capital One, and Chase in the `htmls/` directory. You can use these paths or provide your own custom HTML files to the appropriate arguments.

### Example with default params
```bash
poetry run search_offers "starbucks" "mcdonalds"
```
This will search for offers from Starbucks and McDonald's, save the results to `results.json`, and use default HTML files for Bank of America, Capital One, and Chase located in the `htmls/` directory.

### Example with Custom HTML Files
```bash
poetry run search_offers "starbucks" "mcdonalds" --save results.json --bofa-html path/to/bofa.html --capone-html path/to/capital_one.html --chase-html path/to/chase.html
```
This will search for offers from Starbucks and McDonald's, save the results to `results.json`, and use custom HTML files for Bank of America, Capital One, and Chase.

### Example with Docker (WIP)
```bash
docker compose run --rm prod "starbucks" "mcdonalds" 
```
This will search for offers from Starbucks and McDonald's, save the results to `results.json`, and query HTML files for Bank of America, Capital One, and Chase from a database.

---

## 🧪 Testing & Quality

Cardwise uses modern tooling to ensure high code quality.
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 🗂️ Directory Structure

```
cardwise/
├── src/cardwise/        # Source code
├── src/cardwise/bank_parser/  # Bank parsers
├── src/cardwise/bank_parser/{bank}.py  # specific bank parser
├── src/cardwise/bank_parser/exceptions.py  # generic exceptions
├── src/cardwise/bank_parser/logger.py  # logger
├── src/cardwise/bank_parser/search_offers.py  # entry point script to search for offers
├── src/cardwise/utils/ # Utility functions
├── tests/               # Test suite
```



---

## 🤝 Contributing

We welcome contributions!

* Read our [CONTRIBUTING.md](CONTRIBUTING.md)
* Use [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🧠 Author

**Aydin Abiar** – [@aydinabiar](https://github.com/Aydin-ab)
Feel free to open an issue or discussion to ask questions or share feedback!

