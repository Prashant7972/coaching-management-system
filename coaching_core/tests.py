from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
import datetime

from .models import (
    Student, Faculty, Course, Batch, Enrollment,
    Attendance, FeePayment, Test, TestResult, Notice
)


class CoachingSystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Faculty
        self.faculty = Faculty.objects.create(
            faculty_id='FAC-901',
            first_name='Prof. Arvind',
            last_name='Mishra',
            email='arvind.mishra@vidyasetu.internal',
            phone='+91 98290 41001',
            qualification='Ph.D. Physics (IIT Delhi)',
            specialization='Electrodynamics & Optics',
            joining_date=datetime.date(2025, 1, 1),
            salary_monthly=Decimal('180000.00'),
            status='ACTIVE'
        )

        # Course
        self.course = Course.objects.create(
            course_code='CS-501',
            name='Algorithms & Data Structures',
            duration_weeks=16,
            fee_amount=Decimal('45000.00'),
            status='ACTIVE'
        )

        # Batch
        self.batch = Batch.objects.create(
            batch_code='B26-CS-ALG',
            name='Algorithms Batch Alpha',
            course=self.course,
            faculty=self.faculty,
            start_date=datetime.date(2026, 9, 1),
            schedule_days='Mon, Wed',
            start_time=datetime.time(10, 0),
            end_time=datetime.time(12, 0),
            max_capacity=20,
            status='ONGOING'
        )

        # Student
        self.student = Student.objects.create(
            student_id='VSI-2026-901',
            first_name='Aarav',
            last_name='Sharma',
            gender='M',
            email='aarav.sharma@example.in',
            phone='+91 98291 10001',
            parent_name='Sunil Sharma',
            parent_phone='+91 98291 10002',
            board='CBSE',
            target_exam='JEE (Main & Advanced)',
            category='GEN',
            aadhaar_last_four='4120',
            enrollment_date=datetime.date(2026, 9, 1),
            status='ACTIVE'
        )

        # Enrollment
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            batch=self.batch,
            agreed_fee=Decimal('45000.00'),
            discount=Decimal('5000.00'),
            status='ENROLLED'
        )

        # Payment
        self.payment = FeePayment.objects.create(
            receipt_number='VSI-TAX-TEST-001',
            enrollment=self.enrollment,
            amount=Decimal('20000.00'),
            payment_date=datetime.date(2026, 9, 5),
            payment_method='UPI',
            transaction_reference='UPI-992019482910-HDFC',
            received_by='Suresh Meena (Accounts Officer, Kota Center)'
        )

        # Test
        self.test = Test.objects.create(
            batch=self.batch,
            title='Sorting Algorithms Quiz',
            test_date=datetime.date(2026, 9, 15),
            total_marks=50,
            passing_marks=20
        )

        # Notice
        self.notice = Notice.objects.create(
            title='Orientation Briefing for New Batches',
            content='Welcome to all candidates enrolled in the upcoming academic session.',
            target_group='ALL',
            priority='NORMAL'
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'VidyaSetu Career Institute')
        self.assertContains(response, 'Active Enrollments')

    def test_student_views(self):
        # List
        res_list = self.client.get(reverse('student_list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Aarav Sharma')

        # Detail
        res_detail = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, 'VSI-2026-901')

    def test_faculty_views(self):
        res_list = self.client.get(reverse('faculty_list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Prof. Arvind Mishra')

        res_detail = self.client.get(reverse('faculty_detail', args=[self.faculty.pk]))
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, 'FAC-901')

    def test_course_and_batch_views(self):
        res_courses = self.client.get(reverse('course_list'))
        self.assertEqual(res_courses.status_code, 200)
        self.assertContains(res_courses, 'Algorithms &amp; Data Structures')

        res_batches = self.client.get(reverse('batch_list'))
        self.assertEqual(res_batches.status_code, 200)
        self.assertContains(res_batches, 'B26-CS-ALG')

        res_batch_detail = self.client.get(reverse('batch_detail', args=[self.batch.pk]))
        self.assertEqual(res_batch_detail.status_code, 200)
        self.assertContains(res_batch_detail, 'Algorithms Batch Alpha')

    def test_fee_receipt_view(self):
        res_receipt = self.client.get(reverse('payment_receipt', args=[self.payment.pk]))
        self.assertEqual(res_receipt.status_code, 200)
        self.assertContains(res_receipt, 'VSI-TAX-TEST-001')
        self.assertContains(res_receipt, '20,000.00')

    def test_attendance_marking(self):
        today_str = timezone.localdate().strftime('%Y-%m-%d')
        post_data = {
            'attendance_date': today_str,
            f'status_{self.student.id}': 'PRESENT',
            f'remarks_{self.student.id}': 'Arrived on time',
        }
        res = self.client.post(
            reverse('mark_attendance', args=[self.batch.pk]),
            post_data,
            follow=True
        )
        self.assertEqual(res.status_code, 200)
        att_record = Attendance.objects.filter(
            batch=self.batch,
            student=self.student,
            date=timezone.localdate()
        ).first()
        self.assertIsNotNone(att_record)
        self.assertEqual(att_record.status, 'PRESENT')
        self.assertEqual(att_record.remarks, 'Arrived on time')

    def test_marks_entry(self):
        post_data = {
            f'marks_{self.student.id}': '44.50',
            f'grade_{self.student.id}': 'A',
            f'remarks_{self.student.id}': 'Excellent performance',
        }
        res = self.client.post(
            reverse('enter_marks', args=[self.test.pk]),
            post_data,
            follow=True
        )
        self.assertEqual(res.status_code, 200)
        result = TestResult.objects.filter(test=self.test, student=self.student).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.marks_obtained, Decimal('44.50'))
        self.assertEqual(result.grade, 'A')
        self.assertTrue(result.is_passed)
