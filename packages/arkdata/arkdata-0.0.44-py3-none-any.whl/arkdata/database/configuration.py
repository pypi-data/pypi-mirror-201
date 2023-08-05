import os
from dotenv import dotenv_values
from collections import defaultdict


config = defaultdict(lambda: None)
config.update({
    **dotenv_values(".env.secret"),     # load sensitive variables
    **dotenv_values(".env"),
    **os.environ,                       # override loaded values with environment variables
})

DATABASE_USERNAME = config['MYSQL_USERNAME'] or 'root'
DATABASE_PASSWORD = config['MYSQL_PASSWORD'] or 'password'

DATABASE_HOST = "127.0.0.1"
DATABASE_PORT = "3306"
DATABASE = "ark"
DATABASE_URI = f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}"

TEST_DATABASE_HOST = "127.0.0.1"
TEST_DATABASE_PORT = "3306"
TEST_DATABASE = "test_ark"
TEST_DATABASE_URI = f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{TEST_DATABASE_HOST}:{TEST_DATABASE_PORT}/{TEST_DATABASE}"

