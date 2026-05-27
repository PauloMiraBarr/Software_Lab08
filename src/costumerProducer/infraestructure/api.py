from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.costumerProducer.application.register_dinner import RegisterDinnerUseCase
from src.costumerProducer.domain.dinner_transaction import DinnerTransaction
from src.costumerProducer.infraestructure.rabbitmq_adapter import RabbitMQAdapter

app = FastAPI(title="Restaurant Reward Producer API")


class TransactionRequest(BaseModel):
    amount: float
    card_number: str
    restaurant_code: str


class TransactionResponse(BaseModel):
    status: str
    message: str
    amount: float
    card_number: str
    restaurant_code: str
    date_time: str


def get_use_case() -> RegisterDinnerUseCase:
    adapter = RabbitMQAdapter()
    return RegisterDinnerUseCase(adapter)


@app.post("/transactions", response_model=TransactionResponse, responses={
    400: {"description": "Monto inválido"},
})
def register_transaction(req: TransactionRequest):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

    now = datetime.now()
    transaction = DinnerTransaction(
        amount=req.amount,
        card_number=req.card_number,
        restaurant_code=req.restaurant_code,
        date_time=now,
    )

    use_case = get_use_case()
    use_case.execute(transaction)

    return TransactionResponse(
        status="ok",
        message="Cena registrada exitosamente",
        amount=transaction.amount,
        card_number=transaction.card_number,
        restaurant_code=transaction.restaurant_code,
        date_time=transaction.date_time.isoformat(),
    )


@app.get("/health")
def health():
    return {"status": "ok"}
