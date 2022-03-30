PYTHON_EXE?=python3
MANAGE=.venv/bin/python manage.py
ACTIVATE?=. .venv/bin/activate;
GET_SECRET_KEY=`base64 /dev/urandom | head -c50`
ENV_FILE=.env

# Default Django Port
PORT = 8000

virtualenv:
	@echo "-> Making Virtual Environment"
	@${PYTHON_EXE} -m venv .venv

genkey: virtualenv
	@echo "-> Generating Secret key"
	@if test -f ${ENV_FILE}; then echo ".env file exists already"; true; else \
	mkdir -p $(shell dirname ${ENV_FILE}) && touch ${ENV_FILE}; \
	echo SECRET_KEY=\"${GET_SECRET_KEY}\" > ${ENV_FILE}; \
	cat etc/env.txt >> ${ENV_FILE}; fi

dev: genkey
	@echo "-> Installing Dependencies"
	@${ACTIVATE} pip install -r etc/dev.txt

base: genkey
	@echo "-> Installing Dependencies"
	@${ACTIVATE} pip install -r etc/base.txt

install: genkey
	@echo "-> Installing Dependencies"
	@${ACTIVATE} pip install -r requirements.txt

migrate:
	@echo "-> Apply database migrations"
	${MANAGE} makemigrations
	${MANAGE} migrate

run:
	${MANAGE} runserver ${PORT}


flush:
	@echo "-> Flushing Database"
	${MANAGE} flush

test:
	@${MANAGE} test

celery:
	@echo "-> Starting Celery"
	${ACTIVATE} celery -A backend.celery worker -l info

superuser:
	@echo "-> Creating superuser"
	${MANAGE} createsuperuser