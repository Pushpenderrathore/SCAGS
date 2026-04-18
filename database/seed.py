import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    # Real JEE Mains 2024 approximate cutoffs (percentile-based)
    colleges = [
        # NIT Tier-1
        ("NIT Trichy", "CSE", 99.1, 120000, "Trichy, Tamil Nadu", 95.0, 1),
        ("NIT Warangal", "CSE", 98.8, 110000, "Warangal, Telangana", 93.0, 2),
        ("NIT Surathkal", "CSE", 98.5, 115000, "Surathkal, Karnataka", 91.0, 3),
        ("NIT Calicut", "CSE", 98.2, 108000, "Calicut, Kerala", 90.0, 4),
        ("NIT Allahabad", "CSE", 97.8, 105000, "Prayagraj, UP", 88.0, 5),
        ("NIT Rourkela", "CSE", 97.5, 100000, "Rourkela, Odisha", 86.0, 6),
        ("VNIT Nagpur", "CSE", 97.2, 95000, "Nagpur, Maharashtra", 84.0, 7),
        ("NIT Jaipur", "CSE", 96.8, 98000, "Jaipur, Rajasthan", 83.0, 8),

        # NIT Tier-1 ECE
        ("NIT Trichy", "ECE", 98.5, 120000, "Trichy, Tamil Nadu", 90.0, 1),
        ("NIT Warangal", "ECE", 98.0, 110000, "Warangal, Telangana", 88.0, 2),
        ("NIT Surathkal", "ECE", 97.8, 115000, "Surathkal, Karnataka", 86.0, 3),
        ("NIT Calicut", "ECE", 97.5, 108000, "Calicut, Kerala", 85.0, 4),

        # NIT Tier-2
        ("NIT Agartala", "CSE", 90.0, 75000, "Agartala, Tripura", 65.0, 15),
        ("NIT Manipur", "CSE", 88.0, 70000, "Imphal, Manipur", 60.0, 18),
        ("NIT Sikkim", "CSE", 85.0, 68000, "Ravangla, Sikkim", 55.0, 22),
        ("NIT Arunachal", "CSE", 82.0, 65000, "Yupia, Arunachal", 52.0, 25),
        ("NIT Puducherry", "CSE", 87.0, 72000, "Karaikal, Puducherry", 62.0, 20),
        ("NIT Goa", "CSE", 91.0, 80000, "Goa", 68.0, 13),

        # IIIT Tier-1
        ("IIIT Hyderabad", "CSE", 99.0, 200000, "Hyderabad, Telangana", 98.0, 1),
        ("IIIT Allahabad", "CSE", 97.5, 150000, "Prayagraj, UP", 92.0, 2),
        ("IIIT Delhi", "CSE", 98.0, 180000, "New Delhi", 96.0, 1),
        ("IIIT Bangalore", "CSE", 97.0, 160000, "Bengaluru, Karnataka", 94.0, 3),

        # IIIT ECE
        ("IIIT Hyderabad", "ECE", 98.5, 200000, "Hyderabad, Telangana", 95.0, 1),
        ("IIIT Allahabad", "ECE", 96.5, 150000, "Prayagraj, UP", 88.0, 2),

        # GFTI / State NITs
        ("NIT Hamirpur", "CSE", 93.0, 85000, "Hamirpur, HP", 72.0, 10),
        ("NIT Kurukshetra", "CSE", 94.5, 90000, "Kurukshetra, Haryana", 75.0, 9),
        ("NIT Patna", "CSE", 92.0, 82000, "Patna, Bihar", 70.0, 12),
        ("NIT Durgapur", "CSE", 93.5, 88000, "Durgapur, WB", 73.0, 11),
        ("NIT Srinagar", "CSE", 80.0, 60000, "Srinagar, J&K", 50.0, 28),
        ("NIT Uttarakhand", "CSE", 78.0, 58000, "Srinagar, Uttarakhand", 48.0, 30),

        # Mechanical
        ("NIT Trichy", "Mechanical", 97.5, 120000, "Trichy, Tamil Nadu", 85.0, 1),
        ("NIT Warangal", "Mechanical", 97.0, 110000, "Warangal, Telangana", 83.0, 2),
        ("NIT Surathkal", "Mechanical", 96.5, 115000, "Surathkal, Karnataka", 80.0, 3),
        ("NIT Calicut", "Mechanical", 96.0, 108000, "Calicut, Kerala", 78.0, 4),
        ("NIT Jaipur", "Mechanical", 94.0, 98000, "Jaipur, Rajasthan", 74.0, 8),
        ("NIT Hamirpur", "Mechanical", 88.0, 85000, "Hamirpur, HP", 62.0, 10),
        ("NIT Agartala", "Mechanical", 82.0, 75000, "Agartala, Tripura", 55.0, 15),

        # Civil
        ("NIT Trichy", "Civil", 96.0, 120000, "Trichy, Tamil Nadu", 78.0, 1),
        ("NIT Warangal", "Civil", 95.5, 110000, "Warangal, Telangana", 75.0, 2),
        ("NIT Surathkal", "Civil", 95.0, 115000, "Surathkal, Karnataka", 73.0, 3),
        ("NIT Rourkela", "Civil", 93.0, 100000, "Rourkela, Odisha", 68.0, 6),
        ("NIT Jaipur", "Civil", 90.0, 98000, "Jaipur, Rajasthan", 65.0, 8),
        ("NIT Agartala", "Civil", 76.0, 75000, "Agartala, Tripura", 48.0, 15),

        # EEE
        ("NIT Warangal", "EEE", 97.0, 110000, "Warangal, Telangana", 82.0, 2),
        ("NIT Calicut", "EEE", 96.5, 108000, "Calicut, Kerala", 80.0, 4),
        ("NIT Rourkela", "EEE", 95.5, 100000, "Rourkela, Odisha", 78.0, 6),
        ("NIT Jaipur", "EEE", 93.5, 98000, "Jaipur, Rajasthan", 72.0, 8),
        ("NIT Hamirpur", "EEE", 87.0, 85000, "Hamirpur, HP", 60.0, 10),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO colleges 
        (name, branch, cutoff, fees, location, placement, ranking)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, colleges)

    conn.commit()
    conn.close()
    print(f"[+] Database initialized at {DB_PATH}")
    print(f"[+] Inserted {len(colleges)} college records")

if __name__ == "__main__":
    init_db()
