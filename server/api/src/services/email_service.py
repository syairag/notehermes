import imaplib
import smtplib
import email
from email.header import decode_header
from typing import Dict, Any, List, Optional
from src.config import settings

# 21Vianet (Century Internet) specific endpoints for M365 China
M365_CN_IMAP_HOST = "partner.outlook.cn"
M365_CN_SMTP_HOST = "partner.outlook.cn"
M365_GRAPH_BASE = "https://microsoftgraph.chinacloudapi.cn/v1.0"

# International M365 endpoints
M365_GLOBAL_IMAP_HOST = "outlook.office365.com"
M365_GLOBAL_SMTP_HOST = "smtp.office365.com"
M365_GLOBAL_GRAPH_BASE = "https://graph.microsoft.com/v1.0"


class ExchangeService:
    """Exchange Web Services (EWS) adapter — for on-premises Exchange and Exchange Online."""

    def __init__(self):
        self._account = None

    def connect(
        self,
        server: str,
        email: str,
        password: str,
        use_ssl: bool = True,
        verify_ssl: bool = True,
        auth_type: str = "ntlm",  # ntlm / basic / digest
    ):
        """Connect to an Exchange server via EWS."""
        try:
            from exchangelib import (
                Credentials,
                Configuration,
                Account,
                DELEGATE,
                Build,
                Version,
            )
            from exchangelib.protocol import BaseProtocol
            import urllib3

            # Disable SSL verification warnings if needed
            if not verify_ssl:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            credentials = Credentials(email, password)

            # Auto-discover if server is not provided
            if server:
                # Build a version hint to speed up connection
                version = Version(build=Build(15, 0, 0, 0))
                config = Configuration(
                    server=server,
                    credentials=credentials,
                    auth_type=auth_type,
                    verify_ssl=verify_ssl,
                )
                self._account = Account(
                    primary_smtp_address=email,
                    config=config,
                    autodiscover=False,
                    access_type=DELEGATE,
                )
            else:
                # Use autodiscover
                self._account = Account(
                    primary_smtp_address=email,
                    credentials=credentials,
                    autodiscover=True,
                    access_type=DELEGATE,
                    verify_ssl=verify_ssl,
                )

            print(f"✅ Exchange connected: {email} via {server or 'autodiscover'}")
            return True

        except ImportError:
            raise RuntimeError(
                "exchangelib is not installed. Run: pip install exchangelib"
            )
        except Exception as e:
            print(f"❌ Exchange Connection Failed: {e}")
            raise

    def fetch_emails(self, folder: str = "inbox", limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch recent emails from a folder."""
        if not self._account:
            raise RuntimeError("Not connected to Exchange. Call connect() first.")

        folder_obj = getattr(self._account, folder, self._account.inbox)
        emails_list = []

        # Fetch latest emails
        for item in folder_obj.all().order_by("-datetime_received")[:limit]:
            emails_list.append({
                "id": str(item.id),
                "subject": item.subject or "(无主题)",
                "sender": item.sender.email_address if item.sender else "未知",
                "sender_name": item.sender.name if item.sender else "",
                "date": str(item.datetime_received) if item.datetime_received else "",
                "body_preview": item.text_body[:500] if hasattr(item, "text_body") and item.text_body else "",
                "has_attachments": item.has_attachments,
                "is_read": item.is_read,
            })

        return emails_list

    def mark_as_read(self, item_id: str) -> bool:
        """Mark an email as read."""
        if not self._account:
            return False
        try:
            item = self._account.inbox.get(id=item_id)
            item.is_read = True
            item.save()
            return True
        except Exception as e:
            print(f"Mark as read failed: {e}")
            return False

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> bool:
        """Send an email via Exchange."""
        if not self._account:
            return False
        try:
            from exchangelib import Message, Mailbox
            msg = Message(
                account=self._account,
                subject=subject,
                body=body,
                to_recipients=[Mailbox(email_address=to)],
                cc_recipients=[Mailbox(email_address=cc)] if cc else None,
                bcc_recipients=[Mailbox(email_address=bcc)] if bcc else None,
            )
            msg.send()
            return True
        except Exception as e:
            print(f"Send email failed: {e}")
            return False


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

        # Exchange adapter
        self.exchange = ExchangeService()

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
