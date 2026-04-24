from fastapi import APIRouter, HTTPException, Request, Query
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import secrets

from src.services.oauth2_service import (
    get_auth_url,
    handle_callback,
    get_valid_token,
    token_store,
)

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(req: LoginRequest):
    # TODO: Implement actual auth
    return {"access_token": "***", "token_type": "bearer"}


@router.get("/me")
async def get_me():
    return {"id": "dev-user", "email": "dev@notehermes.com", "name": "Developer"}


# ==================== Microsoft OAuth2 (世纪互联) ====================

# Redirect URI for OAuth2 callback (must match Azure AD app registration)
# Format: http://<frontend_host>/api/v1/auth/microsoft/callback
REDIRECT_URI_PATH = "/api/v1/auth/microsoft/callback"


@router.get("/microsoft/login")
async def microsoft_login(request: Request):
    """Initiate Microsoft OAuth2 login (世纪互联)."""
    if not token_store.has_tokens():
        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)

        # Build redirect URI from request
        base_url = str(request.base_url).rstrip("/")
        redirect_uri = f"{base_url}{REDIRECT_URI_PATH}"

        auth_url = get_auth_url(redirect_uri, state)
        return RedirectResponse(url=auth_url)
    else:
        # Already logged in, go back
        referer = request.headers.get("referer", "/")
        return RedirectResponse(url=f"{referer}?oauth=connected")


@router.get("/microsoft/callback")
async def microsoft_callback(
    request: Request,
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    error_description: str = Query(None),
):
    """Handle Microsoft OAuth2 callback."""
    # Check for errors
    if error:
        return RedirectResponse(
            url=f"/inbox?oauth=error&error={error}&error_description={error_description}"
        )

    if not code:
        return RedirectResponse(
            url="/inbox?oauth=error&error=missing_code&error_description=缺少授权码"
        )

    try:
        # Exchange code for tokens
        base_url = str(request.base_url).rstrip("/")
        redirect_uri = f"{base_url}{REDIRECT_URI_PATH}"
        token_data = handle_callback(code, state or "", redirect_uri)

        # Redirect back to inbox with success
        return RedirectResponse(
            url=f"/inbox?oauth=success&email={token_data.email}"
        )
    except Exception as e:
        error_msg = str(e)
        return RedirectResponse(
            url=f"/inbox?oauth=error&error=callback_failed&error_description={error_msg}"
        )


@router.get("/microsoft/status")
async def microsoft_status():
    """Check if a Microsoft account is connected."""
    token_data = get_valid_token()
    if token_data:
        return {
            "connected": True,
            "email": token_data.email,
            "name": token_data.name,
            "provider": "china365_oauth2",
        }
    return {"connected": False}


@router.post("/microsoft/logout")
async def microsoft_logout():
    """Disconnect Microsoft account."""
    token_store.clear()
    return {"status": "disconnected"}
