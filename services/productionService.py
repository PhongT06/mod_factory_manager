from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.production import Production
from models.product import Product

def save(production_data):
    with Session(db.engine) as session:
        with session.begin():
            product_id = production_data['product_id']
            product = session.get(Product, product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} does not exist")

            new_production = Production(
                product_id=product_id,
                quantity_produced=production_data['quantity_produced'],
                date_produced=production_data['date_produced']
            )
            session.add(new_production)
            session.commit()
            session.refresh(new_production)
            session.refresh(product)
            return new_production

def find_all():
    query = select(Production)
    production_records = db.session.execute(query).scalars().all()
    return production_records

def find_by_id(production_id):
    production_record = db.session.get(Production, production_id)
    return production_record