import os
import sys
from linkedin_api import LinkedInAPIClient
from content_scheduler import LinkedInContentScheduler
import config

# Force UTF-8 on Windows terminal / environments
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def run_scheduled_pipeline():
    """
    Master runner for LinkedIn Automated Publisher:
    1. Determines current language mode ('id' or 'en').
    2. Generates the strategic long-form post based on today's pillar.
    3. Publishes to LinkedIn via official REST API.
    """
    lang = os.getenv("LANGUAGE", config.DEFAULT_LANGUAGE).lower()
    print(f"🚀 [LINKEDIN RUNNER] Memulai pipeline penerbitan (Bahasa: {lang.upper()})...\n")

    scheduler = LinkedInContentScheduler()
    pillar, title, post_content = scheduler.get_todays_post(language=lang)

    print(f"📅 Pilar Aktif: {pillar.upper()} - {title}")
    print(f"📝 Panjang Teks: {len(post_content)} karakter")

    client = LinkedInAPIClient()
    post_id = client.publish_post(post_content)

    if post_id:
        print(f"\n🎉 [PIPELINE SUCCESS] Postingan LinkedIn berhasil dipublikasikan! (ID: {post_id})")
    else:
        print("\n⚠️ [PIPELINE NOTICE] Postingan belum berhasil dipublikasikan. Periksa kredensial atau log error di atas.")

if __name__ == "__main__":
    run_scheduled_pipeline()
