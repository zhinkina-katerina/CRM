import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROM_CLIENT_TOKEN = os.getenv("PROM_CLIENT_TOKEN")
    NOVA_POSHTA_CLIENT_TOKEN = os.getenv("NOVA_POSHTA_CLIENT_TOKEN")


settings = Settings()
