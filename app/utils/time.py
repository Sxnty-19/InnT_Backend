import os
import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_date():
    timezone_name = os.getenv("TIMEZONE", "UTC")
    zona_horaria = pytz.timezone(timezone_name)
    return datetime.now(zona_horaria)
