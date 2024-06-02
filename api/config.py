from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

from os import environ as env

VERSION: str = env.get("version", "0.0.1")
DATABASE_URI: str = env.get("DATABASE_URI")
SECRET_KEY: str = env.get("SECRET_KEY")
if SECRET_KEY is None:
    raise Exception("SECRET_KEY must not be none!!!")