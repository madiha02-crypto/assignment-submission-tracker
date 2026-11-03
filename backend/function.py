from fastapi import HTTPException
from sqlalchemy import Integer,String, Column, create_engine, DateTime,ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime , date

DB_PATH="Assigment.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Assigment (Base):
    __tablename__ = "assigments"
    id = Column(Integer, primary_key=True )
    course = Column(String)
    title = Column(String)
    max_marks = Column(Integer)
    due_at = Column(DateTime , default=datetime.now)
    late_until = Column(DateTime , default=datetime.now)  
    created_on= Column(DateTime , default=datetime.now)
  

    
class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    assigment_id = Column(Integer, ForeignKey("assigment_id"))
    roll_no = Column(Integer)
    link = Column(String  )
    Submitted_at = Column(DateTime,nullable=True )  
    is_late = Column(Integer)  
    marks = Column(float,nullable=True)  
    feedback =Column(String)
    status = Column(bool)

Base.metadata.create_all(engine)




   