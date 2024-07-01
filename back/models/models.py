from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

def get_engine():
    return create_engine('sqlite:///deputies.db')

def init_db(engine):
    Base.metadata.create_all(bind=engine)

class Base(DeclarativeBase):
    pass

class DailyDeputy(Base):
    __tablename__ = 'daily_deputy'

    id: Mapped[int] = mapped_column(primary_key=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    date: Mapped[str] = mapped_column(String)
    chain_index: Mapped[int] = mapped_column(Integer)
    pulse_index: Mapped[int] = mapped_column(Integer)
    pulse_value: Mapped[str] = mapped_column(String)

    deputy: Mapped['Deputy'] = relationship('Deputy', back_populates='daily_deputy')

class Deputy(Base):
    __tablename__ = 'deputy'

    id: Mapped[int] = mapped_column(primary_key=True)
    local_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    father_surname: Mapped[str] = mapped_column(String)
    mother_surname: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    birth_date: Mapped[str] = mapped_column(String)
    profession: Mapped[str] = mapped_column(String, nullable=True)
    district_number: Mapped[int] = mapped_column(Integer)
    district_region: Mapped[str] = mapped_column(String)
    district_communes: Mapped[str] = mapped_column(String)
    party_name: Mapped[str] = mapped_column(String)
    party_acronym: Mapped[str] = mapped_column(String)
    twitter_usr: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    instagram_usr: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_update: Mapped[str] = mapped_column(String)

    daily_deputy: Mapped[List['DailyDeputy']] = relationship(
        'DailyDeputy', back_populates='deputy'
    )
    parlamentary_periods: Mapped[List['ParlamentaryPeriod']] = relationship(
        'ParlamentaryPeriod', back_populates='deputies'
    )
    deputy_votings: Mapped[List['DeputyVoting']] = relationship(
        'DeputyVoting', back_populates='deputy'
    )
    deputy_projects: Mapped[List['DeputyProject']] = relationship(
        'DeputyProject', back_populates='deputy'
    )
    support_staff_expenses: Mapped[List['SupportStaffExpense']] = relationship(
        'SupportStaffExpense', back_populates='deputy'
    )
    operational_expenses: Mapped[List['OperationalExpense']] = relationship(
        'OperationalExpense', back_populates='deputy'
    )
    attendance: Mapped['Attendance'] = relationship(
        'Attendance', back_populates='deputy'
    )

class ParlamentaryPeriod(Base):
    __tablename__ = 'parlamentary_period'

    id: Mapped[int] = mapped_column(primary_key=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)

    deputies: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='parlamentary_periods'
    )

class Bulletin(Base):
    __tablename__ = 'bulletin'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String)
    bulletin_title: Mapped[str] = mapped_column(String)
    bulletin_description: Mapped[str] = mapped_column(String)
    bulletin_status: Mapped[str] = mapped_column(String)
    approval_votes: Mapped[int] = mapped_column(Integer)
    rejection_votes: Mapped[int] = mapped_column(Integer)
    abstention_votes: Mapped[int] = mapped_column(Integer)

    deputy_votings: Mapped[List['DeputyVoting']] = relationship(
        'DeputyVoting', back_populates='bulletin'
    )

class DeputyVoting(Base):
    __tablename__ = 'deputy_voting'

    id: Mapped[int] = mapped_column(primary_key=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    bulletin_id: Mapped[int] = mapped_column(ForeignKey('bulletin.id'))
    vote: Mapped[str] = mapped_column(String)

    bulletin: Mapped['Bulletin'] = relationship(
        'Bulletin', back_populates='deputy_votings'
    )
    deputy: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='deputy_votings'
    )

class LawProject(Base):
    __tablename__ = 'law_project'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    creation_date: Mapped[str] = mapped_column(String)

    authors: Mapped[List['DeputyProject']] = relationship(
        'DeputyProject', back_populates='law_project'
    )

class DeputyProject(Base):
    __tablename__ = 'deputy_project'

    id: Mapped[int] = mapped_column(primary_key=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    project_id: Mapped[int] = mapped_column(ForeignKey('law_project.id'))

    deputy: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='deputy_projects'
    )
    law_project: Mapped['LawProject'] = relationship(
        'LawProject', back_populates='authors'
    )

class SupportStaffExpense(Base):
    __tablename__ = 'support_staff_expense'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    year: Mapped[int] = mapped_column(Integer)
    month: Mapped[int] = mapped_column(Integer)
    hired_staff: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)

    deputy: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='support_staff_expenses'
    )

class OperationalExpense(Base):
    __tablename__ = 'operational_expense'

    id: Mapped[int] = mapped_column(primary_key=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    type: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    month: Mapped[int] = mapped_column(Integer)
    amount: Mapped[int] = mapped_column(Integer)

    deputy: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='operational_expenses'
    )

class Attendance(Base):
    __tablename__ = 'attendance'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    total_sessions: Mapped[int] = mapped_column(Integer)
    total_attended: Mapped[int] = mapped_column(Integer)
    total_justified: Mapped[int] = mapped_column(Integer)
    total_unjustified: Mapped[int] = mapped_column(Integer)

    deputy: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='attendance'
    )

