import logging

from flask import Flask

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])


def create_app(config_class='config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from .controllers import spaceship
    app.register_blueprint(spaceship.app)

    return app
