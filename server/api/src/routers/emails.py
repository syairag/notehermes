from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from src.models.email import EmailResponse, EmailCreate
from src.services.email_service import ExchangeService

router = APIRouter()

# Exchange config cache (in production, store in DB)
_exchange_config: dict = {}


class ExchangeSyncRequest(BaseModel):
    server: Optional[str] = None  # e.g. mail.company.com / autodiscover if empty
    email: str
    password: str
    auth_type: Optional[str] = "ntlm"  # ntlm / basic / digest
    limit: Optional[int] = 20
    provider: Optional[str] = "exchange"  # exchange, china365, outlook


class IMAPConfigRequest(BaseModel):
    provider: str  # gmail, qq, netease, imap
    email: str
    password: Optional[str] = None
    imap_host: Optional[str] = None
    imap_port: Optional[int] = None
    # OAuth2 fields
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


@router.get("/", response_model=List[EmailResponse])
async def list_emails(skip: int = 0, limit: int = 20):
    # TODO: Fetch from DB
    return []


@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(email_id: str):
    raise HTTPException(status_code=404, detail="Email not found")


@router.post("/sync")
async def sync_emails():
    """Sync emails via EWS (Exchange Web Services) or Graph API (OAuth2)."""
    if not _exchange_config:
        # Check for OAuth2 token
        from src.services.oauth2_service import get_valid_token, GraphAPIService
        token_data = get_valid_token()
        if token_data:
            try:
                graph = GraphAPIService(token_data.access_token, is_china=True)
                emails = graph.fetch_emails(limit=20)
                return {
                    "status": "success",
                    "provider": "china365_oauth2",
                    "synced": len(emails),
                    "emails": emails,
                }
            except Exception as e:
                return {
                    "status": "error",
                    "synced": 0,
                    "message": f"Graph API 同步失败: {str(e)}",
                }
        return {
            "status": "no_config",
            "synced": 0,
            "message": "请先在邮箱设置中配置您的邮箱账户",
        }

    provider = _exchange_config.get("provider")

    if provider in ("exchange", "china365", "outlook"):
        try:
            ex = ExchangeService()

            # Determine EWS endpoint based on provider
            if provider == "china365":
                server = "https://partner.outlook.cn/EWS/Exchange.asmx"
            elif provider == "outlook":
                server = "https://outlook.office365.com/EWS/Exchange.asmx"
            else:
                server = _exchange_config.get("server", "")

            auth_type = _exchange_config.get("auth_type", "ntlm")

            ex.connect(
                server=server,
                email=_exchange_config["email"],
                password=_exchange_config["password"],
                auth_type=auth_type,
            )
            emails = ex.fetch_emails(limit=_exchange_config.get("limit", 20))
            return {
                "status": "success",
                "provider": provider,
                "synced": len(emails),
                "emails": emails,
            }
        except Exception as e:
            return {
                "status": "error",
                "synced": 0,
                "message": f"EWS 同步失败: {str(e)}",
            }
    else:
        return {
            "status": "not_implemented",
            "synced": 0,
            "message": f"{provider} 功能开发中",
        }


@router.post("/configure/exchange")
async def configure_exchange(config: ExchangeSyncRequest):
    """Save Exchange server configuration for subsequent syncs."""
    _exchange_config.update({
        "provider": config.provider or "exchange",
        "server": config.server,
        "email": config.email,
        "password": config.password,
        "auth_type": config.auth_type,
        "limit": config.limit,
    })
    return {"status": "configured", "email": config.email}


@router.post("/configure/imap")
async def configure_imap(config: IMAPConfigRequest):
    """Save IMAP configuration for subsequent syncs."""
    _exchange_config.update({
        "provider": config.provider,
        "email": config.email,
        "password": config.password,
        "imap_host": config.imap_host,
        "imap_port": config.imap_port,
    })
    return {"status": "configured", "email": config.email, "provider": config.provider}


@router.post("/summarize/{email_id}")
async def summarize_email(email_id: str):
    return {"summary": "AI summary will appear here"}


@router.post("/extract-tasks/{email_id}")
async def extract_tasks(email_id: str):
    return {"tasks_extracted": []}
