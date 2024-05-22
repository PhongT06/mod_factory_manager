from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from typing import List

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    position: Mapped[str] = mapped_column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Employee {self.id}|{self.name}>"