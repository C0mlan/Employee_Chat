# middleware.py
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError
from user_agents import parse
import logging

logger = logging.getLogger(__name__)


class WebSocketJWTAuthMiddleware(BaseMiddleware):
    """
    JWT auth middleware for Django Channels websockets.
    - Expects: Authorization: Bearer <token> in handshake headers.
    - On success: sets scope["user_id"].
    - On failure: closes the websocket with a custom code.
    """
    CLOSE_MISSING_AUTH = 4001
    CLOSE_INVALID_TOKEN = 4002
    CLOSE_USER_NOT_FOUND = 4003
    CLOSE_SERVER_ERROR = 4011

    async def __call__(self, scope, receive, send):
        user_agent = self._get_user_agent(scope)
        ip_address = scope["client"][0] if scope.get("client") else None
        
        browser_family = getattr(user_agent, "browser", None)
        browser = getattr(browser_family, "family", "Unknown") if browser_family else "Unknown"
        try:
            token = self._get_token_from_scope(scope)
            if token is None:
                logger.warning("WebSocket authentication failed: missing token",

                    extra={
                        "path": scope.get("path"),
                        "browser": browser,
                        "ip_address": ip_address
                    },
                )
                await self._reject_connection(send, self.CLOSE_MISSING_AUTH, "Missing authentication token")
                return
            try:
                access_token = AccessToken(token)
                payload = access_token.payload

            except TokenError as e:
                logger.warning(
                    "WebSocket authentication failed",
                    extra={
                        "path": scope.get("path"),
                        "error_type": type(e).__name__,
                        "browser": browser,
                        "ip_address": ip_address
                    },
                )

                await self._reject_connection(
                    send,
                    self.CLOSE_INVALID_TOKEN,
                    "Token validation failed",
                )
                return

            user_id = payload.get("user_id")
            if not user_id:
                logger.warning(
                    "WebSocket authentication failed: token missing user_id claim",
                    extra={
                        "path": scope.get("path"),
                        "browser": user_agent.browser.family,
                        "ip_address": ip_address
                    },
                )
                await self._reject_connection(send, self.CLOSE_INVALID_TOKEN, "Invalid token: no user_id claim")
                return
    
            scope["user_id"] = user_id
          
            logger.debug(
                "WebSocket authentication successful",
                extra={
                    "user_id": user_id,
               
                },
            )
            return await super().__call__(scope, receive, send)
        except Exception as e:
            # Catch unexpected errors to prevent crashes
            logger.error(
                "WebSocket authentication middleware unexpected error: %s",
                str(e),
                extra={
                    "path": scope.get("path"),
                    "scope_type": scope.get("type"),
                    "browser": user_agent.browser.family,
                    "ip_address": ip_address
                },
                exc_info=True,
                )
            await self._reject_connection(send, self.CLOSE_SERVER_ERROR, "Authentication service unavailable")
            
        

    def _get_token_from_scope(self, scope: Dict[str, Any]) -> Optional[str]:
            """
            Extract JWT token from Authorization header.
            
            Args:
                scope: ASGI scope dict
                
            Returns:
                Token string or None if not found/invalid format
            """
            try:
                headers = dict(scope.get("headers", []))
                auth_header = headers.get(b"authorization", b"").decode("utf-8", errors="ignore").strip()
                
                if not auth_header:
                    return None
                
                if not auth_header.startswith("Bearer "):
                    logger.debug(
                        "Authorization header present but not Bearer scheme",
                        extra={
                            "auth_header_prefix": auth_header[:20],
                            "browser": user_agent.browser.family,
                            "ip_address": ip_address},
                    )
                    return None
                
                token = auth_header.split(" ", 1)[1].strip()
                
                # Basic validation
                if not token:
                    return None
                
                return token
                
            except Exception as e:
                logger.debug(
                    "Failed to extract token from headers: %s",
                    str(e),
                    extra={
                        "error_type": type(e).__name__,
                        "browser": user_agent.browser.family,
                        "ip_address": ip_address},
            
                )
                return None

    async def _reject_connection(self, send, code: int, reason: str):
        """
        Close WebSocket connection with custom code and reason.
        
        Args:
            send: ASGI send callable
            code: WebSocket close code (4000-4999 for application errors)
            reason: Human-readable reason (max 125 bytes)
        """
        try:
            reason_truncated = reason[:125].encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            
            await send({
                "type": "websocket.close",
                "code": code,
                "reason": reason_truncated,
            })
            
            logger.info("WebSocket connection rejected",
                extra={"close_code": code,
                    "reason": reason_truncated,
                },
            )
            
        except Exception as e:
            # Connection may already be closed
            logger.debug(
                "Failed to send close frame: %s",
                str(e),
                extra={
                    "close_code": code, 
                    "reason": reason,
                    "browser": user_agent.browser.family,
                    "ip_address": ip_address},
                    )
                    
            
            

    def _get_user_agent(self, scope):
        headers = dict(scope.get("headers", []))

        user_agent_string = headers.get(b"user-agent", b"").decode(
            "utf-8",
            errors="ignore",
        )

        return parse(user_agent_string)