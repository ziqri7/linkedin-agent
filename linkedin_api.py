import json
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional, Dict, Any
import config

class LinkedInAPIClient:
    """
    Production-ready LinkedIn REST API Client.
    Supports official REST API v2 & UGC Post protocol with automatic mock fallback.
    """

    def __init__(self, access_token: Optional[str] = None, person_urn: Optional[str] = None):
        self.access_token = access_token or config.LINKEDIN_ACCESS_TOKEN
        self.person_urn = person_urn or config.LINKEDIN_PERSON_URN
        self.mock_mode = config.MOCK_MODE

        # Ensure person URN has standard urn:li:person: prefix
        if self.person_urn and not self.person_urn.startswith("urn:li:"):
            self.person_urn = f"urn:li:person:{self.person_urn}"

    def get_headers(self, version: str = "202401") -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": version,
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def fetch_user_profile(self) -> Optional[Dict[str, Any]]:
        """Fetches the authenticated user profile and extracts Person URN."""
        if self.mock_mode or not self.access_token:
            return {"id": "mock_user_123", "urn": "urn:li:person:mock_user_123", "name": "Mock Developer"}

        # Attempt 1: OpenID userinfo endpoint
        url_userinfo = "https://api.linkedin.com/v2/userinfo"
        req = urllib.request.Request(url_userinfo, headers={"Authorization": f"Bearer {self.access_token}"})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                sub = data.get("sub", "")
                name = data.get("name", f"{data.get('given_name', '')} {data.get('family_name', '')}".strip())
                return {
                    "id": sub,
                    "urn": f"urn:li:person:{sub}" if not sub.startswith("urn:li:") else sub,
                    "name": name,
                    "raw": data
                }
        except Exception as e:
            # Attempt 2: Legacy me endpoint
            url_me = "https://api.linkedin.com/v2/me"
            req_me = urllib.request.Request(url_me, headers={"Authorization": f"Bearer {self.access_token}"})
            try:
                with urllib.request.urlopen(req_me, timeout=15) as resp_me:
                    data_me = json.loads(resp_me.read().decode("utf-8"))
                    user_id = data_me.get("id", "")
                    return {
                        "id": user_id,
                        "urn": f"urn:li:person:{user_id}",
                        "name": f"{data_me.get('localizedFirstName', '')} {data_me.get('localizedLastName', '')}".strip(),
                        "raw": data_me
                    }
            except Exception as e_me:
                print(f"❌ [LINKEDIN API ERROR] Gagal mengambil profil user: {e_me}")
                return None

    def publish_post(self, text: str) -> Optional[str]:
        """
        Publishes a long-form text post to the LinkedIn feed.
        Returns the post URN/ID upon success, or None on failure.
        """
        if self.mock_mode:
            print("\n🧪 [MOCK MODE] Postingan LinkedIn disimulasikan:")
            print("=" * 60)
            print(text)
            print("=" * 60)
            mock_id = f"urn:li:share:mock_{abs(hash(text)) % 10000000000}"
            print(f"✅ [MOCK SUCCESS] Postingan terbit (Mock ID: {mock_id})")
            return mock_id

        if not self.access_token or not self.person_urn:
            print("❌ [LINKEDIN ERROR] ACCESS_TOKEN atau PERSON_URN belum dikonfigurasi.")
            return None

        # Attempt 1: Standard UGC Posts endpoint (Most reliable for member social posting)
        ugc_url = "https://api.linkedin.com/v2/ugcPosts"
        payload_ugc = {
            "author": self.person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            req_ugc = urllib.request.Request(
                ugc_url,
                data=json.dumps(payload_ugc).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req_ugc, timeout=20) as resp_ugc:
                res_json = json.loads(resp_ugc.read().decode("utf-8"))
                ugc_id = res_json.get("id")
                print(f"✅ [LINKEDIN SUCCESS] Postingan berhasil tayang via UGC Posts! (ID: {ugc_id})")
                return ugc_id
        except Exception as e_ugc:
            print(f"⚠️ [UGC POST NOTICE] Mencoba endpoint REST posts... Error: {e_ugc}")

            # Attempt 2: Modern REST posts API fallback
            rest_url = "https://api.linkedin.com/rest/posts"
            payload_rest = {
                "author": self.person_urn,
                "commentary": text,
                "visibility": "PUBLIC",
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": []
                },
                "lifecycleState": "PUBLISHED",
                "isReshareDisabledByAuthor": False
            }

            try:
                req = urllib.request.Request(
                    rest_url,
                    data=json.dumps(payload_rest).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json",
                        "X-Restli-Protocol-Version": "2.0.0"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=20) as response:
                    post_urn = response.headers.get("x-restli-id") or response.headers.get("x-linkedin-id")
                    if not post_urn and response.status in (200, 201):
                        post_urn = f"{self.person_urn}_post"
                    print(f"✅ [LINKEDIN SUCCESS] Postingan berhasil tayang via REST API! (ID: {post_urn})")
                    return post_urn
            except Exception as e_rest:
                print(f"❌ [LINKEDIN ERROR] Gagal memposting ke LinkedIn: {e_rest}")
                return None
