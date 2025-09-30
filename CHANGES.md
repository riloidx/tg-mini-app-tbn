# Изменения в проекте

## Что было удалено:
- ❌ Все упоминания Supabase из конфигурации
- ❌ Неиспользуемые переменные окружения (SUPABASE_URL, SUPABASE_KEY)

## Что было улучшено:
- ✅ Переименован volume с `supabase_db_data` на `postgres_data`
- ✅ Добавлен отдельный volume для pgAdmin4 (`pgadmin_data`)
- ✅ Улучшены зависимости между сервисами
- ✅ pgAdmin4 теперь ждет готовности базы данных
- ✅ Добавлен restart policy для pgAdmin4

## Текущая архитектура:
1. **PostgreSQL** - основная база данных
2. **init-db** - инициализация схемы и данных
3. **app** - FastAPI приложение
4. **bot** - Telegram бот
5. **pgAdmin4** - веб-интерфейс для просмотра БД

## Доступ к сервисам:
- FastAPI: http://localhost:8000
- pgAdmin4: http://localhost:5050
  - Email: admin@example.com
  - Password: admin

## Подключение к БД через pgAdmin4:
1. Откройте http://localhost:5050
2. Войдите с указанными выше данными
3. Добавьте новый сервер:
   - Name: Local PostgreSQL
   - Host: db
   - Port: 5432
   - Username: postgres
   - Password: postgres

## Команды для управления:
```bash
# Запуск всех сервисов
start.bat

# Остановка сервисов
stop.bat

# Резервная копия БД
backup_db.bat

# Восстановление БД
restore_db.bat backup_file.sql
```

Теперь проект использует только необходимые компоненты без лишних зависимостей от Supabase.