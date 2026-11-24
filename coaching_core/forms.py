from django import forms
from .models import (
    Student, Faculty, Course, Batch, Enrollment,
    Attendance, FeePayment, Test, TestResult, Notice
)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'gender', 'date_of_birth',
            'email', 'phone', 'parent_name', 'parent_phone',
            'board', 'target_exam', 'category', 'aadhaar_last_four',
            'address', 'enrollment_date', 'status', 'notes'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. VSI-2026-101'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Aarav'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sharma'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'aarav.sharma@example.in'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +91 98291 10001'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sunil Sharma / Sunita Sharma'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +91 98291 10002'}),
            'board': forms.Select(attrs={'class': 'form-select'}),
            'target_exam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. JEE (Main & Advanced) 2027'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'aadhaar_last_four': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXX', 'maxlength': '4'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Permanent / Local Residential Address'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Counseling notes, test series rank, or background remarks'}),
        }


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            'faculty_id', 'first_name', 'last_name', 'email', 'phone',
            'qualification', 'specialization', 'joining_date', 'salary_monthly',
            'status', 'notes'
        ]
        widgets = {
            'faculty_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FAC-PHY-101'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Prof. Arvind'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mishra'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'arvind.mishra@vidyasetu.internal'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98290 41001'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ph.D. Physics (IIT Delhi), M.Sc. (Gold Medalist)'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mechanics & Modern Physics (JEE Adv)'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_monthly': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00', 'placeholder': 'e.g. 195000'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'name', 'description', 'duration_weeks', 'fee_amount', 'status']
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. JEE-2YR-ADV'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. JEE (Main & Advanced) Two-Year Pinnacle Program'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed syllabus coverage and test schedules'}),
            'duration_weeks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'fee_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00', 'placeholder': 'e.g. 145000'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = [
            'batch_code', 'name', 'course', 'faculty', 'start_date', 'end_date',
            'schedule_days', 'start_time', 'end_time', 'room_number',
            'max_capacity', 'status'
        ]
        widgets = {
            'batch_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. KOTA-JEE-MORN-A1'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Top 40 Super Achievers (Morning)'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'schedule_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mon, Wed, Fri or Daily'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ramanujan Hall (Room 101)'}),
            'max_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'batch', 'enrollment_date', 'agreed_fee', 'discount', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'agreed_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00', 'placeholder': 'Total gross fee'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00', 'placeholder': 'Scholarship concession'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. 20% Fee Concession via VidyaSetu Talent Exam'}),
        }


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = [
            'receipt_number', 'enrollment', 'amount', 'payment_date',
            'payment_method', 'transaction_reference', 'received_by', 'remarks'
        ]
        widgets = {
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. VSI-TAX-2026-001'}),
            'enrollment': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '1.00', 'placeholder': 'Amount in INR'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UPI UTR No / Cheque No / NEFT Ref'}),
            'received_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Suresh Meena (Accounts Officer, Kota)'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. 1st Installment towards Tuition & Study Materials (SAC 999293)'}),
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['batch', 'title', 'test_date', 'total_marks', 'passing_marks', 'description']
        widgets = {
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. All-India Minor Test 03: Rotational Dynamics'}),
            'test_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Portion & negative marking scheme (-1 for incorrect)'}),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'target_group', 'priority', 'published_date', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Heading'}),
            'target_group': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Official circular or notification text'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
