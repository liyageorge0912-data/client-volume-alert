import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD

def build_html_table(flagged):
    zero = flagged["zero"]
    low = flagged["low"]
    
    rows = ""
    
    for _, row in zero.iterrows():
        rows += f"""
        <tr style="background-color: #ffcccc;">
            <td style="padding: 8px; border: 1px solid #ddd;">{row['client_name']}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{row['volume']}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">Zero volume</td>
        </tr>
        """
    
    for _, row in low.iterrows():
        rows += f"""
        <tr style="background-color: #fff3cc;">
            <td style="padding: 8px; border: 1px solid #ddd;">{row['client_name']}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{row['volume']}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">Low volume</td>
        </tr>
        """
    
    html = f"""
    <html>
    <body>
        <p>Hi team,</p>
        <p>The following clients have volume issues today 
        ({datetime.today().strftime('%d %b %Y')}):</p>
        <table style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #333; color: white;">
                <th style="padding: 8px; border: 1px solid #ddd;">Client</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Volume</th>
                <th style="padding: 8px; border: 1px solid #ddd;">Issue</th>
            </tr>
            {rows}
        </table>
        <p>Please investigate and resolve.</p>
        <p>This is an automated daily report.</p>
    </body>
    </html>
    """
    
    return html


def send_email(flagged):
    total = len(flagged["zero"]) + len(flagged["low"])
    
    if total == 0:
        print("No issues found. No email sent.")
        return
    
    html = build_html_table(flagged)
    
    msg = MIMEMultipart()
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = GMAIL_ADDRESS
    msg["Subject"] = f"[ALERT] {total} client(s) with volume issues — {datetime.today().strftime('%d %b %Y')}"
    
    msg.attach(MIMEText(html, "html"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
    
    print(f"Email sent — {total} client(s) flagged")


if __name__ == "__main__":
    from query_data import get_daily_volumes
    from detect_issues import detect_issues
    
    df = get_daily_volumes()
    flagged = detect_issues(df)
    send_email(flagged)