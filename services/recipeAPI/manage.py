import click
import os
from server.recipeServer import app

@click.group()
def main():
    pass


@main.command()
def start():
    if os.environ['APP_SETTINGS'] == 'DevelopmentConfig':
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()
