from fastapi import APIRouter, Query
from backend.models.database import SessionLocal, Receipt
from sqlalchemy import func

router = APIRouter(prefix="/receipts", tags=["Receipts"])

# ✅ Get all receipts
@router.get("/")
def get_all_receipts():
    db = SessionLocal()
    receipts = db.query(Receipt).all()
    db.close()
    return receipts

# ✅ Search receipts by vendor keyword
@router.get("/search")
def search_receipts(vendor: str = Query(...)):
    db = SessionLocal()
    results = db.query(Receipt).filter(Receipt.vendor.ilike(f"%{vendor}%")).all()
    db.close()
    return results

# ✅ Sort receipts by a field
@router.get("/sort")
def sort_receipts(field: str = "amount", order: str = "desc"):
    db = SessionLocal()
    query = db.query(Receipt)

    # Map allowed fields
    sort_field = getattr(Receipt, field, None)
    if not sort_field:
        db.close()
        return {"error": "Invalid sort field. Use 'amount', 'date', or 'vendor'."}
    
    # Apply sorting order
    if order == "asc":
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())

    receipts = query.all()
    db.close()
    return receipts

# ✅ Summary stats: total, avg, count
@router.get("/summary")
def summary_receipts():
    db = SessionLocal()
    total_spent = db.query(func.sum(Receipt.amount)).scalar() or 0
    avg_spent = db.query(func.avg(Receipt.amount)).scalar() or 0
    receipt_count = db.query(func.count(Receipt.id)).scalar()
    db.close()
    return {
        "total_spent": total_spent,
        "average_spent": avg_spent,
        "total_receipts": receipt_count
    }
@router.put("/{receipt_id}")
def update_receipt(receipt_id: int, vendor: str, date: str, amount: float):
    db = SessionLocal()
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not receipt:
        db.close()
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    receipt.vendor = vendor
    receipt.date = date
    receipt.amount = amount
    
    db.commit()
    db.refresh(receipt)
    db.close()
    return {"message": "Receipt updated successfully", "receipt": receipt}