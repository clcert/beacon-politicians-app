import sqlite3

def create_db(db_name = "db.sqlite3"):
    """Creates the database file."""
    print("Creating database file...")
    with open(db_name, "w") as db_file:
        db_file.close()
    print("Database file created.")

def init_db(db_name = "db.sqlite3"):
    """Initializes the database."""

    print("Creating tables...")
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
        "month INTEGER,"+
        "expense_type TEXT,"+
        "amount INTEGER, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, year, month, expense_type)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses_offices ("+
        "deputy_id INTEGER,"+
        "year INTEGER,"+
        "month INTEGER,"+
        "offices_number INTEGER,"+
        "total_amount INTEGER, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, year, month)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses_support_staff ("+
        "deputy_id INTEGER,"+
        "year INTEGER,"+
        "month INTEGER,"+
        "hired_staff INTEGER,"+
        "total_amount INTEGER, "+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, year, month)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS law_projects ("+
        "deputy_id INTEGER,"+
        "project_id INTEGER,"+
        "project_name TEXT,"+
        "project_type TEXT,"+
        "project_status TEXT,"+
        "project_date DATE,"+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, project_id)"+
        ")"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS deputy_of_the_day ("+
        "deputy_id INTEGER,"+
        "date DATE,"+
        "chain_id TEXT,"+
        "pulse_id TEXT,"+
        "rand_out TEXT,"+
        "FOREIGN KEY(deputy_id) REFERENCES main_profile(id) "+
        "PRIMARY KEY(deputy_id, date)"+
        ")"
    )
    db.commit()
    db.close()
    print("Done!")
   
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


def get_real_index_from_db(local_index):
    """Get the real index of a deputy from the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT id FROM main_profile WHERE local_id = :local_id
        """,
        {"local_id": local_index}
    )
    row = cursor.fetchone()
    cursor.close()
    db.close()

    if row:
        return row[0]

    return None


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


def find_operational_expenses_for_deputy(deputy_id):
    """
    Find operational expenses of a deputy in the database.
    Returns a list of dictionaries.
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT * FROM expenses_operational 
        WHERE deputy_id = :deputy_id
        ORDER BY year DESC, month DESC
        """,
        {"deputy_id": deputy_id}
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    return rows


def find_operational_indicators_by_category_and_month(category, year, month):
    """
    Given a operational expenses category, a year and a month,
    find the average amount spent by deputies in that category.
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT AVG(amount), MIN(amount), MAX(amount) FROM expenses_operational 
        WHERE expense_type = :category AND year = :year AND month = :month
        """,
        {"category": category, "year": year, "month": month}
    )
    row = cursor.fetchone()
    cursor.close()
    db.close()
    return row


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


def find_staff_expenses_for_deputy(deputy_id):
    """
    Find staff expenses of a deputy in the database.
    Returns a list of dictionaries.
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT * FROM expenses_support_staff WHERE deputy_id = :deputy_id
        ORDER BY year DESC, month DESC
        """,
        {"deputy_id": deputy_id}
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    return rows


def find_support_staff_indicators_by_month(year, month):
    """
    Given a year and a month, find the average amount spent by deputies
    in support staff.
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT AVG(total_amount), MIN(total_amount), MAX(total_amount) FROM expenses_support_staff WHERE year = :year AND month = :month
        """,
        {"year": year, "month": month}
    )
    row = cursor.fetchone()
    cursor.close()
    db.close()
    return row


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


def insert_voting_record(vote, deputy_id):
    """Insert voting record of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    vote['deputy_id'] = deputy_id

    cursor.execute( # Delete previous records
        """
        DELETE FROM votings WHERE deputy_id = :deputy_id
        """,
        {"deputy_id": deputy_id}
    )

    cursor.execute(
        """
        INSERT OR REPLACE INTO votings (deputy_id, voting_id, voting_date, bulletin_number, document_title, article_text, voted_option, total_approved, total_rejected, total_abstention, result)
        VALUES (:deputy_id, :voting_id, :date, :description, :name, :article, :vote_option, :total_yes, :total_no, :total_abstention, :result)
        """,
        vote
    )
    db.commit()
    db.close()


def insert_law_project_record(law_proj, deputy_id):
    """Insert law project record of a deputy into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    law_proj['deputy_id'] = deputy_id
    law_proj['project_type'] = "Moción"
    cursor.execute(
        """
        INSERT OR REPLACE INTO law_projects (deputy_id, project_id, project_name, project_type, project_status, project_date)
        VALUES (:deputy_id, :project_id, :project_name, :project_type, :project_status, :project_date)
        """,
        law_proj
    )
    db.commit()
    db.close()


def find_law_projects_for_deputy(deputy_id):
    """
    Find law projects for a deputy in the database.
    """
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT * FROM law_projects WHERE deputy_id = :deputy_id
        """,
        {"deputy_id": deputy_id}
    )
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


def insert_deputy_of_the_day(record):
    """Insert deputy of the day into the database."""
    db = sqlite3.connect("db.sqlite3")
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO deputy_of_the_day (deputy_id, date, chain_id, pulse_id, rand_out)
        VALUES (:deputy_id, :date, :chain_id, :pulse_id, :rand_out)
        """,
        record
    )
    db.commit()
    db.close()