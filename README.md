# Pseudocoders Backend

## Запустить всё вместе

```sh
docker-compose up --build
```

Можно открывать
* Backend: http://localhost:1337
* Flower Dashboard: http://localhost:5555

Запустить простую таску:

```sh
curl \
    --data '{"type": 0}' \
    --header 'Content-Type: application/json' \
    http://localhost:1337/tasks/
```

Проверить её статус:

```sh
curl http://localhost:1337/tasks/<TASK_ID>/
```

## Запустить по отдельности

1. Установить [Redis](https://redis.io/)
2. Установить зависимости

    ```sh
    cd project && pipenv install
    ```

3. Запустить API

    ```sh
    cd project && python project/manage.py runserver 0.0.0.0:8000
    ```

4. Запустить Celery

    ```sh
    cd project && celery worker --app=core --loglevel=info --logfile=logs/celery.log
    ```
