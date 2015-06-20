from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
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
    print('Table created: makerdb_users')


def create_makerdb_vendor_items():
    Table.create(
        'makerdb_vendor_items',
        schema=[
            HashKey('vendor_item_id', data_type=STRING),
            RangeKey('vendor_name', data_type=STRING)
        ],
        throughput={
            'read': 1,
            'write': 1
        }
    )
    print('Table created: makerdb_vendor_items')


def create_makerdb_user_items():
    Table.create(
        'makerdb_user_items',
        schema=[
            HashKey('user_email', data_type=STRING),
            RangeKey('name', data_type=STRING)
        ],
        throughput={
            'read': 1,
            'write': 1
        }
    )
    print('Table created: makerdb_user_items')


def main():

    tasks = [
        create_makerdb_users,
        create_makerdb_vendor_items,
        create_makerdb_user_items
    ]

    for task in tasks:
        try:
            task()
        except JSONResponseError as e:
            print(e.message)


if __name__ == '__main__':
    main()
