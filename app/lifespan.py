from contextlib import asynccontextmanager

from sqlalchemy import text

from app.infrastructure.db.session import engine
from app.infrastructure.db.base import Base
from app.infrastructure.cache.redis import redis_client



@asynccontextmanager
async def lifespan(app):
    print("\n🚀 Starting WMS Backend...\n")

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ PostgreSQL connected")
    except Exception as e:
        print("❌ PostgreSQL connection failed")
        raise e

    try:
        redis_client.ping()
        print("✅ Redis connected")
    except Exception as e:
        print("❌ Redis connection failed")
        raise e

    print("\n✨ Startup complete\n")

    

    # after few time, we have to change it for prodcution ready
    # we will implement alembic migration later
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created/verified")
    except Exception as e:
        print(f"Error at table creation: {e}")


    yield

    print("\n🛑 Shutting down...\n")