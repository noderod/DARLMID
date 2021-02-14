.PHONY: dev
dev:
	cd server && docker-compose up -d --build
	docker exec -d server_main_node_1 gunicorn traffic:expert_seas_web_app --bind main_node:8080 --worker-class aiohttp.GunicornWebWorker -w 5

.PHONY: teardown
teardown:
	cd server && docker-compose down

.PHONY: deploy
deploy:
	cd server && docker-compose up -d --build