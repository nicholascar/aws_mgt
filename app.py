import logging
import settings
from flask import Flask
from routes import routes
app = Flask(__name__)
app.register_blueprint(routes)


if __name__ == '__main__':
    logging.basicConfig(filename=settings.AWS_API_HOME + 'aws_mgt.log',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%dT%H:%M:%S',
                        format='%(asctime)s %(levelname)s %(message)s')

    app.run(host='0.0.0.0', port=settings.PORT, debug=settings.DEBUG)