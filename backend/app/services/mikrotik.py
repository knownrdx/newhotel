from routeros_api import RouterOsApiPool
from app.core.security import decrypt_secret
from app.models.models import Router


class MikroTikService:
    def connect(self, router: Router):
        pool = RouterOsApiPool(
            router.host,
            username=router.username,
            password=decrypt_secret(router.password_encrypted),
            port=router.api_port,
            plaintext_login=True,
        )
        return pool

    def ensure_profile(self, router: Router, profile_name: str, rate_limit: str, session_timeout: str | None = None):
        pool = self.connect(router)
        api = pool.get_api()
        resource = api.get_resource("/ip/hotspot/user/profile")
        existing = resource.get(name=profile_name)
        if not existing:
            resource.add(name=profile_name, rate_limit=rate_limit, session_timeout=session_timeout or "")
        pool.disconnect()

    def create_hotspot_user(self, router: Router, username: str, password: str, profile_name: str, shared_users: int = 1):
        pool = self.connect(router)
        api = pool.get_api()
        users = api.get_resource("/ip/hotspot/user")
        current = users.get(name=username)
        if current:
            users.set(id=current[0][".id"], password=password, profile=profile_name)
        else:
            users.add(name=username, password=password, profile=profile_name, shared_users=str(shared_users))
        pool.disconnect()

    def disable_hotspot_user(self, router: Router, username: str):
        pool = self.connect(router)
        api = pool.get_api()
        users = api.get_resource("/ip/hotspot/user")
        current = users.get(name=username)
        if current:
            users.set(id=current[0][".id"], disabled="yes")
        pool.disconnect()
