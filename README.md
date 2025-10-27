# AuthService

AuthService/ folder structure

```
amazon/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py         # Handles settings and environment variables
│   │   ├── security.py       # JWT and password hashing logic
│   │   └── oauth.py          # OAuth clients setup
│   │   └── kafka.py          # Kafka producer/consumer
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── auth.py   # API routes for login, token, etc.
│   ├── dependencies.py       # Dependency injection for common objects
│   └── main.py             # Main FastAPI application
├── tests/
├── .env.example
├── Dockerfile
└── requirements.txt
```