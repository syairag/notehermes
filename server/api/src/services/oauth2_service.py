"""
Microsoft 365 OAuth2 authentication service (世纪互联版本).
"""
import os
import time
import logging
from typing import Optional, Dict
from dataclasses import dataclass, field
from requests_oauthlib import OAuth2Session

from src.config import settings

logger = logging.getLogger(__name__)

# Century Internet (21Vianet) Azure AD endpoints
CHINA_AUTH_BASE = "https://login.partner.microsoftonline.cn"
CHINA_GRAPH_BASE = "https://microsoftgraph.chinacloudapi.cn"

# OAuth2 endpoints for China
AUTHORIZE_URL = f"{CHINA_AUTH_BASE}/{{tenant}}/oauth2/v2.0/authorize"
TOKEN_URL = f"{CHINA_AUTH_BASE}/{{tenant}}/oauth2/v2.0/token"


@dataclass
class TokenData:
    access_token: str
    refresh_token: str
    expires_at: float
    email: str
    name: str
    user_id: str


class OAuth2TokenStore:
    """In-memory token store for development. Use DB in production."""
    def __init__(self):
        self._tokens: Dict[str, TokenData] = {}

    def save(self, email: str, token: TokenData):
        self._tokens[email.lower()] = token

    def get(self, email: str) -> Optional[TokenData]:
        return self._tokens.get(email.lower())

    def get_any(self) -> Optional[TokenData]:
        """Get any stored token (for single-user dev mode)."""
        return next(iter(self._tokens.values()), None)

    def remove(self, email: str):
        self._tokens.pop(email.lower(), None)

    def has_tokens(self) -> bool:
        return len(self._tokens) > 0

    def clear(self):
        self._tokens.clear()


# Global token store
token_store = OAuth2TokenStore()


def get_auth_url(redirect_uri: str, state: str) -> str:
    """Generate Microsoft login URL for user authorization."""
    tenant = settings.M365_TENANT_ID or "common"
    url = AUTHORIZE_URL.format(tenant=tenant)
    params = {
        "client_id": settings.M365_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "https://microsoftgraph.chinacloudapi.cn/Mail.Read https://microsoftgraph.chinacloudapi.cn/Mail.ReadWrite https://microsoftgraph.chinacloudapi.cn/User.Read offline_access",
        "state": state,
        "response_mode": "query",
    }
    # Build query string
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{url}?{query}"


def exchange_code(code: str, redirect_uri: str) -> dict:
    """Exchange authorization code for tokens."""
    tenant = settings.M365_TENANT_ID or "common"
    token_url = TOKEN_URL.format(tenant=tenant)

    client = OAuth2Session(
        client_id=settings.M365_CLIENT_ID,
        client_secret=settings.M365_CLIENT_SECRET,
        redirect_uri=redirect_uri,
    )
    token = client.fetch_token(
        token_url,
        code=code,
        include_client_id=True,
    )
    return token


def get_user_profile(access_token: str) -> dict:
    """Get user profile from Microsoft Graph (China)."""
    import httpx
    response = httpx.get(
        f"{CHINA_GRAPH_BASE}/v1.0/me",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    response.raise_for_status()
    return response.json()


def handle_callback(code: str, state: str, redirect_uri: str) -> TokenData:
    """Full OAuth2 callback handler: exchange code, get profile, store token."""
    # Exchange code for tokens
    token = exchange_code(code, redirect_uri)

    # Get user profile
    profile = get_user_profile(token["access_token"])

    # Create token data
    token_data = TokenData(
        access_token=token["access_token"],
        refresh_token=token.get("refresh_token", ""),
        expires_at=time.time() + token.get("expires_in", 3600),
        email=profile.get("mail") or profile.get("userPrincipalName", ""),
        name=profile.get("displayName", ""),
        user_id=profile.get("id", ""),
    )

    # Store token
    token_store.save(token_data.email, token_data)
    logger.info(f"OAuth2 login successful: {token_data.email}")

    return token_data


def get_valid_token() -> Optional[TokenData]:
    """Get a valid (non-expired) token, auto-refresh if needed."""
    token_data = token_store.get_any()
    if not token_data:
        return None

    # Check if token is expired (with 5-minute buffer)
    if time.time() > token_data.expires_at - 300:
        if not token_data.refresh_token:
            token_store.clear()
            return None
        # Auto-refresh
        try:
            refreshed = refresh_token(token_data.refresh_token)
            token_data.access_token = refreshed["access_token"]
            token_data.refresh_token = refreshed.get("refresh_token", token_data.refresh_token)
            token_data.expires_at = time.time() + refreshed.get("expires_in", 3600)
            token_store.save(token_data.email, token_data)
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            token_store.clear()
            return None

    return token_data


def refresh_token(refresh_token: str) -> dict:
    """Refresh an expired access token."""
    tenant = settings.M365_TENANT_ID or "common"
    token_url = TOKEN_URL.format(tenant=tenant)

    import httpx
    response = httpx.post(
        token_url,
        data={
            "client_id": settings.M365_CLIENT_ID,
            "client_secret": settings.M365_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    response.raise_for_status()
    return response.json()
