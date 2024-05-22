from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from typing import List

db = SQLAlchemy()


class Production(db.Model):
    __tablename__ = 'production'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('products.id'), nullable=False)
    quantity_produced: Mapped[int] = mapped_column(nullable=False)
    date_produced: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    product: Mapped['Product'] = db.relationship(back_populates='production')

    def __repr__(self):
        return f"<Production {self.id}|{self.product_id}>"