from datetime import datetime

def convert_date(user_date):
    # Support multiple formats: User input and Automation timestamp
    formats = ["%d/%m/%Y", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
    
    for fmt in formats:
        try:
            date_obj = datetime.strptime(user_date, fmt)
            folder_date = date_obj.strftime("%Y-%m-%d")
            return date_obj, folder_date
        except (ValueError, TypeError):
            continue
            
    print(f"Error: Invalid date format! Received: {user_date}")
    return None, None