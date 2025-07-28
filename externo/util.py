import os

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
API_ALUGUEL_URL = os.getenv("API_ALUGUEL_URL", "http://localhost:8002")