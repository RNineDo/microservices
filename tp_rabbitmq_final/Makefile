build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v --rmi local

logs:
	docker compose logs -f

test:
	docker compose run --rm gateway_service python -m pytest tests/ -v
