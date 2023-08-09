from typing import Optional, Union
from eth_typing import Address, ChecksumAddress
from pydantic import BaseModel
from datetime import datetime


class InputData(BaseModel):
    wallet_address: Optional[Union[Address, ChecksumAddress]]


class BalanceResponse(BaseModel):
    wallet_address: str
    last_update: datetime
    token_balance: float
    usd_balance: float
