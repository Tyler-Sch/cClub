from flask.cli import FlaskGroup
from user_server.userServer import app

cli = FlaskGroup(app)


if __name__ == '__main__':
    cli()
