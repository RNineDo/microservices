build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down && docker compose up -d --build

logs:
	docker compose logs -f

logs-gateway:
	docker compose logs -f gateway_service

logs-product:
	docker compose logs -f product_service

logs-customer:
	docker compose logs -f customer_service

logs-inventory:
	docker compose logs -f inventory_service

logs-pricing:
	docker compose logs -f pricing_service

logs-order:
	docker compose logs -f order_service

ps:
	docker compose ps

clean:
	docker compose down -v --rmi local
