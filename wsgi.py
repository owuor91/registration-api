from app import create_app
from config import ProductionConfig
from db import db

app = create_app(ProductionConfig)
with app.app_context():
    db.create_all()
