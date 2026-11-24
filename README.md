# VidyaSetu Career Institute - Coaching Management ERP

A production-grade, enterprise administrative management application built with **Django** and **MySQL**. Tailored specifically for Indian coaching academies, competitive exam training centers (IIT-JEE, NEET-UG, Foundation, CUET, Commerce/CA), and tuition networks.

The application follows authentic Indian institutional ERP standards with **Indian Rupee (₹) numbering formatting** (Lakhs & Crores), **GST tax invoice generation** under Services Accounting Code (SAC 999293), support for Indian remittance modes (UPI, NEFT/RTGS, IMPS, Cheque/DD), CBSE/ICSE board tracking, and a professional, human-designed administrative interface (strictly devoid of emojis and AI marketing fluff).

---

## Key Enhancements & Indian Economic Context

1. **Indian Currency & Numbering System (`coaching_tags`)**:
   - Custom template filters `{{ value|inr }}` (e.g. `₹1,48,000.00`, `₹75,000.00`) following the Indian comma grouping system (3 digits on the right, followed by 2-digit pairs).
   - Executive compact financial widgets with `{{ value|inr_compact }}` (e.g. `₹7.80 Lakh`, `₹1.25 Cr`).

2. **Official GST Tax Invoices & Fee Receipts**:
   - SAC Code: **999293** (Commercial Training and Coaching Services).
   - Institute GSTIN (`08AAAPV1234F1Z9`), PAN (`AAAPV1234F`), and Kota / Delhi Center branch codes.
   - Comprehensive line-item tuition breakdown:
     1. Base Academic Tuition & Faculty Instruction
     2. Daily Practice Problems (DPP) & Study Kit
     3. All-India Computer Based Test Series (AITS / CBT)
     4. Less: Approved Merit Scholarship / Concession (e.g. VSAT score 95% concession)
     5. Remitted Amount & Net Outstanding Balance
     6. Mode of remittance: UPI (Google Pay, PhonePe, Paytm, BHIM UTR), NEFT/RTGS, Cheque/DD, Cash.
     7. Official institute seal box and authorized signatory sections.
   - Dedicated print stylesheet (`@media print`) for clean browser and PDF printing.

3. **Student Profile & Competitive Exam Tracks**:
   - Roll number identification (e.g., `VSI-2026-101`).
   - Target Examinations: JEE (Main & Advanced), NEET-UG Medical, Class 10 Foundation & Olympiad, CUET-UG, CA Foundation.
   - School Boards: CBSE, ICSE / ISC, State Boards, NIOS.
   - Reservation Categories: General / Open, OBC-NCL, SC, ST, EWS.
   - Aadhaar last 4 digits verification and Parent WhatsApp notification numbers.

4. **Modern, Non-AI Aesthetic**:
   - Deep slate-navy executive top navigation with session indicators.
   - Distinct colored avatar initials chips (`AS`, `AI`, `RG`) for students and mentors.
   - Progress indicators for batch capacity occupancy.
   - Segmented attendance registers with Present (Green), Late (Amber), Absent (Red), and Leave (Blue) status pills.
   - Clean, structured form layouts with field validations and breadcrumb trails.

---

## Tech Stack

- **Backend**: Django 6.1 / Python 3
- **Database Engine**: MySQL (connected via `PyMySQL` driver with `utf8mb4` character set)
- **Frontend / Styling**: Bootstrap 5.3 + Custom enterprise administrative CSS (`portal.css`)
- **Template System**: Django Templating Engine with custom `coaching_tags` library

---

## Quick Setup & Running Guide

### 1. Database Setup in MySQL
Execute `setup_database.sql` in your MySQL console:
```sql
CREATE DATABASE IF NOT EXISTS coaching_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'coaching_user'@'localhost' IDENTIFIED BY 'Coaching@123';
GRANT ALL PRIVILEGES ON coaching_db.* TO 'coaching_user'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and enter your MySQL credentials:
```ini
DB_ENGINE=mysql
DB_NAME=coaching_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```
*(A development fallback to SQLite operates automatically if your local MySQL daemon is not reachable).*

### 3. Migrations & Seed Data
```bash
python3 manage.py migrate
python3 manage.py seed_data
```

### 4. Launch Development Server
```bash
python3 manage.py runserver 0.0.0.0:8000
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

- Default Administrator Login:
  - **Username**: `admin`
  - **Password**: `admin123`
- Django Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
