from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.db_connection import get_db
from db.user_db import UserInDB
from db.transaction_db import TransactionInDB
from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut

router = APIRouter()

@router.put("/user/transaction/", response_model=TransactionOut)
async def make_transaction(transaction_in: TransactionIn, session: Session = Depends(get_db)):
    user_in_db = session.query(UserInDB).get(transaction_in.username)

    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El usuario no existe")

    if user_in_db.balance < transaction_in.value:
        raise HTTPException(status_code=400,
                            detail="No se tienen los fondos suficientes")

    user_in_db.balance = user_in_db.balance - transaction_in.value

    # Vamos a actualizar en la db
    session.commit()

    # Actualiza la sesión que tenemos creada
    session.refresh(user_in_db)

    transaction_in_db = TransactionInDB(**transaction_in.dict(), actual_balance = user_in_db.balance)

    # Como queremos agregar un nuevo valor a la bd,
    # debemos insertarle el elemento a nuestra sesión
    session.add(transaction_in_db)
    session.commit()
    session.refresh(transaction_in_db)

    return  transaction_in_db
