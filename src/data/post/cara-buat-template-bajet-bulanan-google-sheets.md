---
publishDate: 2026-07-15
title: "Cara Buat Bajet Bulanan Guna Google Sheets 2026"
excerpt: "Panduan lengkap cara buat template bajet bulanan guna Google Sheets. Termasuk formula, tracking perbelanjaan, dan tips ikut gaji Malaysia."
category: Kerjaya
image: "~/assets/images/hero-cara-buat-template-bajet-bulanan-google-sheets.jpg"
tags:
  - template bajet
  - google sheets
  - bajet bulanan
  - urus gaji
  - perbelanjaan
  - simpanan
  - "2026"
author: RakyatHub
faq:
  - question: "Google Sheets template bajet bulanan ni free ke?"
    answer: "Ya, Google Sheets adalah percuma. Cuma kena ada akaun Google je. Template yang dikongsikan dalam artikel ni boleh terus copy dan guna tanpa bayar sesen pun."
  - question: "Berapa lama nak set up template bajet bulanan guna Google Sheets?"
    answer: "Anggaran 15-30 minit je untuk set up lengkap termasuk kategori pendapatan, perbelanjaan tetap, dan formula automatik. Lepas tu setiap bulan hanya perlu update 5-10 minit."
  - question: "Apa beza template bajet Google Sheets dengan aplikasi macam Money Lover?"
    answer: "Google Sheets lebih fleksibel — korang boleh customize ikut apa je kategori yang nak ditingau. Aplikasi macam Money Lover atau Wallet by BudgetBakers lebih automatik dengan sync bank, tapi versi free terhad. Google Sheets totally free dan data korang sendiri."
  - question: "Boleh guna Excel untuk template bajet ni?"
    answer: "Boleh. Semua formula dan struktur dalam panduan ni boleh guna dalam Microsoft Excel. Cuma Google Sheets lebih mudah sebab boleh access dari mana-mana guna handphone."
---

Ramai orang susah nak tracking perbelanjaan bulanan. Gaji masuk, lepas tu habis — tak tahu duit tu pergi mana. Salah satu cara paling berkesan untuk kawal kewangan adalah dengan **guna template bajet bulanan**.

Google Sheets adalah platform percuma yang power untuk tujuan ni. Dalam artikel ni, korang akan belajar cara buat template bajet bulanan sendiri dari mula — termasuk formula, kategori, dan tips tracking yang betul.

## 📊 Kenapa Guna Google Sheets Untuk Bajet Bulanan?

Banyak aplikasi kewangan kat pasaran macam Money Lover, Wallet by BudgetBakers, atau YNAB. Tapi Google Sheets ada kelebihan tersendiri:

| Kelebihan | Google Sheets | Aplikasi Kewangan |
|-----------|:------------:|:-----------------:|
| Percuma | ✅ | Limited free version |
| Boleh customize | ✅ Sepenuhnya | Terhad |
| Data milik sendiri | ✅ | Bergantung pada servis |
| Access offline | ✅ | Bergantung pada app |
| Tiada iklan | ✅ | Biasanya ada |
| Auto backup | ✅ Google Drive | Bergantung |

Google Sheets sesuai untuk semua peringkat gaji — dari yang gaji bawah RM2,000 sampai RM10,000+. Yang penting adalah **konsisten mencatat**.

## 💰 Cara Buat Template Bajet Bulanan — Langkah Demi Langkah

### Langkah 1: Buka Google Sheets Baru

1. Buka [sheets.google.com](https://sheets.google.com)
2. Sign in dengan akaun Gmail korang
3. Klik butang **+ Blank** (atau + Kosong) untuk buka spreadsheet baru
4. Rename file: Klik "Untitled spreadsheet" — tukar nama jadi "Bajet Bulanan 2026"

### Langkah 2: Setup Column Headers

Dalam Row 1, taip column headers ni:

| A | B | C | D | E |
|---|---|---|---|---|
| Kategori | Belanjawan (RM) | Sebenar (RM) | Beza (RM) | Nota |

Jadikan header ni bold dan background warna gelap supaya nampak profesional.

### Langkah 3: Senarai Kategori Perbelanjaan

Dalam Column A, mula dari Row 2, taip kategori ikut kumpulan:

**Pendapatan (mulai Row 2):**
- Gaji bersih
- Pendapatan sampingan / side hustle
- Dividen / pelaburan

**Perbelanjaan Tetap / Keperluan (mulai Row 6):**
- Sewa rumah
- Bil elektrik & air
- Bil internet & phone
- Makan & groceries
- Pengangkutan (minyak, tol, parking)
- Insurans
- Bayaran hutang (kereta, PTPTN, rumah)

**Perbelanjaan Fleksibel / Kehendak (mulai Row 14):**
- Makan luar
- Hiburan (Netflix, Spotify, YouTube Premium)
- Shopping & pakaian
- Kopi / Teh tarik
- Hobi

**Simpanan & Pelaburan (mulai Row 19):**
- ASB / ASM
- KWSP sukarela (i-Saraan)
- Tabung kecemasan
- Pelaburan saham / emas
- SSPN (untuk anak)

### Langkah 4: Masukkan Bajet Bulanan

Dalam Column B (Belanjawan), isi jumlah ikut peruntukan korang. Contoh untuk gaji bersih RM3,000 guna kaedah 50/30/20:

| Kategori | Belanjawan (RM) |
|----------|:--------------:|
| Sewa rumah | 600 |
| Makan & groceries | 500 |
| Bil (elektrik/air/internet) | 250 |
| Pengangkutan | 300 |
| Makan luar | 300 |
| Simpanan ASB | 200 |
| Tabung kecemasan | 150 |

> **Tip:** Guna kaedah [pembahagian gaji 50/30/20](/cara-pembahagian-gaji-bulanan-50-30-20-malaysia/) sebagai panduan asas untuk tetapkan bajet ikut kategori.

### Langkah 5: Formula Auto Kira

Formula paling penting dalam template bajet:

**Jumlah Pendapatan:**
```
=SUM(B2:B4)
```
Letak dalam cell B5 atau mana-mana cell kosong.

**Jumlah Perbelanjaan:**
```
=SUM(B6:B21)
```

**Baki Bulanan:**
```
=B5 - B22
```
Formula ni tolak jumlah perbelanjaan daripada jumlah pendapatan.

**Column Beza (D):**
```
=C2-B2
```
Copy formula ni ke semua row dalam column D. Kalau nilai positif — korang berjaya jimat. Kalau negatif — terlebih belanja.

### Langkah 6: Tracking Perbelanjaan Sebenar

Setiap kali lepas belanja, update Column C (Sebenar). Buat habit ni:

- Lepas bayar bil → update terus
- Hujung minggu → update resit terkumpul
- Paling lewat → setiap malam Ahad

> **Tip:** Guna handphone. Google Sheets ada app mobile — senang update masa tengah menunggu atau lepas checkout.

### Langkah 7: Formatting & Visual

Buat template nampak lebih profesional dengan formatting ni:

1. **Pilih semua cell** → Format → Number → Malaysian Ringgit (RM)
2. **Guna warna:** Hijau untuk nilai positif, Merah untuk negatif
3. **Bold** header row dan total row
4. **Alternating colors:** Format → Alternating colors untuk senang baca
5. **Freeze header row:** View → Freeze → 1 row

### Langkah 8: Tambah Dashboard Ringkas

Guna column F dan G untuk buat dashboard pantas:

- **Peratus simpanan:** `=(B5-B22)/B5*100`
- **Sisa bulan lepas tracking:** Bandingkan baki bulan lepas dengan bulan ni
- **Chart:** Select data → Insert → Chart → Pie chart untuk nampak tabiat berbelanja

Contoh: Kalau gaji RM3,000 dan perbelanjaan RM2,400, peratus simpanan = 20%. Target minimum ialah 10-20%.

## 📋 Template Bajet Siap Guna

Kalau malas nak buat dari mula, korang boleh guna template siap sedia ni:

1. Buka Google Sheets
2. Klik **Template Gallery** (ikon di sudut kanan atas)
3. Scroll ke **Personal** section
4. Pilih **Monthly Budget** atau **Annual Budget**
5. Google akan bagi template dengan formula dah siap

Atau korang boleh lawat [template.net](https://template.net) atau [vertex42.com](https://www.vertex42.com) untuk download template Excel/Sheets bajet percuma — banyak yang dah siap dengan kategori Malaysia.

## 🎯 Cara Tracking Perbelanjaan Dengan Betul

### Setiap Hari

Tracking tak semestinya kena catat setiap sen. Cukup:

- Simpan resit dan catat hujung minggu
- Guna aplikasi nota dalam handphone untuk catat cepat
- Untuk bayaran tunai — simpan resit atau catat dalam Google Keep

### Setiap Minggu

- Bandingkan bajet dengan perbelanjaan sebenar
- Kalau dah terlebih dalam satu kategori, kurangkan kategori lain
- Adjust bajet ikut keperluan — jangan terlalu rigid

### Setiap Bulan

- Review total perbelanjaan
- Update tabung simpanan
- Planning untuk bulan depan
- Check progress target kewangan (kereta baru, deposit rumah, emergency fund)

Guna [Kalkulator Bajet](/kalkulator/pendapatan-percentile/) untuk semak kedudukan gaji korang berbanding pasaran.

## 🛑 Perangkap Yang Kena Elak

### 1. Terlalu Detail Sampai Menekan

Ramai orang buat template dengan 50+ kategori — lepas tu penat tracking, terus give up. Mulakan dengan 10-15 kategori besar je dulu.

### 2. Lupa Tracking Tunai

Belanja tunai paling senang lari. RM10 sini, RM20 sana dalam seminggu boleh jadi RM200. Habit: catat semua transaksi tunai dalam masa 24 jam.

### 3. Gaji Tak Stabil

Kalau gaji tak tetap (freelance, komisen, sales), jangan guna jumlah gaji tertinggi sebagai asas bajet. Guna gaji paling rendah atau average 3 bulan lepas. Baca [panduan bajet pendapatan tidak tetap](/bajet-pendapatan-tidak-tetap-freelance-malaysia/) untuk cara spesifik.

### 4. Tak Update Secara Konsisten

Template bajet paling power pun tak guna kalau tak diupdate. Buat reminder mingguan dalam phone. Tracking 5 minit seminggu lebih baik daripada tracking 1 jam sebulan.

### 5. Lupa Masukkan Belanja Tahunan

Roadtax, insurans kereta, renew passport, cukai pendapatan — ramai lupa nak masukkan belanja tahunan ni dalam bajet. Bahagikan kos tahunan dengan 12 dan masukkan sebagai perbelanjaan bulanan.

## 💡 Tips Bajet Ikut Gaji

### Gaji RM2,000 - RM3,000

| Kategori | Peruntukan | Tips |
|----------|:--------:|------|
| Sewa | 25-30% | Cari bilik sewa bawah RM700 atau rumah kongsi |
| Makan | 20-25% | Masak sendiri sekurang-kurangnya 5 hari seminggu |
| Simpanan | 10-15% | Auto-debit hari gaji masuk |
| Hiburan | 5-10% | Guna free alternatives macam YouTube |

### Gaji RM3,000 - RM5,000

| Kategori | Peruntukan | Tips |
|----------|:--------:|------|
| Sewa | 20-25% | Target bawah RM1,200 |
| Makan | 15-20% | Meal prep hujung minggu |
| Simpanan | 15-20% | ASB, Tabung Haji, atau ASM |
| Pelaburan | 5-10% | Mula dengan unit trust atau emas |

### Gaji RM5,000+

| Kategori | Peruntukan | Tips |
|----------|:--------:|------|
| Komitmen tetap | 30-40% | Jangan increase lifestyle ikut gaji naik |
| Simpanan | 20-30% | Maximakan KWSP, ASB, PRS |
| Pelaburan | 10-15% | Saham, emas, hartanah |
| Derma & sedekah | 5-10% | Jangan lupa zakat pendapatan |

## Kesimpulan

Membuat template bajet bulanan guna Google Sheets adalah langkah pertama paling mudah untuk mula mengawal kewangan. Dengan 15-30 minit setup, korang boleh tracking setiap ringgit yang keluar masuk — dan tahu exact mana duit korang pergi setiap bulan.

Yang penting adalah **konsisten**. Tracking 5 minit setiap minggu lebih baik daripada tracking 1 jam sekali cuba lepas tu terus lupa. Mula hari ni — bukak Google Sheets, buat template, dan mula catat perbelanjaan.

**Baca juga:**
- [Panduan Bajet 50/30/20 Malaysia — Cara Urus Gaji & Simpanan](/cadangan-bajet-50-30-20-di-malaysia/) — kaedah asas pembahagian gaji untuk beginner
- [Cara Pembahagian Gaji Bulanan Ikut Kaedah 50/30/20](/cara-pembahagian-gaji-bulanan-50-30-20-malaysia/) — contoh kiraan lengkap ikut gaji
- [Cara Urus Duit Gaji Bawah RM3000](/urus-duit-gaji-bawah-rm3000/) — tips praktikal untuk gaji permulaan

**Kata Kunci SEO:** template bajet bulanan, google sheets bajet, cara buat template bajet, budgeting template malaysia, tracking perbelanjaan bulanan, spreadsheet bajet percuma, urus gaji google sheets

**Rujukan Rasmi:**
- Google Sheets Help — [Create a budget in Google Sheets](https://support.google.com/a/users/answer/9282728)
- BNM — [MyMoney Sense: Budgeting](https://www.bnm.gov.my/mymoneysense)
- AKPK — [Pengurusan Belanjawan](https://www.akpk.org.my/ms/pengurusan-kewangan)
- Money Compass Malaysia — [Monthly Budget Worksheet](https://www.moneycompass.com.my/budgeting)
