from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import STRING
from boto.exception import JSONResponseError


def create_makerdb_users():
    Table.create(
        'makerdb_users',
        schema=[
            HashKey('email', data_type=STRING)
        ],
        throughput={
            'read': 1,
            'write': 1
        }
    )


def main():

    tasks = [
        create_makerdb_users
    ]

    for task in tasks:
        try:
            task()
        except JSONResponseError as e:
            print(e.message)


if __name__ == '__main__':
    main()
