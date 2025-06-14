import sqlite3
import random
from datetime import datetime, timedelta, date
from faker import Faker
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Use TEST_SQLITE_DB_PATH or fallback
DB_FILE = os.getenv("TEST_SQLITE_DB_PATH", "qualys_scan_results.db")
NUM_RECORDS = 5000

fake = Faker()

# Business-facing applications
APPLICATIONS = [
    "Sales", "CustomerCare", "OrderProcessing", "QuoteManagement",
    "Billing", "Inventory", "Fulfillment", "Returns", "Marketing", "Analytics"
]

# Technical platforms used in vulnerability titles
TECH_COMPONENTS = [
    "Oracle", "Java", "Apache", "Nginx", "Tomcat", "OpenSSL",
    "Docker", "Kubernetes", "MySQL", "PostgreSQL"
]

# Vulnerability title templates
VULN_TEMPLATES = [
    "{} Patch Released - {}",
    "Critical {} Vulnerability Detected - {}",
    "{} Zero-Day Found - {}",
    "Security Advisory: {} Exposure - {}",
    "{} RCE Vulnerability - {}"
]

SEVERITY_LEVELS = ["S1", "S2", "S3", "S4", "S5"]
STATUSES = ["open", "remediated", "in-progress"]
OPERATING_SYSTEMS = ["Windows 10", "Ubuntu 22.04", "RHEL 9", "macOS Ventura"]

def create_connection(db_file):
    return sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

def create_table(cur):
    cur.execute("DROP TABLE IF EXISTS scan_results;")
    cur.execute("""
    CREATE TABLE scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT,
        ip_address TEXT,
        application_name TEXT,
        vuln_title TEXT,
        cvss_score REAL,
        severity TEXT,
        status TEXT,
        detection_date DATE,
        due_date DATE,
        resolution_date DATE,
        age INTEGER,
        os TEXT
    );
    """)

def generate_row():
    hostname = fake.hostname()
    ip_address = fake.ipv4()
    app = random.choice(APPLICATIONS)
    tech = random.choice(TECH_COMPONENTS)

    detection_date = fake.date_between(start_date="-365d", end_date="-10d")
    month_year = detection_date.strftime("%b %Y")
    vuln_title = random.choice(VULN_TEMPLATES).format(tech, month_year)

    cvss_score = round(random.uniform(2.0, 10.0), 1)
    severity = random.choice(SEVERITY_LEVELS)
    status = random.choices(STATUSES, weights=[0.5, 0.3, 0.2])[0]

    due_date = detection_date + timedelta(days=random.choice([15, 30, 60]))
    resolution_date = None
    age = 0

    if status == "remediated":
        resolution_date = detection_date + timedelta(days=random.randint(1, 60))
        age = (resolution_date - detection_date).days
    else:
        age = (date.today() - detection_date).days

    os_name = random.choice(OPERATING_SYSTEMS)
    return (
        hostname, ip_address, app, vuln_title,
        cvss_score, severity, status,
        detection_date.isoformat(),
        due_date.isoformat(),
        resolution_date.isoformat() if resolution_date else None,
        age,
        os_name
    )

def main():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    create_table(cur)

    for _ in range(NUM_RECORDS):
        row = generate_row()
        cur.execute("""
            INSERT INTO scan_results (
                hostname, ip_address, application_name, vuln_title,
                cvss_score, severity, status, detection_date,
                due_date, resolution_date, age, os
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

    conn.commit()
    conn.close()
    print(f"✅ {NUM_RECORDS} records inserted into '{DB_FILE}'.")

if __name__ == "__main__":
    main()
