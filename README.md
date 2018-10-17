[![Build Status](https://travis-ci.org/kizzanaome/Fast-foods-Fast-db.svg?branch=ft-challenge3)](https://travis-ci.org/kizzanaome/Fast-foods-Fast-db)
[![Coverage Status](https://coveralls.io/repos/github/kizzanaome/Fast-Food-Fast/badge.svg?branch=develop)](https://coveralls.io/github/kizzanaome/Fast-Food-Fast?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c45f17847a054f958174c194ce396998)](https://www.codacy.com/app/kizzanaome/Fast-Food-Fast?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kizzanaome/Fast-Food-Fast&amp;utm_campaign=Badge_Grade)

# Fast-foods-Fast-db
Fast-Food-Fast is a food delivery service app for a restaurant.


## Requirements
- `Python3.4` - programming language that can be used on any modern computer operating system. 
- `Flask` - Python based web framework
- `Virtualenv` - Allows you to work on a specific project without worry of affecting other projects.
- `python-pip` - Package management system used to install and manage software packages,its a replacemnt of easy_install

## Functionality
- `Add food_menu` Enables admin user to create a food item
- `Get food_menu` Enables user to view the food items available
- `Add order` Enables user to place a  desired food order
- `Edit order` Enables an admin user to edit the status of an order
- `Delete order` User can delete an order
- `View orders` admin User can view all orders created
- `view a single order` admin User can fetch a specific order by its id


## To view the API on Heroku 
Copy this url paste it in a new tab
```
- https://noma-fast-food-fast-db.herokuapp.com/

```

## Installation
First clone this repository
```
$ git clone https://github.com/kizzanaome/Fast-Food-db/tree/ft-challenge3
$ cd Fast-Food-Fast
```
Create virtual environment and install it
```
$ virtualenv venv
$ source/venv/bin/activate
```
Then install all the necessary dependencies
```
pip install -r requirements.txt
```
#Install all the necessary dependencies by
```
$ pip install -r requirements.txt
$ Install PostgreSQL
$ CREATE DATABASE fast_food_db
$ CREATE TABLE users
$ CREATE TABLE orders
$ CREATE TABLE food_menu
```

## Run the application
At the terminal or console type
```
python run.py
```
To run tests run this command at the console/terminal
```
pytest
```
## Versioning
```
This API is versioned using url versioning starting, with the letter 'v'
This is version one"v2" of the API
```


## End Points
|           End Point                      |     Functionality     |
|   -------------------------------------- |-----------------------|
|     POST api/v1/orders                   | Place a new order     |  
|     GET  api/v1/orders                   | Get all the orders.   |   
|     GET  api/v1/orders/order_id          |Fetch a specific order |  
|     PUT api/v1/orders/order_id           |Update the status of an order.|
|     DELETE api/v1/orders                 |Delete a specific order|   
|     POST api/v1/food_items               |Create a food_item     |   
|     GET api/v1/food_items                |Fetch all food_items   |   


## Contributors
- Naome