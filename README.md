Environment Variables
====================

There are just a couple of configurations managed as environment variables. In the development environment, these are injected by Docker Compose and managed in the `docker-compose.yml` file.

* `DATABASE_URL` - This is the connection URL for the PostgreSQL database. It is not used in the **development environment**.
* `DEBUG` - This toggles debug mode for the app to True/False.
* `SECRET_KEY` - This is a secret string that you make up. It is used to encrypt and verify the authentication token on routes that require authentication. This is required. The app won't start without it.



Database Migrations
====================

Database migrations are handled by [Flyway](http://flywaydb.org/) and files are stored in the `/sql` directory. Migrations are automatically applied when running tests with Nose. You can run migrations manually in the development environment using `docker-compose` too. The included script `local_migrate.sh` uses an environment variable created by [Docker Compose](https://docs.docker.com/compose/env/) to find the IP address assigned to the database and execute the Flyway command to run migrations.

```
docker-compose run web ./local_migrate.sh
```



Running Tests
====================

Tests, with code coverage reporting can be ran with the following command:
```
docker-compose run web nosetests -v --with-coverage --cover-erase --cover-package=app --cover-xml --cover-html
```


API Routes
====================


### Authenticate a user

**POST:**
```
/v1/authenticate
```

**Body:**
```json
{
    "email": "something@email.com",
    "password": "12345678"
}
```

**Response:**
```json
{
    "token": "reallylongjsonwebtokenstring"
}
```

**Status Codes:**
* `200` if successful
* `400` if incorrect data provided
* `401` if invalid credentials


### Register a user

**POST:**
```
/v1/user
```

**Body:**
```json
{
    "email": "something@email.com",
    "password": "12345678"
}
```

**Response:**
```json
{
    "token": "reallylongjsonwebtokenstring"
}
```

**Status Codes:**
* `201` if successful
* `400` if incorrect data provided
* `409` if email is in use


### Add an inventory item

**POST:**
```
/v1/inventory-item
```

**Body:**
```json
{
    "name": "Cool Item",
    "url": "http://www.adafruit.com/products/2466",
    "image_url": "http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif",
    "quantity": 1,
    "vendor_name": "Adafruit",
    "vendor_item_id": "2466"
}
```

**Response:**
```json
{
    "id": 1,
    "user_id": 1,
    "name": "Cool Item",
    "url": "http://www.adafruit.com/products/2466",
    "image_url": "http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif",
    "quantity": 1,
    "vendor_name": "Adafruit",
    "vendor_item_id": "2466"
}
```

**Status Codes:**
* `201` if successful
* `400` if incorrect data provided
* `401` if not authenticated


### List inventory items

**GET:**
```
/v1/inventory-item
```

**Query Parameters:**

* `skip`: The number of records to skip for pagination (integer - required)
* `take`: The number of records to take for pagination (integer - required)

**Response:**
```json
{
    count: 1,
    items: [
        {
            "id": 1,
            "user_id": 1,
            "name": "Cool Item",
            "url": "http://www.adafruit.com/products/2466",
            "image_url": "http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif",
            "quantity": 1,
            "vendor_name": "Adafruit",
            "vendor_item_id": "2466"
        }
    ]
}
```

**Status Codes:**
* `200` if successful
* `400` if `skip` or `take` is missing
* `401` if not authenticated


### Get an inventory item

**GET:**
```
/v1/inventory-item/:id
```

**Response:**
```json
{
    "id": 1,
    "user_id": 1,
    "name": "Cool Item",
    "url": "http://www.adafruit.com/products/2466",
    "image_url": "http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif",
    "quantity": 1,
    "vendor_name": "Adafruit",
    "vendor_item_id": "2466"
}
```

**Status Codes:**
* `200` if successful
* `401` if not authenticated
* `404` if not found


### Update an inventory item

**PUT:**
```
/v1/inventory-item/:id
```

**Body:**
```json
{
    "name": "Cool Item",
    "url": "http://www.adafruit.com/products/2466",
    "image_url": "http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif",
    "quantity": 1,
    "vendor_name": "Adafruit",
    "vendor_item_id": "2466"
}
```

**Response:**
```json
{
    "id": 1,
    "user_id": 1,
    "name": "Cool Item",
    "url": "http://www.adafruit.com/products/2466",
    "image_url": "http://www.adafruit.com/images/970x728/2466-05.gif.pagespeed.ce.7pXsy73MYp.gif",
    "quantity": 1,
    "vendor_name": "Adafruit",
    "vendor_item_id": "2466"
}
```

**Status Codes:**
* `200` if successful
* `400` if incorrect data provided
* `401` if not authenticated
* `404` if not found


### Delete an inventory item

**DELETE:**
```
/v1/inventory-item/:id
```

**Body:** None

**Response:** None

**Status Codes:**
* `204` if successful
* `401` if not authenticated
* `404` if not found
