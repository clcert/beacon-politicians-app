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

def find_profile_data_in_db(deputy_index):
    """Find a deputy profile in the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT * FROM main_profile WHERE id = :id
        """,
        {"id": deputy_index}
    )
    row = cursor.fetchone()
    cursor.close()
    db.close()

    if row:
        return {
            'id': row[0],
            'local_id': row[1],
            'first_name': row[2],
            'second_name': row[3],
            'first_surname': row[4],
            'second_surname': row[5],
            'profile_picture': row[6],
            'gender': row[7],
            'birthdate': row[8],
            'profession': row[9],
            'district': row[10],
            'district_region': row[11],
            'party': row[12],
            'party_alias': row[13],
            'last_update': row[14]
        }

    return None


def insert_operational_expenses(op_exp, deputy_id):
    """Insert operational expenses of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    for record in op_exp:
        record_month, record_year = record['month'], record['year']
        del record['month']
        del record['year']

        for key, value in record.items():
            cursor.execute(
                """
                INSERT OR REPLACE INTO expenses_operational (deputy_id, year, month, expense_type, amount)
                VALUES (:deputy_id, :year, :month, :expense_type, :amount)
                """, 
                { 'deputy_id': deputy_id, 'year': record_year, 'month': record_month, 'expense_type': key, 'amount': value }
            )
    db.commit()
    cursor.close()
    db.close()


def insert_staff_expenses(st_exp, deputy_id):
    """Insert staff expenses of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    for record in st_exp:
        record['deputy_id'] = deputy_id
        cursor.execute(
            """
            INSERT OR REPLACE INTO expenses_support_staff (deputy_id, year, month, hired_staff, total_amount)
            VALUES (:deputy_id, :year, :month, :num_personal, :total)
            """, 
            record
        )
    db.commit()
    cursor.close()
    db.close()


def insert_office_expenses(off_exp, deputy_id):
    """Insert office expenses of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()

    for record in off_exp:
        record['deputy_id'] = deputy_id
        cursor.execute(
            """
            INSERT OR REPLACE INTO expenses_offices (deputy_id, year, month, offices_number, total_amount)
            VALUES (:deputy_id, :year, :month, :num_oficinas, :total)
            """, 
            record
        )
    db.commit()
    cursor.close()
    db.close()

def insert_attendance_record(attendance, deputy_id):
    """Insert attendance record of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    attendance['deputy_id'] = deputy_id
    cursor.execute(
        """
        INSERT OR REPLACE INTO attendance (deputy_id, total, present, justified_absent, unjustified_absent)
        VALUES (:deputy_id, :total, :present, :justified_absent, :unjustified_absent)
        """,
        attendance
    )
    db.commit()
    db.close()