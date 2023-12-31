import os
import dotenv

dotenv.load_dotenv()


def str2bool(v):
  if v is None:
    return False
  return v.lower() in ("yes", "true", "t", "1")


AN_API_KEY = os.getenv("AN_API_KEY")
DEV_MODE = str2bool(os.getenv("DEV_MODE"))
DEV_DISABLE_FOREIGN_KEY_CHECKS = str2bool(os.getenv("DEV_DISABLE_FOREIGN_KEY_CHECKS"))
POSTGRES_URL = os.getenv("POSTGRES_URL")
