# 🏆 Scoreboard Cyber HUD & Grand Finals Ceremony (TikTok LIVE Studio & OBS)

Aplikasi Web Modular Overlay untuk **TikTok LIVE Studio** dan **OBS Studio**.

## 🌟 Fitur Utama
- **4 View Modular Transparan**:
  - `/?view=tabel` : Overlay Klasemen 20 Kursi Cyber HUD (Transparan).
  - `/?view=podium` : Overlay Podium Juara *Hall of Champions* (Transparan saat standby, otomatis meletus perayaan saat Host klik PODIUM).
  - `/?view=notif` : Overlay Notifikasi Tangkapan (Toast alert & sound FX di atas webcam/sudut layar).
  - `/` (default) : Dashboard Operator Host untuk mengontrol skor & pemenang.
- **Sinkronisasi Real-Time**:
  - Menggunakan **Cloud Real-Time SSE Bus** + `BroadcastChannel`. Kontrol dari HP atau browser Admin langsung tercermin seketika di TikTok LIVE Studio tanpa jeda.
- **Serverless API Roblox**:
  - `/api/cari-roblox` : Resolusi otomatis akun Roblox & foto profil.
  - `/api/roblox-3d-model` : Model 3D avatar Roblox.

## 🚀 Deployment ke Vercel
1. Buat repository baru di GitHub (misal: `papan-skor-tiktok`).
2. Upload seluruh isi folder ini.
3. Import repository tersebut ke [Vercel](https://vercel.com/new).
4. Selesai! Vercel akan otomatis mengenali folder `public/` dan `api/`.
