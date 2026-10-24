# Data — Catatan Dataset Capstone

Dataset capstone ini TIDAK diduplikasi sebagai file CSV lepas di repo,
karena file lengkapnya sudah ada di dalam `capstone-project.zip`
di root repo ini dan sudah terverifikasi (lihat hasil verifikasi di bawah).
Catatan ini dibuat 24 Oktober 2026.

## Asal dataset

- Dataset survei developer Stack Overflow yang disediakan course
  IBM Data Analyst Professional Certificate, Course 9 (Data Analyst
  Capstone Project) di Coursera. Diunduh Baghiz dari URL course saat
  pengerjaan capstone (6 Oktober 2026), lalu dibersihkan:
  20 baris duplikat dibuang dengan `drop_duplicates()`.
- File di dalam zip persis sama (ukuran + CRC32) dengan file kerja asli
  di workspace pengerjaan capstone.

## Isi `capstone-project.zip` (34.409.598 byte, 22 entri)

| Path di dalam zip | Baris data | Kolom | Ukuran |
|---|---|---|---|
| `capstone-project/data/raw/survey-data-with-duplicate.csv` | 65.457 | 114 | 154.822.125 byte |
| `capstone-project/data/clean/survey-data.csv` | 65.437 | 114 | 159.525.875 byte |

Zip juga berisi `analyze_survey.py`, `findings.json`, `README.md`, dan
12 chart PNG di `capstone-project/charts/` (duplikat dari yang ada di repo).

## Verifikasi (24 Oktober 2026)

- `zipfile.testzip()`: OK, tidak ada entri rusak.
- CRC32 kedua CSV di dalam zip cocok dengan file CSV asli di workspace.
- Jumlah baris dihitung langsung dari dalam zip: mentah 65.457 baris data,
  bersih 65.437 baris data, masing-masing 114 kolom
  (kolom pertama: ResponseId, MainBranch, Age, Employment, RemoteWork, Check).
- Angka ini cocok dengan README repo: 65.457 responden mentah menjadi
  65.437 baris bersih setelah 20 duplikat dihapus.

## Cara memakai

1. Ekstrak `capstone-project.zip`.
2. `analyze_survey.py` memuat file bersih dengan `pd.read_csv("survey-data.csv")`
   dari folder kerjanya, jadi jalankan skrip dari folder yang berisi
   `survey-data.csv` hasil ekstrak (`capstone-project/data/clean/`),
   atau salin CSV bersih itu ke sebelah skrip.

## Kolom yang benar-benar dipakai `analyze_survey.py` (15 dari 114)

ResponseId tidak dipakai skrip; kolom yang dipakai: Age,
ConvertedCompYearly, Country, DatabaseHaveWorkedWith,
DatabaseWantToWorkWith, EdLevel, Employment, JobSat,
LanguageHaveWorkedWith, LanguageWantToWorkWith, MainBranch,
NEWCollabToolsHaveWorkedWith, NEWCollabToolsWantToWorkWith,
PlatformHaveWorkedWith, WebframeHaveWorkedWith.

Sisa kolom tetap disertakan karena file di dalam zip adalah dataset
course apa adanya (bukan ekstrak buatan). File mentah dan bersih
masing-masing di atas 150 MB, jauh di atas batas praktis GitHub
Contents API (sekitar 25 MB per file), jadi bentuk zip di root repo
adalah satu-satunya salinan dataset di repo ini dan memang sudah
lengkap; tidak perlu ekstrak subset tambahan.

## Yang bukan file dataset

Data lowongan pekerjaan pada tahap data collection capstone diambil
lewat Jobs API dan web scraping saat pengerjaan, bukan dari file
dataset, jadi tidak ada file-nya di repo.
