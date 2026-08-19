# Panduan Lengkap Setup & Integrasi LinkedIn API

Dokumen ini menjelaskan langkah demi langkah cara mengaktifkan izin resmi **LinkedIn Developer App** dan menghubungkannya ke **LinkedIn Agent**.

---

## 1. Langkah Pembuatan LinkedIn Developer App

1. Buka [LinkedIn Developers Portal](https://www.linkedin.com/developers/apps) dan login dengan akun LinkedIn Anda.
2. Klik tombol **Create App**.
3. Isi formulir aplikasi:
   * **App name:** `Automation Portfolio Engine` (atau nama pilihan Anda)
   * **LinkedIn Page:** Hubungkan dengan Company Page Anda (atau buat Company Page baru gratis dalam 1 menit).
   * **Privacy policy URL:** Masukkan URL website Anda atau link profil LinkedIn.
   * **App logo:** Unggah gambar logo/profil sederhana.
4. Klik **Create app**.

---

## 2. Mengaktifkan Produk & Izin (Products / Scopes)

Di tab **Products** pada dashboard aplikasi LinkedIn:
1. Pilih dan klik **Request Access** untuk produk:
   * **Share on LinkedIn** (Memberikan izin posting: `w_member_social`).
   * **Sign In with LinkedIn using OpenID Connect** (Memberikan izin profil: `openid`, `profile`, `email`).
2. Masuk ke tab **Auth**:
   * Di bagian **OAuth 2.0 settings**, tambahkan URL di **Authorized redirect URLs for your app**:
     `http://localhost:8000/callback`
   * Catat **Client ID** dan **Client Secret** Anda.

---

## 3. Otorisasi Otomatis via `setup_token.py`

Jalankan perintah berikut di terminal:
```bash
cd C:\Users\bidol\linkedin-agent
python setup_token.py
```

* Skrip akan otomatis membuka browser untuk otorisasi akun.
* Begitu Anda klik **Allow / Izinkan**, skrip akan menangkap kode otorisasi, menukar token, mengambil `Person URN`, dan menulis file `.env` secara otomatis.

---

## 4. Pengujian Lokal (CLI)

```bash
# 1. Uji koneksi API dan profil
python cli.py test

# 2. Preview draf postingan hari ini (Bahasa Indonesia)
python cli.py preview --lang id

# 3. Preview draf postingan hari ini (English / Global)
python cli.py preview --lang en

# 4. Publikasikan langsung ke feed
python cli.py publish --lang id
```

---

## 5. Otomatisasi via GitHub Actions

Agar postingan berjalan otomatis di cloud:
1. Buat repository baru di GitHub dan lakukan `git push`.
2. Masuk ke **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions**.
3. Tambahkan 2 secrets:
   * `LINKEDIN_ACCESS_TOKEN`: Isi dengan token dari file `.env`.
   * `LINKEDIN_PERSON_URN`: Isi dengan URN dari file `.env` (contoh: `urn:li:person:XXXXX`).
4. Pipeline di `.github/workflows/linkedin_cron.yml` akan otomatis aktif pada jam prime time LinkedIn.
