import sqlite3
from utils.settings import DB_PATH
from os import path
import logging

logging.basicConfig(
    format='%(asctime)s [DB: %(levelname)s] %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

class DatabaseConnection:

    def __init__(self, db_path = DB_PATH) -> None:
        self.db_path = db_path
        self.db = None

    def __enter__(self):
        self.db = sqlite3.connect(self.db_path)
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

    def create_database(self):
        """Creates the database file."""
        logging.info(f"creating database file {self.db_path}")
        if path.exists(self.db_path):
            logging.info("database file already exists")
        else:
            with open(self.db_path, "w") as db_file:
                db_file.close()
            logging.info("database file created")

    def create_tables(self):
        with self as db:
            cursor = db.cursor()
            logging.info("creating tables if not exists")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS main_profile (
                    id INTEGER PRIMARY KEY,
                    local_id INTEGER,
                    first_name TEXT,
                    first_surname TEXT,
                    second_surname TEXT,
                    profile_picture TEXT,
                    gender TEXT,
                    birthdate DATE,
                    profession TEXT,
                    district INTEGER,
                    district_region TEXT,
                    party TEXT,
                    party_alias TEXT,
                    twitter_username TEXT,
                    instagram_username TEXT,
                    last_update DATE,
                    district_communes TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    deputy_id INTEGER PRIMARY KEY,
                    total INTEGER,
                    present INTEGER,
                    justified_absent INTEGER,
                    unjustified_absent INTEGER,
                    FOREIGN KEY (deputy_id) REFERENCES main_profile(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parlamentary_periods (
                    deputy_id INTEGER,
                    period_from INTEGER,
                    period_to INTEGER,
                    FOREIGN KEY (deputy_id) REFERENCES main_profile(id)
                    PRIMARY KEY (deputy_id, period_from, period_to)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votings (
                    deputy_id INTEGER,
                    voting_id INTEGER,
                    voting_date DATE,
                    bulletin_number INTEGER,
                    document_title TEXT,
                    article_text TEXT,
                    voted_option TEXT,
                    total_approved INTEGER,
                    total_rejected INTEGER,
                    total_abstention INTEGER,
                    result TEXT,
                    FOREIGN KEY(deputy_id) REFERENCES main_profile(id) 
                    PRIMARY KEY(deputy_id, voting_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses_operational (
                    deputy_id INTEGER,
                    year INTEGER,
                    month INTEGER,
                    expense_type TEXT,
                    amount INTEGER,
                    FOREIGN KEY(deputy_id) REFERENCES main_profile(id) 
                    PRIMARY KEY(deputy_id, year, month, expense_type)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses_offices (
                    deputy_id INTEGER,
                    year INTEGER,
                    month INTEGER,
                    offices_number INTEGER,
                    total_amount INTEGER,
                    FOREIGN KEY(deputy_id) REFERENCES main_profile(id)
                    PRIMARY KEY(deputy_id, year, month)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses_support_staff (
                    deputy_id INTEGER,
                    year INTEGER,
                    month INTEGER,
                    hired_staff INTEGER,
                    total_amount INTEGER,
                    FOREIGN KEY(deputy_id) REFERENCES main_profile(id) 
                    PRIMARY KEY(deputy_id, year, month)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS law_projects (
                    deputy_id INTEGER,
                    project_id INTEGER,
                    project_name TEXT,
                    project_type TEXT,
                    project_status TEXT,
                    project_date DATE,
                    FOREIGN KEY(deputy_id) REFERENCES main_profile(id)
                    PRIMARY KEY(deputy_id, project_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS deputy_of_the_day (
                    deputy_id INTEGER,
                    date DATE,
                    chain_id TEXT,
                    pulse_id TEXT,
                    rand_out TEXT,
                    FOREIGN KEY(deputy_id) REFERENCES main_profile(id)
                    PRIMARY KEY(deputy_id, date)
                )
            """)
            logging.info("tables created")
            cursor.close()


def insert_deputy_profile(deputy_profile):
    """Insert a deputy profile into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting deputy profile {} {} ({}) into database".format(
                deputy_profile['first_name'], 
                deputy_profile['first_surname'], 
                deputy_profile['id']
            )
        )
        cursor.execute(
            """
            INSERT OR REPLACE INTO main_profile (id, local_id, first_name, first_surname, second_surname,
                profile_picture, gender, birthdate, profession, district, district_region, district_communes,
                party, party_alias, twitter_username, instagram_username, last_update)
            VALUES (:id, :local_id, :first_name, :first_surname, :second_surname, :profile_picture, :gender, 
                :birthdate, :profession, :district, :district_region, :district_communes, :party, :party_alias,
                :twitter_username, :instagram_username, :last_update)
            """,
            deputy_profile
        )
        cursor.close()


def insert_parlamentary_period(period):
    """Insert a parlamentary period of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting parlamentary period for deputy {} into database".format(
                period['deputy_id']
            )
        )
        cursor.execute(
            """
            INSERT OR REPLACE INTO parlamentary_periods (deputy_id, period_from, period_to)
            VALUES (:deputy_id, :period_from, :period_to)
            """,
            period
        )
        cursor.close()


def find_deputy_periods(deputy_index):
    """Find the parlamentary periods of a deputy in the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding parlamentary periods for deputy {deputy_index} in database")
        cursor.execute(
            """
            SELECT period_from, period_to FROM parlamentary_periods WHERE deputy_id = :id
            ORDER BY period_from DESC
            """,
            {"id": deputy_index}
        )
        rows = cursor.fetchall()
        cursor.close()
    return rows


def get_real_index_from_db(local_index):
    """Get the real index of a deputy from the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding real index for deputy with local index {local_index}")
        cursor.execute(
            """
            SELECT
                id
            FROM 
                main_profile
                WHERE local_id = :local_id
            """,
            {"local_id": local_index}
        )
        row = cursor.fetchone()
        cursor.close()
    return row[0] if row else None


def find_profile_data_in_db(deputy_index):
    """Find a deputy profile in the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding profile for deputy with index {deputy_index}")
        cursor.execute(
            """
            SELECT 
                id, local_id, first_name, first_surname, second_surname,
                profile_picture, gender, birthdate, profession,
                district, district_region, district_communes,
                party, party_alias, twitter_username, instagram_username,
                last_update
            FROM 
                main_profile 
                WHERE id = :id
            """,
            {"id": deputy_index}
        )
        row = cursor.fetchone()
        cursor.close()
    props = [
        'id', 'local_id', 'first_name', 'first_surname', 'second_surname', 
        'profile_picture', 'gender', 'birthdate', 'profession', 'district',
        'district_region', 'district_communes', 'party', 'party_alias', 
        'twitter_username', 'instagram_username', 'last_update', 
    ]
    if row:
        return { prop: row[i] for i, prop in enumerate(props) }
    return None


def insert_operational_expenses(op_exp, deputy_id):
    """Insert operational expenses of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting operational expenses for deputy {} into database".format(
                deputy_id
            )
        )
        for record in op_exp:
            record_month, record_year = record['month'], record['year']
            del record['month']
            del record['year']

            for key, value in record.items():
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO 
                        expenses_operational (deputy_id, year, month, expense_type, amount)
                    VALUES 
                        (:deputy_id, :year, :month, :expense_type, :amount)
                    """, 
                    { 'deputy_id': deputy_id, 'year': record_year, 'month': record_month, 'expense_type': key, 'amount': value }
                )
        cursor.close()


def find_operational_expenses_for_deputy(deputy_id):
    """
    Find operational expenses of a deputy in the database.
    Returns a list of dictionaries.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding operational expenses for deputy {deputy_id} in database")
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
    return rows


def find_operational_indicators_by_category_and_month(category, year, month):
    """
    Given a operational expenses category, a year and a month,
    find the average amount spent by deputies in that category.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding operational indicators for category {category} in database")
        cursor.execute(
            """
            SELECT 
                AVG(amount), 
                MIN(amount), 
                MAX(amount)
            FROM 
                expenses_operational 
                WHERE 
                    expense_type = :category AND year = :year AND month = :month
            """,
            {"category": category, "year": year, "month": month}
        )
        row = cursor.fetchone()
        cursor.close()
    return row


def find_operational_indicators_by_month(year, month):
    """
    Given a year and a month, find the average amount spent by deputies.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding operational indicators in database")
        cursor.execute(
            """
            WITH expenses_operational_by_deputy AS (
                SELECT SUM(amount) AS amount, deputy_id
                FROM expenses_operational
                WHERE year = :year AND month = :month
                GROUP BY deputy_id
            )
            SELECT 
                AVG(amount), 
                MIN(amount), 
                MAX(amount)
            FROM 
                expenses_operational_by_deputy
            """,
            {"year": year, "month": month}
        )
        row = cursor.fetchone()
        cursor.close()
    return row


def find_operational_ranking_by_month(deputy_id, year, month):
    """
    Given a year and a month, find the ranking position
    from deputies with the highest operational expenses.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            f"finding operational ranking for deputy {deputy_id} at month {year}-{month}"
        )
        cursor.execute(
        """
            WITH expenses_op_rank AS (
                SELECT 
                    deputy_id,
                    SUM(amount) AS month_amount,
                    RANK() OVER (ORDER BY SUM(amount) DESC) AS month_amount_rank
                FROM expenses_operational
                WHERE year = :year AND month = :month
                GROUP BY deputy_id
            )
            SELECT
                deputy_id,
                month_amount,
                month_amount_rank
            FROM
                expenses_op_rank
            WHERE
                deputy_id = :deputy_id  
            """,
            {"year": year, "month": month, "deputy_id": deputy_id}
        )
        rows = cursor.fetchone()
        cursor.close()
    expenses_rank = rows[2] if rows else None
    return expenses_rank


def insert_staff_expenses(st_exp, deputy_id):
    """Insert staff expenses of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting staff expenses for deputy {} into database".format(
                deputy_id
            )
        )
        for record in st_exp:
            record['deputy_id'] = deputy_id
            cursor.execute(
                """
                INSERT OR REPLACE INTO expenses_support_staff (deputy_id, year, month, hired_staff, total_amount)
                VALUES (:deputy_id, :year, :month, :num_personal, :total)
                """, 
                record
            )
        cursor.close()


def find_staff_expenses_for_deputy(deputy_id):
    """
    Find staff expenses of a deputy in the database.
    Returns a list of dictionaries.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding staff expenses for deputy {deputy_id} in database")
        cursor.execute(
            """
            SELECT * FROM expenses_support_staff WHERE deputy_id = :deputy_id
            ORDER BY year DESC, month DESC
            """,
            {"deputy_id": deputy_id}
        )
        rows = cursor.fetchall()
        cursor.close()
    return rows


def find_support_staff_indicators_by_month(year, month):
    """
    Given a year and a month, find the average amount spent by deputies
    in support staff.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding support staff indicators for month {year}-{month} in database")
        cursor.execute(
            """
            SELECT 
                AVG(total_amount), 
                MIN(total_amount), 
                MAX(total_amount)
            FROM 
                expenses_support_staff 
                WHERE 
                    year = :year AND month = :month
            """,
            {"year": year, "month": month}
        )
        row = cursor.fetchone()
        cursor.close()
    return row


def find_support_staff_ranking_by_month(deputy_id, year, month):
    """
    Given a year and a month, find the ranking position
    from deputies with the highest support staff expenses.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            f"finding support staff ranking for deputy {deputy_id} at month {year}-{month}"
        )
        cursor.execute(
            """
            WITH expenses_st_rank AS (
                SELECT
                    deputy_id,
                    total_amount,
                    RANK() OVER (ORDER BY total_amount DESC) AS total_amount_rank
                FROM 
                    expenses_support_staff 
                    WHERE 
                        year = :year AND 
                        month = :month
                ORDER BY
                    total_amount DESC
            )
            SELECT
                deputy_id,
                total_amount,
                total_amount_rank
            FROM
                expenses_st_rank
            WHERE
                deputy_id = :deputy_id  
            """,
            {"year": year, "month": month, "deputy_id": deputy_id}
        )
        rows = cursor.fetchone()
        cursor.close()
    expenses_rank = rows[2] if rows else None
    return expenses_rank


def insert_office_expenses(off_exp, deputy_id):
    """Insert office expenses of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting office expenses for deputy {} into database".format(
                deputy_id
            )
        )
        for record in off_exp:
            record['deputy_id'] = deputy_id
            cursor.execute(
                """
                INSERT OR REPLACE INTO expenses_offices (deputy_id, year, month, offices_number, total_amount)
                VALUES (:deputy_id, :year, :month, :num_oficinas, :total)
                """, 
                record
            )
        cursor.close()


def insert_attendance_record(attendance, deputy_id):
    """Insert attendance record of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting attendance record for deputy {} into database".format(
                deputy_id
            )
        )
        attendance['deputy_id'] = deputy_id
        cursor.execute(
            """
            INSERT OR REPLACE INTO attendance (deputy_id, total, present, justified_absent, unjustified_absent)
            VALUES (:deputy_id, :total, :present, :justified_absent, :unjustified_absent)
            """,
            attendance
        )
        cursor.close()


def delete_previous_voting_records(deputy_id):
    """Delete previous voting records of a deputy."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "deleting previous voting records for deputy {} from database".format(
                deputy_id
            )
        )
        cursor.execute(
            """
            DELETE FROM votings WHERE deputy_id = :deputy_id
            """,
            {"deputy_id": deputy_id}
        )
        cursor.close()


def insert_voting_record(vote, deputy_id):
    """Insert voting record of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        vote['deputy_id'] = deputy_id

        cursor.execute(
            """
            INSERT OR REPLACE INTO votings (deputy_id, voting_id, voting_date, bulletin_number, document_title, article_text, voted_option, total_approved, total_rejected, total_abstention, result)
            VALUES (:deputy_id, :voting_id, :date, :description, :name, :article, :vote_option, :total_yes, :total_no, :total_abstention, :result)
            """,
            vote
        )
        cursor.close()


def find_deputy_votings(deputy_id):
    """
    Find votings of a deputy in the database.
    Returns a list of dictionaries.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding votings for deputy {deputy_id} in database")
        cursor.execute(
            """
            SELECT * FROM votings WHERE deputy_id = :deputy_id
            ORDER BY voting_date DESC
            """,
            {"deputy_id": deputy_id}
        )
        rows = cursor.fetchall()
        cursor.close()
    return rows


def insert_law_project_record(law_proj, deputy_id):
    """Insert law project record of a deputy into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting law project record for deputy {} into database".format(
                deputy_id
            )
        )
        law_proj['deputy_id'] = deputy_id
        law_proj['project_type'] = "Moción"
        cursor.execute(
            """
            INSERT OR REPLACE INTO law_projects (deputy_id, project_id, project_name, project_type, project_status, project_date)
            VALUES (:deputy_id, :project_id, :project_name, :project_type, :project_status, :project_date)
            """,
            law_proj
        )
        cursor.close()


def find_law_projects_for_deputy(deputy_id):
    """
    Find law projects for a deputy in the database.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding law projects for deputy {deputy_id} in database")
        cursor.execute(
            """
            SELECT * FROM law_projects WHERE deputy_id = :deputy_id
            """,
            {"deputy_id": deputy_id}
        )
        rows = cursor.fetchall()
        cursor.close()
    return rows


def insert_deputy_of_the_day(record):
    """Insert deputy of the day into the database."""
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(
            "inserting deputy of the day record for deputy {} into database".format(
                record['deputy_id']
            )
        )
        cursor.execute(
            """
            INSERT OR REPLACE INTO deputy_of_the_day (deputy_id, date, chain_id, pulse_id, rand_out)
            VALUES (:deputy_id, :date, :chain_id, :pulse_id, :rand_out)
            """,
            record
        )
        cursor.close()

def find_deputy_for_date(date):
    """
    Find deputy of the day for a given date.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding deputy of the day for date {date} in database")
        cursor.execute(
            """
            SELECT deputy_id, chain_id, pulse_id, rand_out FROM deputy_of_the_day WHERE date = :date
            """,
            {"date": date}
        )
        row = cursor.fetchone()
        cursor.close()
    return row


def find_last_N_months_with_records(N, table, deputy_id):
    """
    Find the last N months with records in a given table.
    """
    with DatabaseConnection() as db:
        cursor = db.cursor()
        logging.debug(f"finding last {N} months with records for deputy {deputy_id} in database")
        cursor.execute(
            """
            SELECT DISTINCT year, month FROM {}
            WHERE deputy_id = :deputy_id
            ORDER BY year DESC, month DESC
            LIMIT :N
            """.format(table),
            {"N": N, "deputy_id": deputy_id}
        )
        rows = cursor.fetchall()
        cursor.close()
    return rows