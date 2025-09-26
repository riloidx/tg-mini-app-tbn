#!/usr/bin/env python3
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.db.base import Base


async def run_migrations():
    """Run database migrations manually"""
    engine = create_async_engine(settings.database_url)
    
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully")
            
        # Run alembic migrations
        import subprocess
        result = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully")
        else:
            print(f"❌ Migration failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_migrations())