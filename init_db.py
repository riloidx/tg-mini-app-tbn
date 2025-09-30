import asyncio
import asyncpg
import time
from app.core.config import settings

async def wait_for_db(max_retries=30, delay=2):
    """Ожидание готовности базы данных"""
    for attempt in range(max_retries):
        try:
            conn = await asyncpg.connect(settings.database_url.replace('+asyncpg', ''))
            await conn.close()
            print(f"✅ База данных готова к работе (попытка {attempt + 1})")
            return True
        except Exception as e:
            print(f"⏳ Ожидание базы данных... (попытка {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                print("❌ Не удалось подключиться к базе данных после всех попыток")
                return False
    return False

async def init_database():
    try:
        # Ожидание готовности базы данных
        if not await wait_for_db():
            raise Exception("База данных недоступна")
        
        # Подключение к PostgreSQL
        conn = await asyncpg.connect(settings.database_url.replace('+asyncpg', ''))
        
        # Проверка, инициализирована ли уже база
        try:
            result = await conn.fetchval("SELECT COUNT(*) FROM questions")
            if result > 0:
                print("✅ База данных уже инициализирована, пропускаем...")
                await conn.close()
                return
        except:
            # Таблица не существует, продолжаем инициализацию
            pass
        
        # Чтение SQL скрипта
        with open('init_database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Выполнение скрипта
        await conn.execute(sql_script)
        
        print("✅ База данных успешно инициализирована!")
        print("✅ Все таблицы созданы")
        print("✅ 51 вопрос загружен в базу данных")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())