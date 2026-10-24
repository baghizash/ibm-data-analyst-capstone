# IBM Data Analyst Capstone Project

Proyek akhir dari **IBM Data Analyst Professional Certificate** (Course 9/11) di Coursera — analisis tren teknologi dari survei developer global.

## Data
Hasil survei developer dari Stack Overflow (dataset `survey-data.csv`): **65.457 responden mentah**, dibersihkan menjadi **65.437 baris × 114 kolom** (20 baris duplikat dihapus). Kolom mencakup bahasa pemrograman yang dipakai dan diinginkan, database, IDE, platform, demografi, kompensasi, dan kepuasan kerja.

## Yang dilakukan
1. **Data wrangling** — hapus duplikat, normalisasi nilai kompensasi tahunan, standarisasi kolom multi-pilihan.
2. **Exploratory data analysis** — tren bahasa, database, IDE, platform; distribusi usia, negara, dan kompensasi per negara.
3. **Visualisasi** — 9 chart analisis + 3 dashboard composite (`charts/`).
4. **Dashboard** — ringkasan temuan dalam 3 tab dashboard.
5. **Laporan** — presentasi 20 slide (PDF, nama file persis sesuai ketentuan Coursera).

## Temuan utama
- **JavaScript** bahasa paling banyak dipakai (37.492 responden); **Python** paling banyak diinginkan (25.047).
- **Rust** bintang yang sedang naik: rasio ingin/memakai 2,28x.
- **PostgreSQL** database paling dominan; **VS Code** dipakai 65% responden (42.751).
- Median kompensasi global **USD 65.000/tahun**; kesenjangan besar antar negara (AS ~USD 143rb vs India ~USD 16,7rb).
- 76,7% responden adalah developer profesional; 67,9% puas dengan pekerjaannya.

## Isi repo
- `charts/` — 12 PNG: 9 chart analisis + 3 dashboard
- `analyze_survey.py` — skrip analisis yang bisa diulang (reproducible)
- `findings.json` — hasil analisis terstruktur
- `capstone-project.zip` (34 MB) — bundle lengkap: data mentah + data bersih + skrip + chart + README

## Nilai
Proyek akhir lulus via penilaian AI Coursera. Sertifikat resmi IBM Data Analyst Professional Certificate menyusul setelah verifikasi Coursera.

---
Bagian dari portfolio 11 course: [ibm-data-analyst-portfolio](https://github.com/baghizash/ibm-data-analyst-portfolio)
