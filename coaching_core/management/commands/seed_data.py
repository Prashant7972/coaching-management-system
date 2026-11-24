from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import datetime

from coaching_core.models import (
    Student, Faculty, Course, Batch, Enrollment,
    Attendance, FeePayment, Test, TestResult, Notice
)


class Command(BaseCommand):
    help = 'Seeds database with realistic Indian coaching academy data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Populating VidyaSetu Career Institute data..."))

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@vidyasetu.internal', 'admin123')
            self.stdout.write(self.style.SUCCESS("Superuser verified: admin / admin123"))

        # 2. Indian Faculty Mentors & Professors
        faculty_data = [
            {
                'faculty_id': 'FAC-PHY-101',
                'first_name': 'Prof. Arvind',
                'last_name': 'Mishra',
                'email': 'arvind.mishra@vidyasetu.internal',
                'phone': '+91 98290 41001',
                'qualification': 'Ph.D. Theoretical Physics (IIT Delhi), M.Sc. (Gold Medalist)',
                'specialization': 'Classical Mechanics, Electrodynamics & Wave Optics (JEE Adv)',
                'joining_date': datetime.date(2022, 5, 1),
                'salary_monthly': Decimal('195000.00'),
                'status': 'ACTIVE',
                'notes': 'Ex-Senior Faculty Kota; Head of Department - Physics.',
            },
            {
                'faculty_id': 'FAC-MTH-102',
                'first_name': 'Er. Rajeshwar',
                'last_name': 'Rao',
                'email': 'rajeshwar.rao@vidyasetu.internal',
                'phone': '+91 98290 41002',
                'qualification': 'B.Tech Computer Science (IIT Bombay)',
                'specialization': 'Calculus, Coordinate Geometry & Combinatorics (JEE Adv)',
                'joining_date': datetime.date(2023, 1, 10),
                'salary_monthly': Decimal('185000.00'),
                'status': 'ACTIVE',
                'notes': '14+ years of mentoring AIR Top 100 rankers in IIT-JEE.',
            },
            {
                'faculty_id': 'FAC-CHM-103',
                'first_name': 'Dr. Meenakshi',
                'last_name': 'Sundaram',
                'email': 'm.sundaram@vidyasetu.internal',
                'phone': '+91 98290 41003',
                'qualification': 'Ph.D. Organic Chemistry (IISc Bangalore)',
                'specialization': 'Organic Reaction Mechanisms, Stereochemistry & Polymers',
                'joining_date': datetime.date(2023, 6, 15),
                'salary_monthly': Decimal('170000.00'),
                'status': 'ACTIVE',
                'notes': 'Author of Competitive Organic Chemistry Problem Set book.',
            },
            {
                'faculty_id': 'FAC-BIO-104',
                'first_name': 'Prof. Sneha',
                'last_name': 'Mukherjee',
                'email': 'sneha.mukherjee@vidyasetu.internal',
                'phone': '+91 98290 41004',
                'qualification': 'M.Sc. Human Genetics (AIIMS New Delhi)',
                'specialization': 'Cell Biology, Genetics & Human Physiology (NEET-UG)',
                'joining_date': datetime.date(2024, 2, 1),
                'salary_monthly': Decimal('165000.00'),
                'status': 'ACTIVE',
                'notes': 'NEET Academic Cell Lead; NCERT syllabus reviewer.',
            },
            {
                'faculty_id': 'FAC-CHM-105',
                'first_name': 'Er. Alok Kumar',
                'last_name': 'Bansal',
                'email': 'alok.bansal@vidyasetu.internal',
                'phone': '+91 98290 41005',
                'qualification': 'B.Tech Chemical Engineering (IIT Roorkee)',
                'specialization': 'Thermodynamics, Chemical Kinetics & Coordination Compounds',
                'joining_date': datetime.date(2024, 4, 1),
                'salary_monthly': Decimal('160000.00'),
                'status': 'ACTIVE',
                'notes': 'Specialist in Physical Chemistry numeric speed drills.',
            },
            {
                'faculty_id': 'FAC-MTH-106',
                'first_name': 'Dr. Sunita',
                'last_name': 'Deshpande',
                'email': 'sunita.deshpande@vidyasetu.internal',
                'phone': '+91 98290 41006',
                'qualification': 'Ph.D. Applied Mathematics (Delhi University)',
                'specialization': 'Vectors, 3D Geometry & Probability Theory',
                'joining_date': datetime.date(2024, 7, 1),
                'salary_monthly': Decimal('155000.00'),
                'status': 'ACTIVE',
                'notes': 'Expert in Board + Competitive Integrated Coaching.',
            },
        ]

        faculty_objs = {}
        for f in faculty_data:
            obj, _ = Faculty.objects.update_or_create(faculty_id=f['faculty_id'], defaults=f)
            faculty_objs[f['faculty_id']] = obj

        # 3. Premier Indian Coaching Programs
        course_data = [
            {
                'course_code': 'JEE-PINNACLE',
                'name': 'JEE (Main & Advanced) Two-Year Pinnacle Program',
                'description': 'Targeted preparation for Class 11 & 12 students covering Complete Physics, Chemistry & Mathematics syllabus with Daily Practice Problems (DPP) and All-India Test Series (AITS).',
                'duration_weeks': 48,
                'fee_amount': Decimal('148000.00'),
                'status': 'ACTIVE',
            },
            {
                'course_code': 'NEET-SUPER30',
                'name': 'NEET-UG Medical Achievers Batch',
                'description': 'Comprehensive medical entrance coaching for 12th Passed / Dropper students focusing on NCERT line-by-line mastery in Physics, Chemistry, Botany, and Zoology with weekly mock tests.',
                'duration_weeks': 40,
                'fee_amount': Decimal('135000.00'),
                'status': 'ACTIVE',
            },
            {
                'course_code': 'FND-OLYMPIAD',
                'name': 'Class 10 CBSE Board + NTSE / Olympiad Foundation',
                'description': 'Integrated school board coaching combined with advance conceptual foundation for IJSO, NTSE, and PRMO competitive mathematics and sciences.',
                'duration_weeks': 36,
                'fee_amount': Decimal('68000.00'),
                'status': 'ACTIVE',
            },
            {
                'course_code': 'CUET-INTENSIVE',
                'name': 'CUET-UG Central Universities Entrance Crash Program',
                'description': 'Crash coaching program covering General Test, Domain Subjects (PCM/PCB/Commerce), and English Language Comprehension for central university admissions.',
                'duration_weeks': 16,
                'fee_amount': Decimal('42000.00'),
                'status': 'ACTIVE',
            },
        ]

        course_objs = {}
        for c in course_data:
            obj, _ = Course.objects.update_or_create(course_code=c['course_code'], defaults=c)
            course_objs[c['course_code']] = obj

        # 4. Batches in Kota & Delhi Centers
        batch_data = [
            {
                'batch_code': 'KOTA-JEE-26A',
                'name': 'JEE Advanced Morning Cohort Alpha',
                'course': course_objs['JEE-PINNACLE'],
                'faculty': faculty_objs['FAC-PHY-101'],
                'start_date': datetime.date(2026, 8, 1),
                'end_date': datetime.date(2027, 4, 30),
                'schedule_days': 'Mon, Wed, Fri, Sat',
                'start_time': datetime.time(8, 0),
                'end_time': datetime.time(12, 30),
                'room_number': 'AryaBhatta Lecture Hall 101',
                'max_capacity': 35,
                'status': 'ONGOING',
            },
            {
                'batch_code': 'DELHI-NEET-26B',
                'name': 'NEET Medical Droppers Target Batch',
                'course': course_objs['NEET-SUPER30'],
                'faculty': faculty_objs['FAC-BIO-104'],
                'start_date': datetime.date(2026, 8, 10),
                'end_date': datetime.date(2027, 4, 15),
                'schedule_days': 'Mon, Tue, Wed, Thu, Fri',
                'start_time': datetime.time(9, 0),
                'end_time': datetime.time(13, 30),
                'room_number': 'Charak Medical Annex (Room 204)',
                'max_capacity': 30,
                'status': 'ONGOING',
            },
            {
                'batch_code': 'KOTA-FND-26C',
                'name': 'Class 10 Foundation & Olympiad Evening',
                'course': course_objs['FND-OLYMPIAD'],
                'faculty': faculty_objs['FAC-MTH-102'],
                'start_date': datetime.date(2026, 9, 1),
                'end_date': datetime.date(2027, 2, 28),
                'schedule_days': 'Tue, Thu, Sat',
                'start_time': datetime.time(17, 0),
                'end_time': datetime.time(19, 30),
                'room_number': 'Ramanujan Classroom 104',
                'max_capacity': 25,
                'status': 'ONGOING',
            },
            {
                'batch_code': 'ONLINE-CUET-26D',
                'name': 'CUET Hybrid Weekend Intensive',
                'course': course_objs['CUET-INTENSIVE'],
                'faculty': faculty_objs['FAC-CHM-103'],
                'start_date': datetime.date(2026, 10, 1),
                'end_date': datetime.date(2027, 2, 15),
                'schedule_days': 'Sat, Sun',
                'start_time': datetime.time(10, 0),
                'end_time': datetime.time(14, 0),
                'room_number': 'Digital Studio Room 3',
                'max_capacity': 40,
                'status': 'ONGOING',
            },
        ]

        batch_objs = {}
        for b in batch_data:
            obj, _ = Batch.objects.update_or_create(batch_code=b['batch_code'], defaults=b)
            batch_objs[b['batch_code']] = obj

        # 5. Indian Students with Authentic Names
        students_data = [
            ('VSI-2026-101', 'Aarav', 'Sharma', 'M', '2008-05-14', 'aarav.sharma@example.in', '+91 98291 10001', 'Sunil Sharma', '+91 98291 10002', 'CBSE', 'JEE (Main & Advanced)', 'GEN', '4120', 'Plot 42, Mahaveer Nagar III, Kota, Rajasthan'),
            ('VSI-2026-102', 'Ananya', 'Iyer', 'F', '2008-09-22', 'ananya.iyer@example.in', '+91 98291 10003', 'V. S. Iyer', '+91 98291 10004', 'CBSE', 'NEET-UG Medical', 'GEN', '7891', 'Flat 302, Green Glen Residency, Indiranagar, Bengaluru'),
            ('VSI-2026-103', 'Rohan', 'Verma', 'M', '2007-11-04', 'rohan.verma@example.in', '+91 98291 10005', 'Dinesh Verma', '+91 98291 10006', 'STATE', 'JEE (Main & Advanced)', 'OBC', '6312', 'House 14B, Civil Lines, Kanpur, Uttar Pradesh'),
            ('VSI-2026-104', 'Priya', 'Nair', 'F', '2008-03-18', 'priya.nair@example.in', '+91 98291 10007', 'K. K. Nair', '+91 98291 10008', 'ICSE', 'NEET-UG Medical', 'GEN', '9021', 'Apt 12, Palm Meadows, Kochi, Kerala'),
            ('VSI-2026-105', 'Ishan', 'Gupta', 'M', '2008-07-29', 'ishan.gupta@example.in', '+91 98291 10009', 'Ramesh Gupta', '+91 98291 10010', 'CBSE', 'JEE (Main & Advanced)', 'GEN', '3349', 'Sector 15, Vasundhara, Ghaziabad, Delhi NCR'),
            ('VSI-2026-106', 'Tanvi', 'Deshmukh', 'F', '2009-01-15', 'tanvi.d@example.in', '+91 98291 10011', 'Suresh Deshmukh', '+91 98291 10012', 'STATE', 'Class 10 NTSE / Board', 'GEN', '8812', '55 Shivaji Nagar, Pune, Maharashtra'),
            ('VSI-2026-107', 'Aditya', 'Patel', 'M', '2008-04-03', 'aditya.p@example.in', '+91 98291 10013', 'Bhavin Patel', '+91 98291 10014', 'CBSE', 'JEE (Main & Advanced)', 'OBC', '1244', '21 Shanti Sadan, CG Road, Ahmedabad, Gujarat'),
            ('VSI-2026-108', 'Meera', 'Choudhary', 'F', '2007-12-11', 'meera.c@example.in', '+91 98291 10015', 'Balwan Choudhary', '+91 98291 10016', 'STATE', 'NEET-UG Medical', 'OBC', '5523', 'Ward 8, Mandore Road, Jodhpur, Rajasthan'),
            ('VSI-2026-109', 'Vikram', 'Rawat', 'M', '2008-08-09', 'vikram.r@example.in', '+91 98291 10017', 'Harish Rawat', '+91 98291 10018', 'CBSE', 'CUET-UG Entrance', 'EWS', '9012', 'Near Clock Tower, Dehradun, Uttarakhand'),
            ('VSI-2026-110', 'Kavya', 'Reddy', 'F', '2008-06-25', 'kavya.reddy@example.in', '+91 98291 10019', 'M. N. Reddy', '+91 98291 10020', 'STATE', 'JEE (Main & Advanced)', 'GEN', '7731', 'Banjara Hills, Road No 10, Hyderabad, Telangana'),
            ('VSI-2026-111', 'Siddharth', 'Joshi', 'M', '2008-02-19', 'siddharth.j@example.in', '+91 98291 10021', 'Mahesh Joshi', '+91 98291 10022', 'CBSE', 'JEE (Main & Advanced)', 'GEN', '2219', '18 Navrangpura, Ahmedabad, Gujarat'),
            ('VSI-2026-112', 'Diya', 'Mukherjee', 'F', '2008-10-12', 'diya.m@example.in', '+91 98291 10023', 'Subir Mukherjee', '+91 98291 10024', 'ICSE', 'NEET-UG Medical', 'GEN', '6601', 'Salt Lake Sector V, Kolkata, West Bengal'),
        ]

        student_objs = []
        for s in students_data:
            stu, _ = Student.objects.update_or_create(
                student_id=s[0],
                defaults={
                    'first_name': s[1],
                    'last_name': s[2],
                    'gender': s[3],
                    'date_of_birth': datetime.date.fromisoformat(s[4]),
                    'email': s[5],
                    'phone': s[6],
                    'parent_name': s[7],
                    'parent_phone': s[8],
                    'board': s[9],
                    'target_exam': s[10],
                    'category': s[11],
                    'aadhaar_last_four': s[12],
                    'address': s[13],
                    'enrollment_date': datetime.date(2026, 8, 1),
                    'status': 'ACTIVE',
                    'notes': f'Registered for academic session 2026-27. Target: {s[10]}.',
                }
            )
            student_objs.append(stu)

        # 6. Enrollments with Indian Fee Structures & Scholarships
        enrollments_plan = [
            # JEE Morning Batch (Kota)
            (student_objs[0], batch_objs['KOTA-JEE-26A'], Decimal('148000.00'), Decimal('25000.00'), 'VSAT Merit Rank 44 Concession'),
            (student_objs[2], batch_objs['KOTA-JEE-26A'], Decimal('148000.00'), Decimal('15000.00'), 'Early Bird Concession'),
            (student_objs[4], batch_objs['KOTA-JEE-26A'], Decimal('148000.00'), Decimal('0.00'), 'Standard fee installment plan'),
            (student_objs[6], batch_objs['KOTA-JEE-26A'], Decimal('148000.00'), Decimal('10000.00'), 'Sibling enrollment discount'),
            (student_objs[9], batch_objs['KOTA-JEE-26A'], Decimal('148000.00'), Decimal('35000.00'), 'National Talent Search (NTSE) Scholar 25%'),
            (student_objs[10], batch_objs['KOTA-JEE-26A'], Decimal('148000.00'), Decimal('18000.00'), 'Merit scholarship on Class 10th 97.4% marks'),

            # NEET Droppers Batch (Delhi)
            (student_objs[1], batch_objs['DELHI-NEET-26B'], Decimal('135000.00'), Decimal('20000.00'), 'Class 12th Board 96% Merit Award'),
            (student_objs[3], batch_objs['DELHI-NEET-26B'], Decimal('135000.00'), Decimal('0.00'), 'Standard two-installment plan'),
            (student_objs[7], batch_objs['DELHI-NEET-26B'], Decimal('135000.00'), Decimal('15000.00'), 'State quota defense scholarship'),
            (student_objs[11], batch_objs['DELHI-NEET-26B'], Decimal('135000.00'), Decimal('25000.00'), 'KVPY Fellow Scholarship'),

            # Foundation Class 10 (Kota)
            (student_objs[5], batch_objs['KOTA-FND-26C'], Decimal('68000.00'), Decimal('8000.00'), 'Junior Science Olympiad Qualifier'),

            # CUET Weekend (Online)
            (student_objs[8], batch_objs['ONLINE-CUET-26D'], Decimal('42000.00'), Decimal('5000.00'), 'EWS concession approved by directorate'),
        ]

        enrollment_objs = []
        for stu, bth, fee, disc, rem in enrollments_plan:
            enr, _ = Enrollment.objects.update_or_create(
                student=stu,
                batch=bth,
                defaults={
                    'agreed_fee': fee,
                    'discount': disc,
                    'status': 'ENROLLED',
                    'enrollment_date': bth.start_date,
                    'remarks': rem,
                }
            )
            enrollment_objs.append(enr)

        # 7. Fee Payments with Indian Banking Modes (UPI, NEFT, RTGS, Cheque, Cash)
        payments_data = [
            (enrollment_objs[0], Decimal('75000.00'), datetime.date(2026, 8, 2), 'VSI-INV-202608-0101', 'UPI', 'UPI-992019482910-HDFC'),
            (enrollment_objs[0], Decimal('48000.00'), datetime.date(2026, 10, 5), 'VSI-INV-202610-0102', 'NEFT_RTGS', 'NEFT-SBIN0029104'),
            (enrollment_objs[1], Decimal('80000.00'), datetime.date(2026, 8, 3), 'VSI-INV-202608-0103', 'UPI', 'UPI-884920194829-ICICI'),
            (enrollment_objs[2], Decimal('75000.00'), datetime.date(2026, 8, 4), 'VSI-INV-202608-0104', 'CHEQUE_DD', 'CHQ-SBI-440192'),
            (enrollment_objs[3], Decimal('70000.00'), datetime.date(2026, 8, 5), 'VSI-INV-202608-0105', 'UPI', 'UPI-774920194821-PAYTM'),
            (enrollment_objs[4], Decimal('113000.00'), datetime.date(2026, 8, 6), 'VSI-INV-202608-0106', 'NEFT_RTGS', 'RTGS-PUNB0049201'),
            (enrollment_objs[5], Decimal('65000.00'), datetime.date(2026, 8, 12), 'VSI-INV-202608-0107', 'UPI', 'UPI-334920194829-GPay'),
            (enrollment_objs[6], Decimal('70000.00'), datetime.date(2026, 8, 15), 'VSI-INV-202608-0108', 'CASH', 'COUNTER-CASH-RCPT-44'),
            (enrollment_objs[7], Decimal('60000.00'), datetime.date(2026, 8, 16), 'VSI-INV-202608-0109', 'CHEQUE_DD', 'CHQ-BOI-992810'),
            (enrollment_objs[8], Decimal('35000.00'), datetime.date(2026, 9, 2), 'VSI-INV-202609-0110', 'UPI', 'UPI-554920194829-PhonePe'),
            (enrollment_objs[9], Decimal('37000.00'), datetime.date(2026, 10, 2), 'VSI-INV-202610-0111', 'UPI', 'UPI-114920194829-BHIM'),
            (enrollment_objs[10], Decimal('75000.00'), datetime.date(2026, 8, 18), 'VSI-INV-202608-0112', 'UPI', 'UPI-884920194833-KOTAK'),
        ]

        for enr, amt, dt, rec, met, ref in payments_data:
            FeePayment.objects.update_or_create(
                receipt_number=rec,
                defaults={
                    'enrollment': enr,
                    'amount': amt,
                    'payment_date': dt,
                    'payment_method': met,
                    'transaction_reference': ref,
                    'received_by': 'Finance Counter 01 (Kota Central)',
                    'remarks': 'Term Tuition Fee + Study Material Kit (SAC 999293)',
                }
            )

        # 8. Attendance in Indian Session
        jee_batch = batch_objs['KOTA-JEE-26A']
        jee_enrs = Enrollment.objects.filter(batch=jee_batch, status='ENROLLED')

        sample_dates = [
            datetime.date(2026, 11, 16),
            datetime.date(2026, 11, 18),
            datetime.date(2026, 11, 20),
            datetime.date(2026, 11, 23),
            timezone.localdate(),
        ]

        for dt in sample_dates:
            for idx, enr in enumerate(jee_enrs):
                if idx == 1 and dt == sample_dates[1]:
                    st = 'ABSENT'
                    rem = 'Leave application submitted - Medical appointment'
                elif idx == 3 and dt == sample_dates[3]:
                    st = 'LATE'
                    rem = 'Hostel bus transit delay 15 mins'
                else:
                    st = 'PRESENT'
                    rem = ''

                Attendance.objects.update_or_create(
                    batch=jee_batch,
                    student=enr.student,
                    date=dt,
                    defaults={'status': st, 'remarks': rem}
                )

        # 9. All India Minor & Major Tests
        test_1, _ = Test.objects.update_or_create(
            batch=jee_batch,
            title='All-India Minor Test 04: Rotational Motion & Center of Mass',
            defaults={
                'test_date': datetime.date(2026, 10, 28),
                'total_marks': 300,
                'passing_marks': 105,
                'description': 'NTA JEE Advanced pattern: Single Choice (+3/-1), Multiple Correct (+4/-2), Numerical Value (+3/0).',
            }
        )

        scores = [246.0, 268.0, 192.5, 178.0, 285.0, 212.0]
        grades = ['A', 'A+', 'B', 'B', 'A+', 'A']
        for enr, sc, gd in zip(jee_enrs, scores, grades):
            TestResult.objects.update_or_create(
                test=test_1,
                student=enr.student,
                defaults={
                    'marks_obtained': Decimal(str(sc)),
                    'grade': gd,
                    'remarks': 'Commendable problem-solving speed in multi-correct section.',
                }
            )

        # Upcoming Test
        Test.objects.update_or_create(
            batch=jee_batch,
            title='All-India Major Test 01: Complete Mechanics & Thermodynamics',
            defaults={
                'test_date': timezone.localdate() + datetime.timedelta(days=5),
                'total_marks': 300,
                'passing_marks': 110,
                'description': 'Comprehensive syllabus revision simulation as per latest NTA guidelines.',
            }
        )

        neet_batch = batch_objs['DELHI-NEET-26B']
        Test.objects.update_or_create(
            batch=neet_batch,
            title='NEET Full Mock 03: Human Genetics & Biological Classification',
            defaults={
                'test_date': timezone.localdate() + datetime.timedelta(days=3),
                'total_marks': 720,
                'passing_marks': 360,
                'description': 'NCERT Line-by-Line assessment; 180 questions with OMR simulation.',
            }
        )

        # 10. Official Institutional Circulars / Notices
        notices_data = [
            {
                'title': 'National Testing Agency (NTA) JEE Main 2027 Session I Online Form Guidance Desk',
                'target_group': 'ALL',
                'priority': 'HIGH',
                'published_date': timezone.localdate() - datetime.timedelta(days=1),
                'content': 'A dedicated document verification and online application facilitation counter has been set up at Academic Block Room 102. Students must bring Class 10 Marksheet, Aadhaar Card, and Category Certificate (OBC-NCL/EWS issued after April 1).',
                'is_active': True,
            },
            {
                'title': 'Term-II Fee Installment Reminder for Academic Year 2026-27',
                'target_group': 'PARENTS',
                'priority': 'URGENT',
                'published_date': timezone.localdate(),
                'content': 'Parents are kindly requested to remit the second term tuition fee installment on or before the 10th of next month via the student portal UPI gateway, Net Banking (NEFT/RTGS), or at the central cash counter. Official GST tax invoices will be issued immediately upon clearance.',
                'is_active': True,
            },
            {
                'title': 'Central Library & Silent Self-Study Hours Extended for Board & Entrance Aspirants',
                'target_group': 'STUDENTS',
                'priority': 'NORMAL',
                'published_date': timezone.localdate() - datetime.timedelta(days=4),
                'content': 'In view of upcoming pre-board and minor assessments, the Ramanujan Central Reading Room will remain open until 10:30 PM on weekdays. Wi-Fi and reference library catalogs will be accessible with student RFID identity cards.',
                'is_active': True,
            },
            {
                'title': 'Faculty Academic Review & OMR Result Analysis Meeting',
                'target_group': 'FACULTY',
                'priority': 'HIGH',
                'published_date': timezone.localdate() - datetime.timedelta(days=2),
                'content': 'All HODs and subject faculties are requested to attend the monthly academic performance and error-analysis review this Thursday at 4:30 PM in the Director Boardroom.',
                'is_active': True,
            },
        ]

        for n in notices_data:
            Notice.objects.update_or_create(title=n['title'], defaults=n)

        self.stdout.write(self.style.SUCCESS("VidyaSetu Career Institute data seeded successfully!"))
