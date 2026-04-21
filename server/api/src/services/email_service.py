import imaplib
import smtplib
import email
from email.header import decode_header
from typing import Dict, Any, List
from src.config import settings

# 21Vianet (Century Internet) specific endpoints for M365 China
M365_CN_IMAP_HOST = "partner.outlook.cn"
M365_CN_SMTP_HOST = "partner.outlook.cn"
M365_GRAPH_BASE = "https://microsoftgraph.chinacloudapi.cn/v1.0"

# International M365 endpoints
M365_GLOBAL_IMAP_HOST = "outlook.office365.com"
M365_GLOBAL_SMTP_HOST = "smtp.office365.com"
M365_GLOBAL_GRAPH_BASE = "https://graph.microsoft.com/v1.0"

class EmailService:
    def __init__(self):
        # Determine if we are using the China version (Century Internet)
        self.is_china = getattr(settings, 'USE_CHINA_M365', False)
        
        if self.is_china:
            self.imap_host = M365_CN_IMAP_HOST
            self.graph_base = M365_GRAPH_BASE
            self.auth_endpoint = "https://login.partner.microsoftonline.cn/"
        else:
            self.imap_host = M365_GLOBAL_IMAP_HOST
            self.graph_base = M365_GLOBAL_GRAPH_BASE
            self.auth_endpoint = "https://login.microsoftonline.com/"

    def connect_imap(self, username: str, password: str) -> imaplib.IMAP4_SSL:
        """Connects to IMAP server using configured endpoint."""
        try:
            print(f"Connecting to IMAP: {self.imap_host} ...")
            # In a real scenario, port is usually 993 for SSL
            mail = imaplib.IMAP4_SSL(self.imap_host, 993)
            mail.login(username, password)
            return mail
        except Exception as e:
            print(f"IMAP Connection Failed: {e}")
            raise

    def fetch_emails(self, username: str, password: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetches recent emails from the inbox."""
        mail = self.connect_imap(username, password)
        mail.select("inbox")
        
        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()
        
        emails_list = []
        # Fetch the last 'limit' emails
        for i in range(len(mail_ids) - 1, max(len(mail_ids) - 1 - limit, -1), -1):
            status, msg_data = mail.fetch(mail_ids[i], "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    emails_list.append({
                        "subject": self.decode_mime_header(msg["Subject"]),
                        "from": self.decode_mime_header(msg["From"]),
                        "date": msg["Date"]
                    })
        return emails_list

    @staticmethod
    def decode_mime_header(header_value: str) -> str:
        if not header_value:
            return ""
        decoded_parts = decode_header(header_value)
        return "".join([part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part for part, encoding in decoded_parts])
