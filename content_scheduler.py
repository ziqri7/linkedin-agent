import sys
import random
from datetime import datetime
from typing import Tuple, Dict, Any
from content_generator import LinkedInContentGenerator
import config

# Force UTF-8 on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class LinkedInContentScheduler:
    """
    Schedules and generates goal-directed, high-conversion LinkedIn posts
    based on weekly pillars in both Indonesian (ID) and English (EN).
    """

    def __init__(self):
        self.generator = LinkedInContentGenerator()

    # Real-World Case Studies Bank (Bilingual)
    CASE_STUDIES = [
        {
            "id": "wa_order_automation",
            "title_id": "Otomasi Rekap Pesanan WhatsApp ke Google Sheets",
            "title_en": "Automating WhatsApp Order Entry to Live Cloud Sheets",
            "data_id": {
                "hook": "Masih banyak tim operasional yang menghabiskan 2–3 jam tiap malam cuma buat copy-paste chat pesanan WhatsApp ke spreadsheet manual.\n\nPadahal 1 webhook sederhana bisa memangkas waktu kerja itu jadi 1 detik.",
                "problem": "Di banyak bisnis retail & UMKM, admin toko sering salah catat alamat pengiriman atau total harga karena kelelahan membaca ratusan format chat pesan yang tidak seragam.",
                "points": [
                    {"title": "Validasi Format Otomatis", "desc": "Webhook menangkap pesan masuk, mengekstrak data nama, barang, dan nominal menggunakan skrip parser ringan."},
                    {"title": "Sinkronisasi Real-Time", "desc": "Data langsung masuk ke baris baru Google Sheets dan memicu notifikasi konfirmasi otomatis ke pembeli."},
                    {"title": "Penyimpanan & Keamanan", "desc": "Setiap transaksi memiliki log ID unik, mencegah pesanan ganda atau salah hitung stok."}
                ],
                "impact": "Waktu lembur admin terpangkas 80%, tingkat kesalahan rekap turun ke 0%, dan laporan penjualan siap ditinjau secara instan setiap saat.",
                "cta": "Banyak yang mengira sistem seperti ini harus mahal dan rumit, padahal arsitektur sederhana berbasis API sudah lebih dari cukup untuk menyelesaikan masalah operasional tahunan.\n\nApakah alur kerja di tim Anda masih ada yang direkap secara manual? Mari diskusi di kolom komentar! 👇",
                "tags": ["WorkflowAutomation", "Python", "BusinessEfficiency", "DigitalOperations"]
            },
            "data_en": {
                "hook": "Most operations teams still waste 2–3 hours every evening manually copying chat messages and order slips into spreadsheets.\n\nHere is how a 35-line Python webhook eliminated that repetitive workload in 1 second:",
                "problem": "Manual data entry isn't just slow—it's error-prone. Misspelled shipping addresses, duplicate orders, and inventory mismatch cost businesses thousands of dollars in lost operational time.",
                "points": [
                    {"title": "Payload Extraction", "desc": "Incoming webhook payloads capture order items and customer metadata with instant data validation."},
                    {"title": "Instant Cloud Sync", "desc": "Transactions append directly to cloud storage/sheets with unique idempotent request keys."},
                    {"title": "Automated Customer Handshake", "desc": "Customers receive immediate, structured confirmations without requiring manual admin intervention."}
                ],
                "impact": "80% reduction in daily administrative hours, zero data-entry human errors, and real-time inventory clarity for leadership.",
                "cta": "You don't need an over-engineered SaaS tool when a well-scoped automation script solves the root bottleneck.\n\nWhat manual workflow in your team currently consumes the most wasted hours? Let's discuss below! 👇",
                "tags": ["SoftwareEngineering", "Automation", "Python", "Productivity"]
            }
        },
        {
            "id": "excel_cleaner_script",
            "title_id": "Skrip Pembersih File Excel Cabang Otomatis",
            "title_en": "Consolidating 10+ Messy Excel Branch Reports in 3 Seconds",
            "data_id": {
                "hook": "Setiap akhir bulan, tim finance menghabiskan seharian cuma buat menyatukan puluhan file Excel cabang yang format tanggalnya berantakan.\n\nIni arsitektur script Python 40 baris yang menyelesaikannya dalam hitungan detik:",
                "problem": "Format kolom beda urutan, baris kosong yang terselip, dan duplikasi data membuat laporan master bulanan memakan waktu seharian hanya untuk proses pembersihan data.",
                "points": [
                    {"title": "Folder Ingestion", "desc": "Script membaca seluruh file .xlsx di folder input tanpa perlu membuka aplikasi Excel satu per satu."},
                    {"title": "Schema Normalization", "desc": "Menstandarkan tipe tanggal, menghapus spasi liar, dan membuang baris duplikat secara otomatis."},
                    {"title": "Master Export", "desc": "Menggabungkan seluruh cabang ke dalam 1 file master bersih yang siap diolah ke dashboard analitik."}
                ],
                "impact": "Pekerjaan 8 jam kerja manual berubah menjadi eksekusi 3 detik dengan tingkat akurasi data 100%.",
                "cta": "Efisiensi sejati bukan soal menyuruh tim bekerja lebih keras, melainkan memberi mereka sistem yang menghilangkan pekerjaan robotik.\n\nBagikan pengalaman Anda: proses data apa yang paling menyita waktu tim finance/operasional Anda? 👇",
                "tags": ["PythonAutomation", "DataOperations", "EfisiensiBisnis", "FinanceTech"]
            },
            "data_en": {
                "hook": "At month-end, operations and finance teams often spend an entire day cleaning and merging dozens of mismatched branch spreadsheets.\n\nHere is how a pragmatic 40-line Python script handles the entire pipeline in under 3 seconds:",
                "problem": "Inconsistent date formats, stray blank rows, and duplicate entries turn data consolidation into a massive productivity drain.",
                "points": [
                    {"title": "Automated Ingestion", "desc": "The script scans directory inputs, ingesting all multi-format workbooks without launching Excel."},
                    {"title": "Schema Normalization", "desc": "Standardizes date objects, trims whitespace, and deduplicates records programmatically."},
                    {"title": "Clean Master Export", "desc": "Outputs a clean, unified dataset directly structured for downstream business intelligence dashboards."}
                ],
                "impact": "Turned an 8-hour manual recurring chore into a 3-second automated task with 100% data integrity.",
                "cta": "True operational leverage comes from removing robotic manual tasks from your human talent.\n\nHow does your team currently handle multi-source data consolidation? Let's connect and discuss! 👇",
                "tags": ["Python", "DataEngineering", "WorkflowAutomation", "OperationalEfficiency"]
            }
        },
        {
            "id": "invoice_reminder_system",
            "title_id": "Sistem Pengingat Invoice & Piutang Otomatis",
            "title_en": "Automated Invoice & Overdue AR Follow-up Pipeline",
            "data_id": {
                "hook": "Cashflow bisnis sering tersendat bukan karena klien tidak mau bayar, tapi karena tim lupa atau canggung menagih invoice yang jatuh tempo.\n\nBerikut cara membangun sistem reminder piutang otomatis tanpa ribet:",
                "problem": "Follow-up manual yang terlambat 7–14 hari setelah jatuh tempo membuat arus kas operasional tertahan dan membebani tim keuangan.",
                "points": [
                    {"title": "Scheduled Cron Job", "desc": "Sistem terjadwal setiap pagi memeriksa database invoice dan menghitung sisa hari jatuh tempo."},
                    {"title": "Multi-tier Notification", "desc": "Otomatis mengirimkan reminder sopan pada H-3, hari H, dan H+2 melalui saluran resmi (Email/WhatsApp API)."},
                    {"title": "Status Auto-Update", "desc": "Begitu pembayaran terverifikasi, status invoice langsung ter-update lunas dan menonaktifkan reminder berikutnya."}
                ],
                "impact": "Tingkat ketepatan waktu pembayaran klien naik hingga 40%, tanpa drama canggung menagih manual.",
                "cta": "Membangun sistem otomasi tidak harus menunggu perusahaan berskala besar; semakin awal dibangun, semakin sehat cashflow bisnis Anda.\n\nAlur penagihan seperti apa yang saat ini berjalan di bisnis Anda? Tulis di bawah yuk! 👇",
                "tags": ["CashflowManagement", "OtomasiBisnis", "Fintech", "SoftwareSolutions"]
            },
            "data_en": {
                "hook": "Cashflow bottlenecks in growing businesses rarely happen because clients refuse to pay—they happen because teams forget or feel awkward following up on due invoices.\n\nHere is an automated invoice reminder architecture that solves this effortlessly:",
                "problem": "Manual follow-ups delayed by even 5–10 days directly strain working capital and consume unnecessary accounting bandwidth.",
                "points": [
                    {"title": "Scheduled Ledger Scanner", "desc": "A lightweight morning cron evaluates pending receivable records against dynamic due-date thresholds."},
                    {"title": "Staged Friendly Reminders", "desc": "Dispatches polite, professional notices at Due-3 days, On-Due, and Past-Due via verified API channels."},
                    {"title": "Reconciliation Trigger", "desc": "Payment webhook confirmation immediately marks the record as settled, halting further notifications."}
                ],
                "impact": "40% improvement in on-time receivables collection and zero awkward manual chasing.",
                "cta": "Building reliable operational automations early creates compounding efficiency as your company scales.\n\nWhat is your current strategy for managing accounts receivable workflows? Share your thoughts below! 👇",
                "tags": ["FinTech", "Operations", "AutomationArchitecture", "EngineeringLeadership"]
            }
        },
        {
            "id": "linkedin_agent_dogfood",
            "title_id": "Arsitektur Agen Konten LinkedIn Anti-Slop via Official REST API",
            "title_en": "Building an Anti-Slop Autonomous LinkedIn Agent via Official REST API v2",
            "data_id": {
                "hook": "Banyak akun LinkedIn kena shadowban bukan karena terlalu sering posting, tapi karena automasinya keliru (pakai bot scraping liar).\n\nIni arsitektur 4 modul Python yang kami bangun untuk automasi posting via Official REST API v2 tanpa biaya server sepeser pun:",
                "problem": "Konten AI di LinkedIn sering kali generik dan membosankan karena penuh frasa klise, sementara tool pihak ketiga yang tidak resmi berisiko memblokir akun secara permanen.",
                "points": [
                    {"title": "OAuth 2.0 & Token Handshake Otomatis", "desc": "Menggunakan protokol resmi (scope w_member_social & openid). Skrip menangkap callback lokal, mendeteksi Person URN secara dinamis, dan mengamankan kredensial di environment variable."},
                    {"title": "Filter Anti-Slop (Rule-Based Sanitizer)", "desc": "Menyaring kata pembuka generik AI, membatasi maksimal 4 hashtag relevan, dan memformat 2 baris awal khusus untuk memicu dwell time '...see more' pada layar mobile."},
                    {"title": "Bilingual Structured Pillars", "desc": "Konten dibagi ke pilar mingguan (Problem vs Solution, Case Study, dan System Architecture) dalam Bahasa Indonesia dan English."},
                    {"title": "Zero-Cost Cloud Automation", "desc": "Memanfaatkan cron job gratis di GitHub Actions untuk eksekusi terjadwal di jam prime time tanpa perlu sewa VPS."}
                ],
                "impact": "Distribusi konten konsisten 100% tanpa risiko akun, nol biaya server, dan format bacaan yang rapi serta bebas dari AI-slop.",
                "cta": "Automasi terbaik bukan soal menggantikan pemikiran manusia dengan spam, tapi membuang friksi teknis agar pesan berkualitas terdistribusi secara konsisten.\n\nApakah tim Anda sudah mulai memanfaatkan official API untuk automasi alur kerja? Mari diskusi di kolom komentar! 👇",
                "tags": ["SoftwareEngineering", "WorkflowAutomation", "Python", "Productivity"]
            },
            "data_en": {
                "hook": "Most LinkedIn accounts get shadowbanned not from high posting frequency, but from dangerous unapproved browser scraping bots.\n\nHere is the 4-module Python architecture we built to automate clean posting via the official REST API v2 with zero server cost:",
                "problem": "AI-generated content often turns into repetitive slop with cliché openers, while unauthorized third-party extensions risk permanent account bans.",
                "points": [
                    {"title": "Official OAuth 2.0 UGC Handshake", "desc": "Implements authorized REST API v2 (w_member_social & openid scopes) with automated localhost callback capture and dynamic Person URN detection."},
                    {"title": "Anti-Slop Heuristic Sanitizer", "desc": "Bans robotic AI clichés, enforces concise mobile-friendly spacing, and crafts 2-line openers designed for algorithmic dwell time."},
                    {"title": "Bilingual Strategic Pillars", "desc": "Rotates weekly focus between Problem/Solution teardowns, technical case studies, and engineering ROI insights in both ID and EN."},
                    {"title": "Zero-Cost GitHub Actions Cron", "desc": "Runs serverless scheduled triggers during peak engagement windows without maintaining expensive cloud VMs."}
                ],
                "impact": "100% compliant automation, zero monthly infrastructure overhead, and human-sounding technical copy that drives engagement.",
                "cta": "True operational leverage is not about spamming—it is about removing technical friction to keep high-value insights flowing consistently.\n\nAre you leveraging official APIs for your daily workflows? Let's connect and discuss below! 👇",
                "tags": ["SoftwareEngineering", "Automation", "Python", "Productivity"]
            }
        }
    ]

    def get_todays_post(self, language: str = None) -> Tuple[str, str, str]:
        """
        Determines the strategic content pillar and produces a formatted LinkedIn post.
        Language can be 'id' (Indonesian) or 'en' (English).
        """
        lang = language or config.DEFAULT_LANGUAGE
        weekday = datetime.now().weekday() # 0 = Monday, 2 = Wednesday, 4 = Friday
        selected_case = random.choice(self.CASE_STUDIES)

        case_data = selected_case["data_en"] if lang == "en" else selected_case["data_id"]
        title = selected_case["title_en"] if lang == "en" else selected_case["title_id"]

        pillar_name = "case_study"
        if weekday == 0:
            pillar_name = "problem_solution"
        elif weekday == 2:
            pillar_name = "case_study"
        elif weekday == 4:
            pillar_name = "business_cta"
        else:
            pillar_name = "pragmatic_insights"

        post_content = self.generator.format_post(
            hook=case_data["hook"],
            problem_statement=case_data["problem"],
            solution_points=case_data["points"],
            metrics_impact=case_data["impact"],
            cta=case_data["cta"],
            hashtags=case_data["tags"]
        )

        return pillar_name, title, post_content

if __name__ == "__main__":
    scheduler = LinkedInContentScheduler()
    print("\n--- PREVIEW POST BAHASA INDONESIA ---")
    p, t, content_id = scheduler.get_todays_post(language="id")
    print(f"Pilar: {p} | Judul: {t}\n")
    print(content_id)

    print("\n" + "=" * 60)
    print("\n--- PREVIEW POST ENGLISH (GLOBAL) ---")
    p_en, t_en, content_en = scheduler.get_todays_post(language="en")
    print(f"Pillar: {p_en} | Title: {t_en}\n")
    print(content_en)
