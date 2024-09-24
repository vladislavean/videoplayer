.PHONY: server
server:
	uvicorn app.main:app --host 10.8.0.4 --port 5000 --reload

.PHONY: local
local:
	uvicorn app.main:app --host 127.0.0.1 --port 8081 --reload