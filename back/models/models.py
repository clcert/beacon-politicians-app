from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_engine():
    return create_engine('sqlite:///deputies.db')

def init_db():
    Base.metadata.create_all(bind=get_engine())

class Base(DeclarativeBase):
    def save_or_update(self, refresh=False):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        qry_object = session.query(self.__class__).filter(self.__class__.id == self.id).first()
        if qry_object:
            for key, value in self.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(qry_object, key, value)
        else:
            session.add(self)
        session.commit()
        if refresh:
            session.refresh(self)
        session.close()

    def save_if_not_exists(self):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        qry_object = session.query(self.__class__).filter(self.__class__.id == self.id).first()
        if not qry_object:
            session.add(self)
            session.commit()
        session.close()

    def as_dict(self):
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }

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

    @classmethod
    def get_deputy_by_local_id(cls, local_id):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        deputy = session.query(cls).filter(cls.local_id == local_id).first()
        session.close()
        return deputy

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

    def save_or_update(self):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        obj_class = self.__class__
        qry_object = session.query(obj_class).filter(
            obj_class.deputy_id == self.deputy_id,
            obj_class.start_date == self.start_date,
            obj_class.end_date == self.end_date
        ).first()
        if qry_object:
            for key, value in self.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(qry_object, key, value)
        else:
            session.add(self)
        session.commit()
        session.close()

    def save_if_not_exists(self):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        obj_class = self.__class__
        qry_object = session.query(obj_class).filter(
            obj_class.deputy_id == self.deputy_id,
            obj_class.start_date == self.start_date,
            obj_class.end_date == self.end_date
        ).first()
        if not qry_object:
            session.add(self)
            session.commit()
        session.close()

class DocumentTypes:
    LAW_PROJECT = 'Proyecto de Ley'
    OTHER = 'Otros'

class Document(Base):
    __tablename__ = 'document'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(String)
    document_type: Mapped[str] = mapped_column(String)
    bulletin_id: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    approval_votes: Mapped[int] = mapped_column(Integer)
    rejection_votes: Mapped[int] = mapped_column(Integer)
    abstention_votes: Mapped[int] = mapped_column(Integer)

    deputy_votings: Mapped[List['DeputyVoting']] = relationship(
        'DeputyVoting', back_populates='document'
    )


class DeputyVoting(Base):
    __tablename__ = 'deputy_voting'

    id: Mapped[int] = mapped_column(primary_key=True)
    deputy_id: Mapped[int] = mapped_column(ForeignKey('deputy.id'))
    document_id: Mapped[int] = mapped_column(ForeignKey('document.id'))
    vote: Mapped[str] = mapped_column(String)

    document: Mapped['Document'] = relationship(
        'Document', back_populates='deputy_votings'
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

class AppErrorLog(Base):
    __tablename__ = 'error'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String, default=datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    @classmethod
    def create(cls, err_type, source, exception):
        logger.error(f"error:\n{exception}")
        AppErrorLog(
            code=err_type.code,
            description=err_type.description,
            source=source
        ).save()
        exit(1)

    def save(self):
        Session = sessionmaker(bind=get_engine())
        session = Session()
        session.add(self)
        session.commit()
        session.close()