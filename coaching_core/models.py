from django.db import models
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
        ('SUSPENDED', 'Suspended'),
    ]

    BOARD_CHOICES = [
        ('CBSE', 'CBSE (Central Board)'),
        ('ICSE', 'ICSE / ISC'),
        ('STATE', 'State Board'),
        ('OTHER', 'Other / NIOS'),
    ]

    CATEGORY_CHOICES = [
        ('GEN', 'General / Open'),
        ('OBC', 'OBC-NCL'),
        ('SC', 'Scheduled Caste (SC)'),
        ('ST', 'Scheduled Tribe (ST)'),
        ('EWS', 'Economically Weaker Section (EWS)'),
    ]

    student_id = models.CharField(max_length=20, unique=True, verbose_name="Enrollment / Roll No")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, verbose_name="Student Contact / WhatsApp")
    parent_name = models.CharField(max_length=100, verbose_name="Parent / Guardian Name")
    parent_phone = models.CharField(max_length=20, verbose_name="Parent WhatsApp / Phone")
    board = models.CharField(max_length=10, choices=BOARD_CHOICES, default='CBSE', verbose_name="Academic Board")
    target_exam = models.CharField(max_length=60, default='JEE (Main & Advanced)', verbose_name="Target Examination")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='GEN', verbose_name="Category")
    aadhaar_last_four = models.CharField(max_length=4, blank=True, verbose_name="Aadhaar (Last 4 Digits)")
    address = models.TextField(blank=True, verbose_name="Permanent / Local Address")
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True, verbose_name="Internal Counselor / Academic Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        fn = self.first_name[0].upper() if self.first_name else ''
        ln = self.last_name[0].upper() if self.last_name else ''
        return f"{fn}{ln}" or "ST"

    @property
    def total_outstanding_fees(self):
        total = Decimal('0.00')
        for enrollment in self.enrollments.filter(status='ENROLLED'):
            total += enrollment.balance_due
        return total


class Faculty(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('RESIGNED', 'Resigned'),
    ]

    faculty_id = models.CharField(max_length=20, unique=True, verbose_name="Faculty Code / ID")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    qualification = models.CharField(max_length=120, help_text="e.g. B.Tech IIT Delhi, M.Sc. Physics (Gold Medalist)")
    specialization = models.CharField(max_length=120, help_text="e.g. JEE Advanced Physics, Physical Chemistry")
    joining_date = models.DateField(default=timezone.now)
    salary_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Monthly Remuneration (INR)")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['faculty_id']
        verbose_name = "Faculty Member"
        verbose_name_plural = "Faculty Members"

    def __str__(self):
        return f"{self.faculty_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        fn = self.first_name[0].upper() if self.first_name else ''
        ln = self.last_name[0].upper() if self.last_name else ''
        return f"{fn}{ln}" or "FC"


class Course(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    course_code = models.CharField(max_length=20, unique=True, verbose_name="Program Code")
    name = models.CharField(max_length=150, verbose_name="Course Program Name")
    description = models.TextField(blank=True)
    duration_weeks = models.PositiveIntegerField(default=24, verbose_name="Duration (Weeks)")
    fee_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Standard Course Fee (INR)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course_code']
        verbose_name = "Course Program"
        verbose_name_plural = "Course Programs"

    def __str__(self):
        return f"{self.course_code}: {self.name}"


class Batch(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    batch_code = models.CharField(max_length=30, unique=True, verbose_name="Batch Code")
    name = models.CharField(max_length=150, verbose_name="Batch Cohort Name")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    faculty = models.ForeignKey(
        Faculty, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='batches',
        verbose_name="Lead Faculty Mentor"
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    schedule_days = models.CharField(
        max_length=100, 
        help_text="Class days, e.g. Mon, Wed, Fri"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="e.g. Ramanujan Hall, AryaBhatta Lab, Room 102"
    )
    max_capacity = models.PositiveIntegerField(default=40)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='UPCOMING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date', 'batch_code']
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    def __str__(self):
        return f"{self.batch_code} - {self.name}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='ENROLLED').count()

    @property
    def seats_available(self):
        count = self.enrolled_count
        avail = self.max_capacity - count
        return max(avail, 0)

    @property
    def occupancy_percentage(self):
        if self.max_capacity > 0:
            return round((self.enrolled_count / self.max_capacity) * 100, 1)
        return 0


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(default=timezone.now)
    agreed_fee = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Gross Program Fee (INR)")
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="Scholarship / Concession (INR)")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ENROLLED')
    remarks = models.TextField(blank=True, help_text="Scholarship criteria or installment approval note")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enrollment_date']
        constraints = [
            models.UniqueConstraint(fields=['student', 'batch'], name='unique_student_batch_enrollment')
        ]
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student.full_name} -> {self.batch.batch_code}"

    @property
    def net_fee(self):
        return self.agreed_fee - self.discount

    @property
    def total_paid(self):
        total = self.payments.aggregate(total=Sum('amount'))['total']
        return total or Decimal('0.00')

    @property
    def balance_due(self):
        balance = self.net_fee - self.total_paid
        return max(balance, Decimal('0.00'))

    @property
    def payment_status(self):
        paid = self.total_paid
        net = self.net_fee
        if paid >= net and net > 0:
            return 'PAID'
        elif paid > 0:
            return 'PARTIAL'
        return 'PENDING'


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late Arrival'),
        ('EXCUSED', 'Leave Sanctioned'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date', 'student__last_name']
        constraints = [
            models.UniqueConstraint(fields=['batch', 'student', 'date'], name='unique_batch_student_date_attendance')
        ]
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return f"{self.date} | {self.batch.batch_code} | {self.student.full_name}: {self.status}"


class FeePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI (Google Pay / PhonePe / Paytm / BHIM)'),
        ('NEFT_RTGS', 'NEFT / RTGS Net Banking'),
        ('IMPS', 'IMPS Instant Remittance'),
        ('CHEQUE_DD', 'Cheque / Demand Draft (DD)'),
        ('CASH', 'Cash at Center Counter'),
        ('CARD', 'Debit / Credit Card (POS)'),
    ]

    receipt_number = models.CharField(max_length=30, unique=True, verbose_name="Tax Invoice / Receipt No")
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Amount Received (INR)")
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='UPI')
    transaction_reference = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="UPI UTR, Cheque/DD No, or Bank Reference Number"
    )
    received_by = models.CharField(max_length=100, default="Suresh Meena (Accounts Officer, Kota Center)")
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']
        verbose_name = "Fee Payment"
        verbose_name_plural = "Fee Payments"

    def __str__(self):
        return f"{self.receipt_number} - {self.enrollment.student.full_name} ({self.amount})"


class Test(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=150, verbose_name="Test / Minor Exam Title")
    test_date = models.DateField(default=timezone.now)
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    description = models.TextField(blank=True, verbose_name="Syllabus Topics Covered")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-test_date']
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return f"{self.batch.batch_code} - {self.title} ({self.test_date})"

    @property
    def submissions_count(self):
        return self.results.count()


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-marks_obtained']
        constraints = [
            models.UniqueConstraint(fields=['test', 'student'], name='unique_test_student_result')
        ]
        verbose_name = "Test Result"
        verbose_name_plural = "Test Results"

    def __str__(self):
        return f"{self.test.title} | {self.student.full_name}: {self.marks_obtained}/{self.test.total_marks}"

    @property
    def percentage(self):
        if self.test.total_marks > 0:
            return round((self.marks_obtained / Decimal(self.test.total_marks)) * Decimal('100'), 1)
        return Decimal('0.0')

    @property
    def is_passed(self):
        return self.marks_obtained >= Decimal(self.test.passing_marks)


class Notice(models.Model):
    TARGET_CHOICES = [
        ('ALL', 'All Members & Students'),
        ('STUDENTS', 'Students Only'),
        ('FACULTY', 'Faculty Only'),
        ('PARENTS', 'Parents & Guardians'),
    ]

    PRIORITY_CHOICES = [
        ('NORMAL', 'Standard Notice'),
        ('HIGH', 'Important Notification'),
        ('URGENT', 'Urgent Circular'),
    ]

    title = models.CharField(max_length=200)
    target_group = models.CharField(max_length=15, choices=TARGET_CHOICES, default='ALL')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='NORMAL')
    published_date = models.DateField(default=timezone.now)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Notice"
        verbose_name_plural = "Notices"

    def __str__(self):
        return f"{self.published_date} | {self.title}"
