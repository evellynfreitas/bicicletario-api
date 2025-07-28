import os

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

if os.getenv("API_ALUGUEL_URL"):
    API_ALUGUEL_URL = "hhttps://bicicletario-api-aluguel.onrender.com"
else:
    API_ALUGUEL_URL = "http://localhost:8002"