# Project 1
#Goodread api
#api key: TwVykWZjLcLSFJlI9L75KQ
#export GOODREADS_API_KEY=TwVykWZjLcLSFJlI9L75KQ
#secret: aMKGZMApmClzYwEvR7aMvGGxsMMNcg4QmExhf1qzc
#export SECRET_KEY=aMKGZMApmClzYwEvR7aMvGGxsMMNcg4QmExhf1qzc
#Database uri: postgres://lakbjupmxtbnrt:ae49e5868286d15a7280ddc9bee116ae3d473d7b1792637d3a1013c88350a218@ec2-54-75-231-215.eu-west-1.compute.amazonaws.com:5432/d2qf55bkosfsou
#export DATABASE_URL=postgres://lakbjupmxtbnrt:ae49e5868286d15a7280ddc9bee116ae3d473d7b1792637d3a1013c88350a218@ec2-54-75-231-215.eu-west-1.compute.amazonaws.com:5432/d2qf55bkosfsou
#Password Postgresql: ae49e5868286d15a7280ddc9bee116ae3d473d7b1792637d3a1013c88350a218
### Web Programming with Python and JavaScript

This project is a web application which provides ability to users to leave their reviews about book(s), selected from database and can see reviews made by other people. This web app uses a third-party API provided by GoodReads ( another book review website ) to fetch their ratings and review data also. This project also provide a API to query for reviews and info about a particular book via its api route.

### TEST RUN

https://books-xpt1x.herokuapp.com/ 
> Powered by Heroku

## USAGE

- Login / Register the user account
- Search for a book via ISBN / Title / Author
- Get details about book and ratings from GoodReads
- Provide a rating and submit a review
- Fetch details about a ISBN using **API ROUTE** ( /api/' isbn ' ) 
> Ex: http://your-site/api/031606792X

## INSTALL 

Python3 is required

```bash
# setup environment variables
$ export FLASK_APP=application.py
$ export DATABASE_URL=''
$ export GOODREADS_API_KEY=''

# this is unique identifier for your app
$ export SECRET_KEY=''

# clone this repo with git
$ git clone https://github.com/xpt1x/Project1.git
$ cd Project1
$ pip install -r requirements.txt

# now create tables and import data from csv
$ python create.py
$ python import.py

# finally run the application
$ flask run
```

> Note: Mysqlclient is required: [Install MysqlClient](https://github.com/PyMySQL/mysqlclient-python) if you want to use MYSQL as your db

> Get your DATABASE_URL from your DATABASE Credentials 

> Get your [GOODREADS_API_KEY](https://www.goodreads.com/api)
