FROM python:3.11

COPY requirements/base.txt /app/requirements/base.txt
COPY requirements/production.txt /app/requirements/production.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements/production.txt

COPY ./app /app

# Создаем папку для сбора статических файлов внутри контейнера командой python3 -m app.manage collectstatic --noinput
# В противном случае Docker не создаст папку и файлы не будут скопированы
RUN mkdir /app/staticfiles

COPY ./docker /docker

# Данной командой мы разрешаем Docker выполнять все команды в папке docker с расширением .sh (bash-команды),
# которые в нашем случае используются для запуска Celery и Flower (в docker-compose.yml)
RUN chmod a+x docker/*.sh

# gunicorn
# ВАЖНО: не запускаем сервер, т.к. данный Dockerfile также используется и для сборки и запуска Celery и Flower
# Запускаем сервер в docker-compose
#CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000