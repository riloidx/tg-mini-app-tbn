@echo off
echo Запуск сервисов...

REM Остановка и удаление старых контейнеров
echo Остановка старых контейнеров...
docker-compose down

REM Создание и запуск сервисов
echo Создание и запуск сервисов...
docker-compose up --build -d

REM Проверка статуса
echo Проверка статуса сервисов...
timeout /t 5 /nobreak > nul
docker-compose ps

echo.
echo Сервисы запущены!
echo FastAPI: http://localhost:8000
echo pgAdmin4: http://localhost:5050 (admin@example.com / admin)
echo.
echo Для просмотра логов используйте: docker-compose logs -f [service_name]
echo Для остановки используйте: docker-compose down