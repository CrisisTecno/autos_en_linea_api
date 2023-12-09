from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from config.database import connect_to_database
from api.catalogo.catalogo import catalogo_fl
from api.distribuidor.distribuidor import distribuidor_fl
from api.sucursal.sucursal import sucursal_fl
import asyncio

app = Flask(__name__)
app.env = "development"

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response



app.register_blueprint(catalogo_fl, url_prefix='/catalogo')
app.register_blueprint(distribuidor_fl, url_prefix='/distribuidor')
app.register_blueprint(sucursal_fl, url_prefix='/sucursal')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
