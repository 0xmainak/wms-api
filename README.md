# current file structure

```
├── app
│   ├── api
│   │   ├── health.py
│   │   └── router.py
│   ├── config.py
│   ├── core
│   │   ├── permissions.py
│   │   └── security.py
│   ├── dependencies.py
│   ├── infrastructure
│   │   ├── cache
│   │   │   └── redis.py
│   │   └── db
│   │       ├── base.py
│   │       ├── seed.py
│   │       └── session.py
│   ├── lifespan.py
│   ├── main.py
│   ├── middleware
│   │   └── auth.py
│   └── modules
│       ├── auth
│       │   ├── models.py
│       │   ├── repository.py
│       │   ├── router.py
│       │   ├── schemas.py
│       │   └── service.py
│       ├── roles
│       │   ├── models.py
│       │   ├── repository.py
│       │   ├── router.py
│       │   ├── schemas.py
│       │   └── service.py
│       └── users
│           ├── models.py
│           ├── repository.py
│           ├── router.py
│           ├── schemas.py
│           └── service.py
├── pyproject.toml
├── README.md
├── test.py
└── uv.lock
```