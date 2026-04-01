from datetime import datetime
from query_data import get_daily_volumes
from detect_issues import detect_issues
from send_email import send_email

def main():
    print(f"Starting volume check — {datetime.today().strftime('%d %b %Y %H:%M')}")
    
    print("Pulling data from database...")
    df = get_daily_volumes()
    print(f"Retrieved {len(df)} clients")
    
    print("Checking for issues...")
    flagged = detect_issues(df)
    zero_count = len(flagged["zero"])
    low_count = len(flagged["low"])
    print(f"Zero volume: {zero_count} client(s)")
    print(f"Low volume: {low_count} client(s)")
    
    print("Sending email...")
    send_email(flagged)
    
    print("Done.")

main()