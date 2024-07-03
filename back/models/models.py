from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

def get_engine():
    return create_engine('sqlite:///deputies.db')

def init_db():
    Base.metadata.create_all(bind=get_engine())

class Base(DeclarativeBase):
    @classmethod
    def save_or_update(cls, new_obj):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        qry_object = session.query(cls).filter(cls.id == new_obj.id).first()
        if qry_object:
            for key, value in new_obj.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(qry_object, key, value)
        else:
            session.add(new_obj)
        session.commit()
        session.close()

    @classmethod
    def save_if_not_exists(cls, new_obj):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        qry_object = session.query(cls).filter(cls.id == new_obj.id).first()
        if not qry_object:
            session.add(new_obj)
            session.commit()
        session.close()

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
    birth_date: Mapped[str] = mapped_column(String, nullable=True)
    profession: Mapped[str] = mapped_column(String)
    district_number: Mapped[int] = mapped_column(Integer)
    district_region: Mapped[str] = mapped_column(String)
    district_communes: Mapped[str] = mapped_column(String)
    party_name: Mapped[str] = mapped_column(String)
    party_acronym: Mapped[str] = mapped_column(String, nullable=True)
    twitter_usr: Mapped[Optional[str]] = mapped_column(String)
    instagram_usr: Mapped[Optional[str]] = mapped_column(String)
    last_update: Mapped[str] = mapped_column(String, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    daily_deputy: Mapped[List['DailyDeputy']] = relationship(
        'DailyDeputy', back_populates='deputy'
    )
    deputy_periods: Mapped[List['DeputyPeriod']] = relationship(
        'DeputyPeriod', back_populates='deputies'
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

class DeputyPeriod(Base):
    __tablename__ = 'deputy_period'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str] = mapped_column(String)

    deputies: Mapped['Deputy'] = relationship(
        'Deputy', back_populates='deputy_periods'
    )

    __table_args__ = (
        UniqueConstraint('deputy_id', 'start_date', 'end_date', name='deputy_periods_unique'),
    )

    @classmethod
    def save_or_update(cls, new_obj):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        qry_object = session.query(cls).filter(
            cls.deputy_id == new_obj.deputy_id,
            cls.start_date == new_obj.start_date,
            cls.end_date == new_obj.end_date
        ).first()
        if qry_object:
            for key, value in new_obj.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(qry_object, key, value)
        else:
            session.add(new_obj)
        session.commit()
        session.close()

    @classmethod
    def save_if_not_exists(cls, new_obj):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        qry_object = session.query(cls).filter(
            cls.deputy_id == new_obj.deputy_id,
            cls.start_date == new_obj.start_date,
            cls.end_date == new_obj.end_date
        ).first()
        if not qry_object:
            session.add(new_obj)
            session.commit()
        session.close()

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

    id: Mapped[str] = mapped_column(String,primary_key=True)
    name: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    creation_date: Mapped[str] = mapped_column(String)

    authors: Mapped[List['DeputyProject']] = relationship(
        'DeputyProject', back_populates='law_project'
    )

class DeputyProject(Base):
    __tablename__ = 'deputy_project'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    project_id: Mapped[str] = mapped_column(ForeignKey('law_project.id'))

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

