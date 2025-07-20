import re

def parse_receipt_text(text: str):
    """Extract vendor, date, and amount from OCR text with flexible patterns"""
    
    # ✅ Date formats: 05 Aug 2024, 05/08/2024, 2024-08-05
    date_pattern = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+\w+\s+\d{4}|\d{4}-\d{2}-\d{2})\b"
    
    # ✅ Amount formats: ₹1234.56, Rs 1,234.56, $2,338.35
    amount_pattern = r"(?:Rs\.?|INR|₹|\$)\s?([\d,]+\.?\d{0,2})"

    # Extract date
    date_match = re.search(date_pattern, text)
    date = date_match.group(1) if date_match else None

    # Extract amount → pick the largest value (likely total)
    amounts = re.findall(amount_pattern, text)
    amount = None
    if amounts:
        # Remove commas, convert to float, pick max
        cleaned = [float(a.replace(",", "")) for a in amounts]
        amount = max(cleaned)

    # Vendor → still take the first line as a guess
    vendor = text.split("\n")[0].strip()

    return {
        "vendor": vendor,
        "date": date,
        "amount": amount
    }
