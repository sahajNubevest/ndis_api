# app/main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import SupportItem, Base

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NDIS Pricing API")

# Dependency: provide a SQLAlchemy session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pricing/{support_item_number}")
def get_pricing(
    support_item_number: str,
    state: str = Query(
        None,
        description=(
            "Optional. Specify a state or region to get its price. "
            "Valid values are: ACT, NSW, NT, QLD, SA, TAS, VIC, WA, "
            "Remote, Very Remote."
        )
    ),
    db: Session = Depends(get_db)
):
    # Retrieve the full support item from the database
    item = db.query(SupportItem).filter(SupportItem.support_item_number == support_item_number).first()
    if not item:
        raise HTTPException(status_code=404, detail="Support item not found")
    
    # If a state parameter is provided, return just that price
    if state:
        # Normalize the state input to match the column names in the model.
        # In our model, we use lower-case column names without spaces (e.g., "act", "nsw", "very_remote").
        state_norm = state.lower().replace(" ", "_")
        valid_states = {"act", "nsw", "nt", "qld", "sa", "tas", "vic", "wa", "remote", "very_remote"}
        if state_norm not in valid_states:
            raise HTTPException(status_code=400, detail="Invalid state or location specified")
        
        # Use Python's getattr to fetch the price attribute dynamically.
        price = getattr(item, state_norm)
        return {
            "price": float(price) if price is not None else None
        }
    
    # Otherwise, return the full item details.
    return item.as_dict()
