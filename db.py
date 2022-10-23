import os


DATABASE_NAME = os.environ.get("DB_CONN", "yoyo")


class DbService:
    TABLE_NAME = "tags"

    def get_connection(self) -> str:
        return DATABASE_NAME


db_service = DbService()
