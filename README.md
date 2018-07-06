[![Build Status](https://travis-ci.org/byarustev/RideApi.svg?branch=develop)](https://travis-ci.org/byarustev/RideApi)
[![Maintainability](https://api.codeclimate.com/v1/badges/38f513cdfe1984e4be8a/maintainability)](https://codeclimate.com/github/byarustev/RideApi/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/byarustev/RideApi/badge.svg?branch=develop)](https://coveralls.io/github/byarustev/RideApi?branch=develop)

# RideMyWay API

RideMyWay is a carpooling web application that provides drivers with the ability to create ride offers
and passengers to join available ride offers.
	
## Features 
- users can signup on the api
- users can login into the api
- api provides a jwt for authentication at login and signup
- Users can post ride offers
- Passengers can request to join a ride
- Drivers can view, accept and reject join requests



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites

What things you need to install the software

* [PostgreSQL](https://www.postgresql.org/)
* Python 

### Installing

A step by step series of examples that tell you how to get a development env running

To deploy this application follow the following steps
* clone the project from git hub
* download [PostgreSQL](https://www.postgresql.org/) for setting up the database
* Install PostgreSQL and setup a server 
* create two database with a names "myway" and "myway_test"
* create a python virtual environment and install all the libraries in the "requirements.txt" file 
* navigate to the root of the project and execute the application by running a command "python run.py"

Once the application starts running. Then you can proceed to test the application using postman. The application by default runs on port 5000
. If everything is done perfect you will see a url like http://127.0.0.1:5000/ can be used to access the application through a browser.

These are the endpoints that are currently available


|__Type__| __Endpoint__ | __What the endpoint does__ | 
|------|-------------|------------|
|POST|  /api/v1/auth/signup       | used for signing up a user     |
|POST| /api/v1/auth/login        | used to login into the api | 
|POST|  /api/v1/users/rides       | used to create a new ride offer     |
|POST|  /api/v1/rides/<int:ride_id>/requests       | used to create a request to join a given ride     |
|GET|  /api/v1/rides/<int:ride_id>       | returns details of a given ride     |
|GET|  /api/v1/rides        | returns all the rides in the system     |
|GET|  /api/v1/users/rides/<int:ride_id>/requests       | returns all the requests that were made to a given ride offer     |
|PUT|  /api/v1/users/rides/<int:ride_id>/requests/<int:request_id>      | used to accept or reject a ride join request     |
|GET|  /api/v1/mytrips      | returns all the trips a user has even taken and the offers he/she has ever created     |




## Running the tests

Tests can be run by running the command below at the root of the project directory
```
if not installed run "pip install nose" to install nose 
then "nosetests" to run the test
```


You can also get the test coverage by running the command below. this requires you to have installed nose 

```
nosetests --with-coverage --cover-package=api
```

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - Python web framework used
* [PostgreSQL](https://www.postgresql.org/) - An open source object-relational database was used to store data
* [Flask-Jwt-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/) - Flask library Used to generate JWT tokens for authentication


## Versioning

URL Versioning has been used to version this applications endpoint 

Currently only version:1 is available 
