import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Print variables to check if they are loaded
print("FLASK_SECRET_KEY:", os.getenv("FLASK_SECRET_KEY"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_NAME:", os.getenv("DB_NAME"))
