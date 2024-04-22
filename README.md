# Project Overview

The aim of this project is to develop a web application designed to scrape data from Amazon and eBay for comprehensive market analysis. The web-based nature of the application ensures accessibility from anywhere, eliminating the need for custom scripts, library installations, command executions, and manual maintenance.

---

## Web Version Usage

1. **Visit** [ParseJet](http://www.parsejet.com).
2. **Sign Up/Login** to access the platform.
3. **Select** the desired tool:
    - Scrape Amazon Direct Product URLs
    - Scrape eBay Direct Product URLs
    - Comparison tools between Amazon and eBay marketplaces
4. **Input** the data source and await completion of the job.
5. **Download** the generated data.

---

## Local Setup Instructions

1. **Install Python** on your machine.
2. **Open** Command Prompt and navigate to the project directory.
3. **Install** the required dependencies using the following command:
    ```
    pip install -r requirements.txt
    ```
4. **Start** the Django server with the command:
    ```
    python manage.py runserver
    ```
5. **Run** Celery-Redis on Windows to handle background jobs:
    ```
    celery -A Crawler.cele worker --pool=solo -l info
    ```
6. **Submit** the product URLs, and upon completion, you will receive an email with a link to download the generated CSV file.

---

**Regards,**  
Eng Hussain
