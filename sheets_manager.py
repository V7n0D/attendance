import datetime
import calendar
from .sheets_service import get_client
from googleapiclient.discovery import build
from gspread_formatting import CellFormat, TextFormat, format_cell_range, Color


# Set your personal email
YOUR_EMAIL = "vinodkinpbl@gmail.com"

def get_current_month_sheet(client, creds):

    """
    Returns the worksheet for the current month.
    Creates the sheet if it doesn't exist, inserts headers,
    pre-fills the month with 'Absent', applies formatting.
    """

    now = datetime.datetime.now()
    sheet_title = now.strftime("%B %Y")

    # Try to open existing monthly sheet or create a new one
    try:

        sheet = client.open(sheet_title)
        print(f"✅ Sheet '{sheet_title}' opened")

    except:
        
        sheet = client.create(sheet_title)
        print(f"📄 Created new sheet: {sheet_title}")

        # Share the new sheet with your Gmail
        drive_service = build('drive', 'v3', credentials=creds)
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': YOUR_EMAIL,
        }
        drive_service.permissions().create(
            fileId=sheet.id,
            body=permission,
            sendNotificationEmail=True
        ).execute()

    worksheet = sheet.sheet1

    
    # Ensure headers are correct
    expected_headers = ['Date', 'Day', 'Status', 'Time In', 'Time Out']
    current_headers = worksheet.row_values(1)
    if current_headers != expected_headers:
        worksheet.insert_row(expected_headers, 1)
        print("🛠️ Headers inserted")

        # Apply bold and center alignment to headers
        header_format = CellFormat(
            textFormat=TextFormat(bold=True),
            horizontalAlignment="CENTER"
        )
        format_cell_range(worksheet, "A1:E1", header_format)

    # Pre-fill entire month with "Absent" if not already filled
    records = worksheet.get_all_records()
    if not records:
        year, month = now.year, now.month
        num_days = calendar.monthrange(year, month)[1]
        rows = []
        for day in range(1, num_days + 1):
            date_obj = datetime.date(year, month, day)
            date_str = date_obj.strftime("%d-%m-%Y")
            day_name = date_obj.strftime("%A")
            rows.append([date_str, day_name, 'A', '', ''])
        worksheet.insert_rows(rows, row=2)
        print(f"📅 Pre-filled {len(rows)} days with Absent")
        
        # Apply center alignment to data rows
        data_format = CellFormat(horizontalAlignment="CENTER")
        format_cell_range(worksheet, f"A2:E{num_days + 1}", data_format)
    
    return worksheet


def mark_attendance(action):

    """
    Marks attendance based on action: 'clock_in' or 'clock_out'.
    Updates time and status, and applies conditional formatting.
    """
     
    print("✅ mark_attendance() called with action:", action)

    client, creds = get_client()
    worksheet = get_current_month_sheet(client, creds)

    now = datetime.datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%I:%M %p")

    # Find today's row in the sheet
    records = worksheet.get_all_records()
    row_index = None
    for i, row in enumerate(records, start=2):  # row 1 is header
        if row.get('Date') == date_str:
            row_index = i
            break
    

    
    # Update sheet depending on the action
    if action == "clock_in" and row_index:
        worksheet.update_cell(row_index, 3, 'P')       # Status
        worksheet.update_cell(row_index, 4, time_str)  # Time In
    elif action == "clock_out" and row_index:
        worksheet.update_cell(row_index, 5, time_str)  # Time Out
    else:
        print("⚠️ Row not found or invalid action")

        # Apply conditional formatting to Status column (P = green, A = red)
    try:
    
        present_format = CellFormat(backgroundColor=Color(0.8, 1, 0.8))  # Green
        absent_format = CellFormat(backgroundColor=Color(1, 0.8, 0.8))   # Red

        for i, row in enumerate(records, start=2):
            status = row.get('Status', '')
            if status == 'P':
                format_cell_range(worksheet, f"C{i}", present_format)
            elif status == 'A':
                format_cell_range(worksheet, f"C{i}", absent_format)

    except ImportError:
        print("Optional: Install gspread-formatting to enable coloring")
