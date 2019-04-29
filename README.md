# Cooking Club

Inspired by Tinder, I created a website for finding recipes in a visual and fun way.
Add the ones you want to a recipe list, automatically generate a grocery list,
and get cooking. Many technologies have been used to create the base version
of this web page and I'm excited to add more features. Main components include react client for the front end, a recipe database and api, a user database and api, a recurrent neural network for part of speech tagging of ingredients, webscrapers, up to 1 million recipes, and nginx set up as a reverse proxy.

### Prerequisites:

For simple build:
```
  docker
  docker-compose
```

### Installation:
Set up system:
  create a directory and clone repository
```
  git clone https://github.com/wintermutestoothache/cClub.git
  cd cClub
```
for prod version:
```
  export REACT_APP_USERS_SERVICE_URL=http://localhost
  export REACT_APP_RECIPES_SERVICE_URL=http://localhost
  docker-compose -f docker-compose-prod.yml up --build -d

  docker-compose -f docker-compose-prod.yml exec -T recipes-db psql recipes_test -U postgres < ./services/recipeAPI/server/db/currentDBdump.sql

  docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
  ```

  open a browser and navigate to http://localhost

## See a live demo version at:

 http://35.172.185.176

## Built with:

* [Sanic](https://github.com/huge-success/sanic) - python3.6 based async web server
* [AsyncPG](https://magicstack.github.io/asyncpg/current/) - python async database interface library
* [Postgres](https://www.postgresql.org/)

* [Kera](https://keras.io/) - a framework for developing neural networks
* [Pandas](https://pandas.pydata.org/) - data analysis framework

* [Flask](http://flask.pocoo.org/) - basic web microframework
* [SQLAlchemy](https://www.sqlalchemy.org/) - python based ORM

* [Nginx](https://www.nginx.com/resources/wiki/) - open-source http server and reverse proxy

* [React](https://reactjs.org/)

And many others.
