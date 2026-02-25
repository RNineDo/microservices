import uvicorn
from fastapi import FastAPI
from services.gateway_service.infrastructure.rest.routers import api_router

app = FastAPI(title="Gateway Microservices TP")
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("services.gateway_service.main:app", host="0.0.0.0", port=8000, reload=False)
