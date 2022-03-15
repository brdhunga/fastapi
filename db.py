import os


DATABASE_NAME = os.environ["DB_CONN"]


class DbService:
    TABLE_NAME = "tags"

    def get_connection(self) -> str:
        return DATABASE_NAME


db_service = DbService()