import random
from datetime import datetime
from typing import Tuple, Dict, Any
from content_generator import LinkedInContentGenerator
import config

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
