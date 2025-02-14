from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import SupportItem, Base

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NDIS Pricing API")

# Dependency: Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ New Route to Get All Pricing Items
@app.get("/pricing", summary="Get All Support Items")
def get_all_pricing(db: Session = Depends(get_db)):
    items = db.query(SupportItem).all()
    return [item.as_dict() for item in items]

# ✅ Existing Route to Get a Specific Item by Support Item Number
@app.get("/pricing/{support_item_number}", summary="Get Pricing")
def get_pricing(
    support_item_number: str,
    state: str = Query(
        None,
        description="Optional. Specify a state to get its price (ACT, NSW, NT, QLD, SA, TAS, VIC, WA, Remote, Very Remote)."
    ),
    db: Session = Depends(get_db)
):
    item = db.query(SupportItem).filter(SupportItem.support_item_number == support_item_number).first()
    if not item:
        raise HTTPException(status_code=404, detail="Support item not found")

    # If state is provided, return only the price for that state
    if state:
        state_norm = state.lower().replace(" ", "_")
        valid_states = {"act", "nsw", "nt", "qld", "sa", "tas", "vic", "wa", "remote", "very_remote"}

        if state_norm not in valid_states:
            raise HTTPException(status_code=400, detail="Invalid state specified")

        price = getattr(item, state_norm, None)
        return {
            "support_item_number": support_item_number,
            "state": state,
            "price": float(price) if price is not None else None
        }

    return item.as_dict()
