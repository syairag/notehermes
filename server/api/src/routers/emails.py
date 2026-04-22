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


@router.get("/", response_model=List[EmailResponse])
async def list_emails(skip: int = 0, limit: int = 20):
    # TODO: Fetch from DB
    return []


@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(email_id: str):
    raise HTTPException(status_code=404, detail="Email not found")


@router.post("/sync")
async def sync_emails():
    """Sync emails — requires Exchange config to be set first via /emails/configure/exchange"""
    if not _exchange_config:
        return {
            "status": "no_config",
            "synced": 0,
            "message": "请先配置邮箱（支持 Exchange / IMAP）",
        }

    provider = _exchange_config.get("provider")

    if provider == "exchange":
        try:
            ex = ExchangeService()
            ex.connect(
                server=_exchange_config.get("server", ""),
                email=_exchange_config["email"],
                password=_exchange_config["password"],
                auth_type=_exchange_config.get("auth_type", "ntlm"),
            )
            emails = ex.fetch_emails(limit=_exchange_config.get("limit", 20))
            return {
                "status": "success",
                "synced": len(emails),
                "emails": emails,
            }
        except Exception as e:
            return {
                "status": "error",
                "synced": 0,
                "message": f"Exchange 同步失败: {str(e)}",
            }
    else:
        return {
            "status": "not_implemented",
            "synced": 0,
            "message": f"{provider} 同步功能开发中",
        }


@router.post("/configure/exchange")
async def configure_exchange(config: ExchangeSyncRequest):
    """Save Exchange server configuration for subsequent syncs."""
    _exchange_config.update({
        "provider": "exchange",
        "server": config.server,
        "email": config.email,
        "password": config.password,
        "auth_type": config.auth_type,
        "limit": config.limit,
    })
    return {"status": "configured", "email": config.email}


@router.post("/summarize/{email_id}")
async def summarize_email(email_id: str):
    return {"summary": "AI summary will appear here"}


@router.post("/extract-tasks/{email_id}")
async def extract_tasks(email_id: str):
    return {"tasks_extracted": []}
