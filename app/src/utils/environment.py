from os import getenv


def get_bool(key: str, default: bool) -> bool:
    return getenv(key, str(default)) == "True"


LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

HOST = getenv("HOST", "0.0.0.0")  # noqa: S104
PORT = int(getenv("PORT", "8000"))

ADMIN_USERNAME = getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD", "admin")

DB_DRIVER: str = getenv("DB_DRIVER", "mysql+aiomysql")
DB_HOST: str = getenv("DB_HOST", "localhost")
DB_PORT: int = int(getenv("DB_PORT", "3306"))
DB_DATABASE: str = getenv("MYSQL_DATABASE", "db")
DB_USERNAME: str = getenv("MYSQL_USER", "admin")
DB_PASSWORD: str = getenv("MYSQL_PASSWORD", "admin")
POOL_RECYCLE: int = int(getenv("POOL_RECYCLE", 300))
POOL_SIZE: int = int(getenv("POOL_SIZE", 20))
MAX_OVERFLOW: int = int(getenv("MAX_OVERFLOW", 20))
SQL_SHOW_STATEMENTS: bool = get_bool("SQL_SHOW_STATEMENTS", False)

SECRET_KEY: str = getenv("SECRET_KEY", "a_random_string")
ALGORITHM: str = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
