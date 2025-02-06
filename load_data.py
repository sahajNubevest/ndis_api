# load_data.py
import pandas as pd
from app.database import SessionLocal, engine
from app.models import SupportItem, Base

def parse_price(value):
    """
    Convert a price value from the Excel file to a float.
    It removes any '$' or commas and converts the result.
    """
    if pd.isna(value):
        return None
    try:
        # Convert value to string, remove $ and commas, then convert to float.
        return float(str(value).replace("$", "").replace(",", "").strip())
    except Exception as e:
        print(f"Error parsing price value {value}: {e}")
        return None

def load_excel_data(file_path: str):
    # Read the "Current Support Items" sheet
    df = pd.read_excel(file_path, sheet_name="Current Support Items")
    
    session = SessionLocal()
    for _, row in df.iterrows():
        item = SupportItem(
            support_item_number = row.get("Support Item Number"),
            support_item_name = row.get("Support Item Name"),
            registration_group_number = row.get("Registration Group Number"),
            registration_group_name = row.get("Registration Group Name"),
            support_category_number = row.get("Support Category Number"),
            support_category_number_pace = row.get("Support Category Number (PACE)"),
            support_category_name = row.get("Support Category Name"),
            support_category_name_pace = row.get("Support Category Name (PACE)"),
            unit = row.get("Unit"),
            quote = row.get("Quote"),
            start_date = str(row.get("Start date")),  # Optionally, parse to a proper date
            end_date = str(row.get("End Date")),
            act = parse_price(row.get("ACT")),
            nsw = parse_price(row.get("NSW")),
            nt = parse_price(row.get("NT")),
            qld = parse_price(row.get("QLD")),
            sa = parse_price(row.get("SA")),
            tas = parse_price(row.get("TAS")),
            vic = parse_price(row.get("VIC")),
            wa = parse_price(row.get("WA")),
            remote = parse_price(row.get("Remote")),
            very_remote = parse_price(row.get("Very Remote")),
            non_face_to_face_support_provision = row.get("Non-Face-to-Face Support Provision"),
            provider_travel = row.get("Provider Travel"),
            short_notice_cancellations = row.get("Short Notice Cancellations."),
            ndia_requested_reports = row.get("NDIA Requested Reports"),
            irregular_sil_supports = row.get("Irregular SIL Supports"),
            type = row.get("Type")
        )
        session.add(item)
    session.commit()
    session.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    # Create tables if they don't already exist
    Base.metadata.create_all(bind=engine)
    # Replace with your actual Excel file path
    excel_file_path = "NDIS Support Catalogue.xlsx"
    load_excel_data(excel_file_path)
