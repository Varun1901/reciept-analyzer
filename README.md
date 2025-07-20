# 📊 Receipt Analyzer – Full Stack Mini App
A **full-stack mini-application** for uploading receipts and bills. It extracts structured data (vendor, date, amount) using **OCR + regex**, stores it in **SQLite**, and provides an interactive **dashboard** with insights like total spend, vendor distribution, and monthly trends.

## ✨ Features
✅ Upload receipts (JPG, PNG, PDF, TXT)  
✅ OCR text extraction using **Tesseract**  
✅ Parse **Vendor, Date, Amount** using regex  
✅ Store parsed data in **SQLite database**  
✅ Search, Sort, and View receipts via API  
✅ Interactive **Streamlit dashboard**  
✅ Edit OCR mistakes and update data  
✅ Export receipts as **CSV/JSON**  
✅ Visual insights → vendor distribution, spending trends

## 🏗️ Tech Stack
- **Backend:** FastAPI + SQLAlchemy (SQLite DB)
- **OCR:** pytesseract + Pillow
- **Frontend:** Streamlit + Plotly
- **Database:** SQLite (lightweight, ACID-compliant)

## 📂 Project Structure
```
receipt-analyzer/
├── backend/
│   ├── main.py               # FastAPI entry point
│   ├── models/
│   │   ├── database.py       # SQLite models
│   ├── routes/
│   │   ├── upload.py         # Upload + OCR + Save
│   │   ├── receipts.py       # Search, Sort, Summary APIs
│   ├── utils/
│       ├── ocr_parser.py     # OCR text extraction
│       ├── text_parser.py    # Regex parsing (vendor, date, amount)
│       ├── validators.py     # File type validation
│
├── frontend/
│   ├── app.py                # Streamlit dashboard
│
├── receipts.db               # SQLite database (auto-created)
├── uploaded_files/           # Uploaded receipt images
├── requirements.txt          # Dependencies
└── README.md
```

## ⚡ Setup & Installation
### 1️⃣ Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/receipt-analyzer.git
cd receipt-analyzer
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
# Activate
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux
```
### 3️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install fastapi uvicorn python-multipart pytesseract Pillow sqlalchemy pydantic streamlit requests pandas plotly
```
### 4️⃣ Install Tesseract OCR Engine
- **Windows:** [Download Tesseract OCR (UB Mannheim Build)](https://github.com/UB-Mannheim/tesseract/wiki)
- After installing, add `C:\Program Files\Tesseract-OCR\` to your PATH  
- Verify:
```bash
tesseract --version
```

## 🚀 Run the App
### ✅ Start Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
API will be available at 👉 **http://127.0.0.1:8000/docs**
### ✅ Start Frontend (Streamlit)
```bash
streamlit run frontend/app.py
```
Dashboard will open at 👉 **http://localhost:8501**

## 📊 How It Works
1️⃣ Upload a receipt (JPG, PNG, PDF, TXT)  
2️⃣ Backend extracts raw text using **Tesseract OCR**  
3️⃣ Regex parses **vendor, date, amount**  
4️⃣ Data is saved in **SQLite**  
5️⃣ Dashboard shows:  
   - All receipts in a table  
   - Total spend, average receipt, total receipts  
   - Vendor distribution (bar chart)  
   - Monthly spending trend (line chart)  
6️⃣ Edit OCR mistakes and update instantly  
7️⃣ Export all receipts as **CSV/JSON**

## ✅ APIs
- `POST /upload` → Upload & parse a receipt  
- `GET /receipts` → Get all saved receipts  
- `GET /receipts/search?vendor=Amazon` → Search by vendor  
- `GET /receipts/sort?field=amount&order=desc` → Sort receipts  
- `GET /receipts/summary` → Get total & average spend  
- `PUT /receipts/{id}` → Update a receipt


## 👨‍💻 Author
Developed as a **Python Intern Full Stack Assignment**  
Feel free to ⭐ the repo if you find it useful!
