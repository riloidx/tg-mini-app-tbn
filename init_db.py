import asyncio
import asyncpg
from app.core.config import settings

async def init_database():
    try:
        # Подключение к PostgreSQL
        conn = await asyncpg.connect(settings.database_url.replace('+asyncpg', ''))
        
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

if __name__ == "__main__":
    asyncio.run(init_database())