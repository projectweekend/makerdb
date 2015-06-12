makerdb
====================


Running Tests
====================

Tests, with code coverage reporting can be ran with the following command:
```
docker-compose run web nosetests -v --with-coverage --cover-package=app --cover-xml --cover-html
```
