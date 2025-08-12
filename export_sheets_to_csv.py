# scripts/export_sheets_to_csv.py
import os, json, csv, gspread
from google.oauth2.service_account import Credentials

SHEET_ID = os.environ["SHEET_ID"]
SVC_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Ожидаемые листы
SHEETS = [
    ("portfolio", "portfolio.csv"),
    ("operations", "operations.csv"),
]

def main():
    creds = Credentials.from_service_account_info(json.loads(SVC_JSON), scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)

    for ws_title, out_csv in SHEETS:
        ws = sh.worksheet(ws_title)  # бросит WorksheetNotFound, если нет такого листа
        rows = ws.get_all_values()   # список списков (строки)
        # Пишем как есть, без преобразований — ты просил «всю таблицу»
        with open(out_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"Wrote {out_csv}: {len(rows)} rows")

if __name__ == "__main__":
    main()
