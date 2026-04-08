# 🚀 Python Automation Pipeline

An end-to-end automation system that performs web scraping, data processing, Excel report generation, and automated email distribution.

---

## 📌 Features

- 🌐 Web Scraping using BeautifulSoup
- 📊 Data Processing using Pandas
- 📁 Excel Report Generation using OpenPyXL
- 📧 Automated Email Sending using SMTP
- ⏰ Task Scheduling using Windows Task Scheduler

---

## ⚙️ Project Workflow

Web Scraping → CSV → Excel Report → Email → Scheduled Automation

---

## 🧩 Modules

### 1. scraper.py
- Scrapes book data from website
- Extracts title, price, rating, availability
- Saves data to CSV

### 2. excel_bot.py
- Reads CSV data
- Calculates metrics (Revenue, Top Product, etc.)
- Generates formatted Excel report with dashboard

### 3. email_bot.py
- Reads recipient details from CSV
- Sends personalized HTML emails
- Supports attachments
- Logs email status

### 4. master.py
- Runs all scripts in sequence
- Handles errors and logs execution time

---

## 📊 Sample Output

- `scraped_books.csv`
- `sales_report_YYYYMMDD.xlsx`
- `email_log.csv`

---

## 🛠️ Tech Stack

- Python
- Pandas
- BeautifulSoup
- OpenPyXL
- SMTP (Gmail)

---

## ▶️ How to Run

### Steps: Install dependencies
```bash
pip install pandas openpyxl beautifulsoup4 requests
