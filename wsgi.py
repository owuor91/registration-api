from app import create_app
from config import ProductionConfig

app = create_app(ProductionConfig)
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'reallynicee38y72piebird'
jwt = JWTManager(app)
