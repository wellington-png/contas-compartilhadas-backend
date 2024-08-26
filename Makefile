prebuild:
	cp example.env .env
	cp example.db.env .db.env

dump_all:
	sudo docker compose exec contas_backend python manage.py dumpdata accounts core customer office > fixtures/data.json

migrate:
	sudo docker compose exec contas_backend python manage.py migrate
zero_migrate:
	sudo docker compose exec contas_backend python manage.py migrate accounts zero
	sudo docker compose exec contas_backend python manage.py migrate core zero
	sudo docker compose exec contas_backend python manage.py migrate customer zero
	sudo docker compose exec contas_backend python manage.py migrate finance zero
	sudo docker compose exec contas_backend python manage.py migrate kanban zero
	sudo docker compose exec contas_backend python manage.py migrate office zero
	sudo docker compose exec contas_backend python manage.py migrate payment zero
	sudo docker compose exec contas_backend python manage.py migrate schedule zero
	sudo docker compose exec contas_backend python manage.py migrate subscription zero

makemigrations:
	sudo docker compose exec contas_backend python manage.py makemigrations

reset_migrations:
	sudo docker compose exec contas_backend find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "*/venv/*" -delete
	sudo docker compose exec contas_backend python manage.py makemigrations
	

delete_pycache:
	find . -path "*/__pycache__" | xargs rm -rf

load_data:
	sudo docker compose exec contas_backend python manage.py loaddata fixtures/*.json

load_user_data:
	sudo docker compose exec contas_backend  python manage.py loaddata users.json

test:
	sudo docker compose exec contas_backend python manage.py test

populate_db:
	sudo docker compose exec contas_backend python manage.py populate_db

lint:
	black .
	flake8 . --extend-exclude=migrations,venv --max-line-length 120

runserver:
	sudo docker compose up

build:
	sudo docker compose up --build