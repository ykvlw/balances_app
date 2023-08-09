from fastapi import HTTPException, Depends, APIRouter
from datetime import datetime
from pymongo.collection import Collection
from db.db import get_db_collection
from services.balances import web3, get_balances
from shema.balances import InputData, BalanceResponse

router = APIRouter(
    prefix="/v1",
    tags=["balances"],
    responses={404: {"description": "Not found"}},
)


@router.post("/get_balance/")
async def get_balance(input_data: InputData, db_collection: Collection = Depends(get_db_collection)):
    wallet_address = input_data.wallet_address

    if not web3.is_address(wallet_address):
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    token_balance, usd_balance = get_balances(wallet_address)

    balance_entry = {
        "wallet_address": wallet_address,
        "last_update": datetime.utcnow(),
        "token_balance": token_balance,
        "usd_balance": usd_balance
    }
    db_collection.insert_one(balance_entry)

    return BalanceResponse(**balance_entry)


@router.get("/get_history/")
async def get_history(wallet_address: str, db_collection: Collection = Depends(get_db_collection)):
    history_entries = db_collection.find({"wallet_address": wallet_address})
    history = [
        {
            "timestamp": entry["last_update"],
            "token_balance": entry["token_balance"],
            "usd_balance": entry["usd_balance"]
        }
        for entry in history_entries
    ]
    return history
