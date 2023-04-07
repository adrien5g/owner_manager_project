import logging
from typing import Callable
from waitress import serve
from flask import Flask, Blueprint
from flask_pydantic_openapi import FlaskPydanticOpenapi
from utils import get_doc

class ApiHandler:

    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.doc: FlaskPydanticOpenapi = get_doc()

    def register_blueprint(self, blueprint: Blueprint) -> None:
        self.app.register_blueprint(blueprint)

    def register_middleware(self, function: Callable) -> None:
        self.app.before_request(function)

    def start(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.info('Running on host http://0.0.0.0:5000')

        self.doc.register(self.app)
        serve(self.app, host="0.0.0.0", port=5000)
