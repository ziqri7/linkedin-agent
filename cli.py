import sys
import argparse
from linkedin_api import LinkedInAPIClient
from content_scheduler import LinkedInContentScheduler
import config

# Force UTF-8 on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Automation Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Perintah yang tersedia")

    # Command: preview
    p_preview = subparsers.add_parser("preview", help="Lihat draf postingan hari ini tanpa menerbitkan")
    p_preview.add_argument("--lang", choices=["id", "en"], default=config.DEFAULT_LANGUAGE, help="Pilihan bahasa (id/en)")

    # Command: publish
    p_pub = subparsers.add_parser("publish", help="Buat dan terbitkan postingan ke LinkedIn")
    p_pub.add_argument("--lang", choices=["id", "en"], default=config.DEFAULT_LANGUAGE, help="Pilihan bahasa (id/en)")
    p_pub.add_argument("--auto", action="store_true", help="Publikasikan langsung tanpa konfirmasi interaktif")

    # Command: custom
    p_custom = subparsers.add_parser("custom", help="Terbitkan teks kustom langsung")
    p_custom.add_argument("text", type=str, help="Teks postingan yang akan diterbitkan")

    # Command: test
    subparsers.add_parser("test", help="Uji koneksi API dan periksa profil terhubung")

    args = parser.parse_args()
    scheduler = LinkedInContentScheduler()
    client = LinkedInAPIClient()

    if args.command == "preview":
        pillar, title, post_text = scheduler.get_todays_post(language=args.lang)
        print(f"\n📑 [PREVIEW POST LINKEDIN - {args.lang.upper()}]")
        print(f"Pilar: {pillar.upper()} | Topik: {title}")
        print("=" * 60)
        print(post_text)
        print("=" * 60)
        print(f"Total Karakter: {len(post_text)}")

    elif args.command == "publish":
        pillar, title, post_text = scheduler.get_todays_post(language=args.lang)
        print(f"\n📑 [DRAFT POST LINKEDIN - {args.lang.upper()}]")
        print(f"Pilar: {pillar.upper()} | Topik: {title}")
        print("=" * 60)
        print(post_text)
        print("=" * 60)

        if not args.auto:
            confirm = input("\n🚀 Apakah Anda yakin ingin memposting ke LinkedIn? (y/n): ").strip().lower()
            if confirm not in ("y", "yes"):
                print("Dibatalkan oleh pengguna.")
                return

        print("\n⏳ Mengirimkan postingan ke LinkedIn...")
        post_id = client.publish_post(post_text)
        if post_id:
            print(f"🎉 Sukses! Post ID: {post_id}")

    elif args.command == "custom":
        print(f"\n⏳ Mengirimkan custom post ke LinkedIn...")
        post_id = client.publish_post(args.text)
        if post_id:
            print(f"🎉 Sukses! Post ID: {post_id}")

    elif args.command == "test":
        print("\n🔍 Memeriksa koneksi LinkedIn API...")
        profile = client.fetch_user_profile()
        if profile:
            print(f"✅ Koneksi Berhasil!")
            print(f"👤 Nama: {profile.get('name')}")
            print(f"🆔 URN: {profile.get('urn')}")
            print(f"⚙️ Status Mock Mode: {config.MOCK_MODE}")
        else:
            print("❌ Gagal terhubung ke profil LinkedIn. Periksa ACCESS_TOKEN di .env")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
