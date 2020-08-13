from app import create_app
from config import ProductionConfig
from db import db

app = create_app(ProductionConfig)
db.create_all(app)
