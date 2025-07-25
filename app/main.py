from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Manage Stocks API",
    description="API for querying and registering stocks",
    version="0.1.0",
    contact={"name": "Luiz Campos", "email": "luizcampos331@gmail.com"},
    license_info={"name": "MIT"},
)


@app.get("/", response_class=JSONResponse)
async def root():
    return "API Account Transactions 0.1.0"
