---
title: "HANDOFF — LinkedIn Autonomous Growth Agent"
updated: 2026-08-19
project: linkedin-agent
tags: [handoff, linkedin-agent, agent-collab]
---

# 🤝 HANDOFF — LinkedIn Autonomous Growth & Content Agent

> **Tujuan Proyek:** Sistem agen otonom untuk meriset, memformat (anti-slop), dan mempublikasikan konten studi kasus automasi alur kerja tingkat enterprise ke LinkedIn via Official REST API v2 & UGC Post protocol.  
> **Status:** ✅ Selesai 100% (Modul & Arsitektur Lengkap)

---

## 📁 Peta Berkas & Modul Utama

```
linkedin-agent/
├── .env.example              # Template environment variables (Token & URN)
├── .github/workflows/
│   └── linkedin_cron.yml     # Workflow GitHub Actions untuk penerbitan terjadwal di cloud
├── cli.py                    # Antarmuka CLI interaktif (test, preview, publish, custom)
├── config.py                 # Konfigurasi aplikasi & fallback credentials
├── content_generator.py      # Engine anti-slop & formatter postingan panjang
├── content_scheduler.py      # Bank studi kasus bilingual (ID/EN) & pemilih pilar mingguan
├── linkedin_api.py           # Klien resmi LinkedIn REST API v2 & UGC Post protocol
├── persona.json              # Definisi persona, target audiens, dan aturan anti-slop
├── scheduled_runner.py       # Master pipeline runner untuk eksekusi terjadwal
├── setup_token.py            # Otomasi OAuth 2.0 via browser callback localhost:8000
├── README.md                 # Dokumentasi arsitektur dan panduan cepat
└── SETUP_NOTES.md            # Panduan pendaftaran aplikasi di LinkedIn Developer Portal
```

---

## 🔑 Arsitektur & Aturan Sistem

1. **Official API Compliance:** 100% menggunakan protokol resmi OAuth 2.0 dengan scope `w_member_social`, `openid`, dan `profile`. Tidak ada scraping browser tanpa izin untuk menjamin keselamatan akun dari ban/shadowban.
2. **Anti-Slop Content Philosophy:** Setiap draf postingan wajib melewati pembersihan kata klise AI, menjaga panjang preview baris pembuka untuk dwell time klik *"...see more"*, dan membatasi maksimal 4 hashtag relevan.
3. **Bilingual Target Audience:**
   - **ID (Indonesia):** Ditujukan untuk owner bisnis, agensi, dan manajer operasional regional.
   - **EN (English):** Ditujukan untuk tech founders, CTO, dan solopreneur global.
4. **Zero-Cost Deployment:** Cukup menggunakan GitHub Actions cron job tanpa memerlukan server VPS berbayar.

---

## 🚀 Perintah CLI yang Tersedia

```bash
# Uji koneksi API dan identitas profil
python cli.py test

# Preview draf postingan hari ini (Bahasa Indonesia)
python cli.py preview --lang id

# Preview draf postingan hari ini (English)
python cli.py preview --lang en

# Terbitkan draf postingan hari ini ke feed LinkedIn
python cli.py publish --lang id

# Terbitkan postingan kustom langsung
python cli.py custom "Teks postingan kustom Anda"
```
