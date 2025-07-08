import os

if os.getenv("API_EXTERNO_URL"):
    API_EXTERNO_URL = "https://bicicletario-api.onrender.com"
else:
    API_EXTERNO_URL = "http://localhost:8001"


if os.getenv("API_ALUGUEL_URL"):
    API_ALUGUEL_URL = "hhttps://bicicletario-api-aluguel.onrender.com"
else:
    API_ALUGUEL_URL = "http://localhost:8002"

