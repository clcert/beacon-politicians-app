import sqlite3

def init_db(db_name = "db.sqlite3"):
    """Initialize the database."""

    # Create the file
    print("[Init DB] Creating database file...")
    with open(db_name, "w") as db_file:
        db_file.close()

    # Create the tables
    print("[Init DB] Creating tables...")
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS main_profile ("+
        "id INTEGER PRIMARY KEY,"+
        "local_id INTEGER,"+
        "first_name TEXT,"+
        "second_name TEXT,"+
        "first_surname TEXT,"+
        "second_surname TEXT,"+
        "profile_picture TEXT,"+
        "gender TEXT,"+
        "birthdate DATE,"+
        "profession TEXT,"+
        "district INTEGER,"+
        "district_region TEXT,"+
        "party TEXT,"+
        "party_alias TEXT,"+
        "last_update DATE)"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS attendance ("+
        "deputy_id INTEGER PRIMARY KEY,"+
        "total INTEGER,"+
        "present INTEGER,"+
        "justified_absent INTEGER,"+
        "unjustified_absent INTEGER, "+
        "FOREIGN KEY (deputy_id) REFERENCES main_profile(id)" +
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS parlamentary_periods ("+
        "deputy_id INTEGER,"+
        "period_from INTEGER,"+
        "period_to INTEGER, "+
        "FOREIGN KEY (deputy_id) REFERENCES main_profile(id)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS votings ("+
        "deputy_id INTEGER,"+
        "voting_id INTEGER,"+
        "voting_date DATE,"+
        "bulletin_number INTEGER,"+ 
        "document_title TEXT,"+
        "article_text TEXT,"+
        "voted_option TEXT,"+
        "total_approved INTEGER,"+
        "total_rejected INTEGER,"+
        "total_abstention INTEGER,"+
        "result TEXT, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, voting_id)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses_operational ("+
        "deputy_id INTEGER,"+
        "year INTEGER,"+
        "month TEXT,"+
        "expense_type TEXT,"+
        "amount INTEGER, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, year, month, expense_type)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses_offices ("+
        "deputy_id INTEGER,"+
        "year INTEGER,"+
        "month TEXT,"+
        "offices_number INTEGER,"+
        "total_amount INTEGER, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, year, month)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses_support_staff ("+
        "deputy_id INTEGER,"+
        "year INTEGER,"+
        "month TEXT,"+
        "hired_staff INTEGER,"+
        "total_amount INTEGER, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, year, month)"+
        ")"
    )
    print("[Init DB] Done!")
   
def insert_deputy_profile(deputy_profile):
    """Insert a deputy profile into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO main_profile (id, local_id, first_name, second_name, first_surname, second_surname,
            profile_picture, gender, birthdate, profession, district, district_region, party, party_alias,
            last_update)
        VALUES (:id, :local_id, :first_name, :second_name, :first_surname, :second_surname,
            :profile_picture, :gender, :birthdate, :profession, :district, :district_region, :party, :party_alias,
            :last_update)
        """,
        deputy_profile
    )
    db.commit()
    db.close()

def insert_parlamentary_period(period):
    """Insert a parlamentary period of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO parlamentary_periods (deputy_id, period_from, period_to)
        VALUES (:id, :period_from, :period_to)
        """,
        period
    )
    db.commit()
    db.close()