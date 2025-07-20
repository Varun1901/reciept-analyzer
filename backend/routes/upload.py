from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.utils.validators import validate_file_type
from backend.utils.ocr_parser import extract_text_from_image
from backend.utils.text_parser import parse_receipt_text
from backend.models.database import SessionLocal, Receipt
import shutil, os

router = APIRouter(prefix="/upload", tags=["Upload"])
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if not validate_file_type(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format! Allowed: jpg, png, pdf, txt")
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR + Parsing
    text = extract_text_from_image(file_path)
    parsed_data = parse_receipt_text(text)

    # ✅ Save to SQLite
    db = SessionLocal()
    new_receipt = Receipt(
        vendor=parsed_data["vendor"],
        date=parsed_data["date"],
        amount=parsed_data["amount"],
        filename=file.filename
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    db.close()

    return {
        "message": "Uploaded & saved successfully!",
        "filename": file.filename,
        "parsed_text": text,
        "extracted_fields": parsed_data
    }
