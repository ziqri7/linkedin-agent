import os
import sys
import json
import urllib.request
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

AUTH_CODE = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global AUTH_CODE
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            AUTH_CODE = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h1 style="color: #0a66c2;">✅ Autentikasi LinkedIn Berhasil!</h1>
                    <p>Kode otorisasi telah ditangkap oleh sistem. Anda dapat menutup tab browser ini dan kembali ke terminal.</p>
                </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            err = params.get("error_description", ["Gagal otorisasi"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h1>❌ Error dari LinkedIn: {err}</h1><p>Pastikan produk 'Share on LinkedIn' sudah di-request di tab Products.</p>".encode("utf-8"))

    def log_message(self, format, *args):
        pass # Silence HTTP server logs

def run_token_setup():
    print("=" * 65)
    print(" 🔑 LINKEDIN OAUTH2 TOKEN GENERATOR & VERIFIER ")
    print("=" * 65)

    client_id = os.getenv("LINKEDIN_CLIENT_ID", "").strip()
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print("\nSilakan masukkan kredensial LinkedIn Developer App Anda:")
        if not client_id:
            client_id = input("1. Masukkan LINKEDIN_CLIENT_ID: ").strip()
        if not client_secret:
            client_secret = input("2. Masukkan LINKEDIN_CLIENT_SECRET: ").strip()

    redirect_uri = "http://localhost:8000/callback"
    scopes = "openid profile w_member_social"

    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={client_id}"
        f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&scope={urllib.parse.quote(scopes)}"
    )

    print(f"\n🌐 Membuka browser untuk otorisasi LinkedIn...")
    print(f"URL: {auth_url}\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    print("⏳ Menunggu verifikasi di browser (port 8000)...")
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)

    while AUTH_CODE is None:
        httpd.handle_request()

    httpd.server_close()
    print(f"✅ Authorization code berhasil didapatkan!")

    # Tukar Authorization Code dengan Access Token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": AUTH_CODE,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }).encode("utf-8")

    req = urllib.request.Request(token_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})

    try:
        with urllib.request.urlopen(req) as response:
            token_data = json.loads(response.read().decode("utf-8"))
            access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in")
            print(f"🎉 Access Token berhasil diterbitkan! (Masa berlaku: {expires_in // 86400} hari)")
    except Exception as e:
        print(f"❌ Gagal menukar token: {e}")
        return

    # Ambil Profile & Person URN
    person_urn = ""
    user_name = "Pengguna LinkedIn"

    # Percobaan 1: OpenID userinfo
    try:
        userinfo_url = "https://api.linkedin.com/v2/userinfo"
        req_user = urllib.request.Request(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})
        with urllib.request.urlopen(req_user, timeout=10) as resp:
            user_data = json.loads(resp.read().decode("utf-8"))
            sub = user_data.get("sub", "")
            if sub:
                person_urn = f"urn:li:person:{sub}" if not sub.startswith("urn:li:") else sub
                user_name = user_data.get("name", user_name)
    except Exception:
        pass

    # Percobaan 2: Legacy me endpoint
    if not person_urn:
        try:
            me_url = "https://api.linkedin.com/v2/me"
            req_me = urllib.request.Request(me_url, headers={"Authorization": f"Bearer {access_token}"})
            with urllib.request.urlopen(req_me, timeout=10) as resp_me:
                data_me = json.loads(resp_me.read().decode("utf-8"))
                uid = data_me.get("id", "")
                if uid:
                    person_urn = f"urn:li:person:{uid}"
                    fname = data_me.get("localizedFirstName", "")
                    lname = data_me.get("localizedLastName", "")
                    user_name = f"{fname} {lname}".strip() or user_name
        except Exception:
            pass

    if person_urn:
        print(f"👤 Profil Terhubung: {user_name} ({person_urn})")
    else:
        print("\n⚠️ Person URN tidak terdeteksi otomatis.")
        print("💡 Tips: Anda bisa memasukkan username/ID profil LinkedIn Anda, atau tekan Enter untuk menggunakan default.")
        manual_id = input("Masukkan ID Profil LinkedIn (atau URN): ").strip()
        if manual_id:
            person_urn = f"urn:li:person:{manual_id}" if not manual_id.startswith("urn:li:") else manual_id
        else:
            person_urn = f"urn:li:person:{client_id[:10]}"

    # Tulis ke .env
    env_content = f"""# LinkedIn API Credentials (Auto-Generated)
LINKEDIN_CLIENT_ID={client_id}
LINKEDIN_CLIENT_SECRET={client_secret}
LINKEDIN_REDIRECT_URI={redirect_uri}
LINKEDIN_ACCESS_TOKEN={access_token}
LINKEDIN_PERSON_URN={person_urn}

# Execution Modes
MOCK_MODE=False
DEFAULT_LANGUAGE=id
POST_DELAY_SECONDS=3
"""
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(env_content)

    print("\n" + "=" * 65)
    print("✅ KONFIGURASI SUKSES! File .env telah diperbarui ke mode LIVE.")
    print("=" * 65)

if __name__ == "__main__":
    run_token_setup()
