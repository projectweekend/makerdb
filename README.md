makerdb
====================


Running Tests
====================

Tests, with code coverage reporting can be ran with the following command:
```
docker-compose run web nosetests -v --with-coverage --cover-package=app --cover-xml --cover-html
```


Create DynamoDB Tables
====================

The following script will create the all the app tables in DynamoDB. Before running it be sure the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables are defined in the `hidden.env` file:
```
docker-compose run web python create_tables.py
```
