from app import config
from boto.dynamodb2.layer1 import DynamoDBConnection


def get_dynamodb_connection():
    if config.DOCKER_DB_HOST and config.DOCKER_DB_PORT:
        # If running in Docker Compose, connect to local dynamodb
        return DynamoDBConnection(
            host=config.DOCKER_DB_HOST,
            port=int(config.DOCKER_DB_PORT),
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)
    # If not running in Docker Compose, let boto do it's default thing
    return None


dynamodb_connection = get_dynamodb_connection()
