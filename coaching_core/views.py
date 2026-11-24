from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Q, Count
from django.utils import timezone
from decimal import Decimal
import datetime

from .models import (
    Student, Faculty, Course, Batch, Enrollment,
    Attendance, FeePayment, Test, TestResult, Notice
)
from .forms import (
    StudentForm, FacultyForm, CourseForm, BatchForm,
    EnrollmentForm, FeePaymentForm, TestForm, NoticeForm
)


# ==========================================
# DASHBOARD
# ==========================================

def dashboard(request):
    today = timezone.localdate()

    total_students = Student.objects.filter(status='ACTIVE').count()
    total_faculty = Faculty.objects.filter(status='ACTIVE').count()
    ongoing_batches = Batch.objects.filter(status='ONGOING').count()

    # Fee metrics
    total_collected = FeePayment.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Calculate pending fees across active enrollments
    active_enrollments = Enrollment.objects.filter(status='ENROLLED')
    total_agreed = active_enrollments.aggregate(total=Sum('agreed_fee'))['total'] or Decimal('0.00')
    total_discount = active_enrollments.aggregate(total=Sum('discount'))['total'] or Decimal('0.00')
    net_receivable = total_agreed - total_discount
    pending_fees = max(net_receivable - total_collected, Decimal('0.00'))

    # Today's attendance
    today_attendance = Attendance.objects.filter(date=today)
    att_present = today_attendance.filter(status='PRESENT').count()
    att_absent = today_attendance.filter(status='ABSENT').count()
    att_late = today_attendance.filter(status='LATE').count()
    att_total = today_attendance.count()

    recent_enrollments = Enrollment.objects.select_related('student', 'batch').order_by('-created_at')[:6]
    recent_payments = FeePayment.objects.select_related('enrollment__student', 'enrollment__batch').order_by('-payment_date', '-created_at')[:5]
    upcoming_tests = Test.objects.select_related('batch').filter(test_date__gte=today).order_by('test_date')[:4]
    active_notices = Notice.objects.filter(is_active=True).order_by('-priority', '-published_date')[:5]

    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'ongoing_batches': ongoing_batches,
        'total_collected': total_collected,
        'pending_fees': pending_fees,
        'att_present': att_present,
        'att_absent': att_absent,
        'att_late': att_late,
        'att_total': att_total,
        'recent_enrollments': recent_enrollments,
        'recent_payments': recent_payments,
        'upcoming_tests': upcoming_tests,
        'active_notices': active_notices,
        'today': today,
    }
    return render(request, 'dashboard.html', context)


# ==========================================
# STUDENTS
# ==========================================

def student_list(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    if status_filter:
        students = students.filter(status=status_filter)

    students = students.order_by('student_id')

    context = {
        'students': students,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'students/student_list.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student.full_name} ({student.student_id}) registered successfully.")
            return redirect('student_detail', pk=student.pk)
    else:
        # Suggest next student ID
        last_student = Student.objects.order_by('-id').first()
        next_num = (last_student.id + 1) if last_student else 1
        suggested_id = f"VSI-{timezone.now().year}-{next_num:03d}"
        form = StudentForm(initial={'student_id': suggested_id})

    return render(request, 'students/student_form.html', {'form': form, 'title': 'Register New Student'})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('batch', 'batch__course').all()
    
    # Calculate attendance summary for this student
    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(student=student, status='PRESENT').count()
    attendance_rate = round((present_classes / total_classes * 100), 1) if total_classes > 0 else 0

    # Test results
    test_results = student.test_results.select_related('test', 'test__batch').order_by('-test__test_date')

    context = {
        'student': student,
        'enrollments': enrollments,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'attendance_rate': attendance_rate,
        'test_results': test_results,
    }
    return render(request, 'students/student_detail.html', context)


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student record for {student.full_name} updated.")
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {'form': form, 'title': f'Edit Student: {student.full_name}'})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f"Student record for {name} was deleted.")
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {
        'object': student,
        'cancel_url': 'student_detail',
        'cancel_pk': student.pk,
        'item_type': 'Student Record'
    })


# ==========================================
# FACULTY
# ==========================================

def faculty_list(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    faculty_members = Faculty.objects.all()

    if query:
        faculty_members = faculty_members.filter(
            Q(faculty_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(email__icontains=query)
        )

    if status_filter:
        faculty_members = faculty_members.filter(status=status_filter)

    context = {
        'faculty_members': faculty_members,
        'query': query,
        'status_filter': status_filter,
    }
    return render(request, 'faculty/faculty_list.html', context)


def faculty_create(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            faculty = form.save()
            messages.success(request, f"Faculty {faculty.full_name} added successfully.")
            return redirect('faculty_detail', pk=faculty.pk)
    else:
        last_faculty = Faculty.objects.order_by('-id').first()
        next_num = (last_faculty.id + 1) if last_faculty else 1
        suggested_id = f"FAC-VSI-{next_num:03d}"
        form = FacultyForm(initial={'faculty_id': suggested_id})

    return render(request, 'faculty/faculty_form.html', {'form': form, 'title': 'Add Faculty Member'})


def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    batches = faculty.batches.select_related('course').all()
    return render(request, 'faculty/faculty_detail.html', {'faculty': faculty, 'batches': batches})


def faculty_update(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, f"Faculty {faculty.full_name} updated successfully.")
            return redirect('faculty_detail', pk=faculty.pk)
    else:
        form = FacultyForm(instance=faculty)

    return render(request, 'faculty/faculty_form.html', {'form': form, 'title': f'Edit Faculty: {faculty.full_name}'})


def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        name = faculty.full_name
        faculty.delete()
        messages.success(request, f"Faculty record for {name} removed.")
        return redirect('faculty_list')
    return render(request, 'confirm_delete.html', {
        'object': faculty,
        'cancel_url': 'faculty_detail',
        'cancel_pk': faculty.pk,
        'item_type': 'Faculty Member'
    })


# ==========================================
# COURSES & BATCHES
# ==========================================

def course_list(request):
    courses = Course.objects.annotate(batch_count=Count('batches')).order_by('course_code')
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course {course.course_code}: {course.name} created.")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Add New Course'})


def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course {course.course_code} updated.")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': f'Edit Course: {course.course_code}'})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f"Course {name} deleted.")
        return redirect('course_list')
    return render(request, 'confirm_delete.html', {
        'object': course,
        'cancel_url': 'course_list',
        'cancel_pk': None,
        'item_type': 'Course'
    })


def batch_list(request):
    batches = Batch.objects.select_related('course', 'faculty').order_by('-start_date')
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        batches = batches.filter(status=status_filter)
    return render(request, 'courses/batch_list.html', {'batches': batches, 'status_filter': status_filter})


def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f"Batch {batch.batch_code} created successfully.")
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm()
    return render(request, 'courses/batch_form.html', {'form': form, 'title': 'Create New Batch'})


def batch_detail(request, pk):
    batch = get_object_or_404(Batch.objects.select_related('course', 'faculty'), pk=pk)
    enrollments = batch.enrollments.select_related('student').order_by('student__student_id')
    tests = batch.tests.order_by('-test_date')
    recent_attendance_dates = (
        Attendance.objects.filter(batch=batch)
        .values('date')
        .distinct()
        .order_by('-date')[:5]
    )

    context = {
        'batch': batch,
        'enrollments': enrollments,
        'tests': tests,
        'recent_attendance_dates': recent_attendance_dates,
    }
    return render(request, 'courses/batch_detail.html', context)


def batch_update(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, f"Batch {batch.batch_code} updated.")
            return redirect('batch_detail', pk=batch.pk)
    else:
        form = BatchForm(instance=batch)
    return render(request, 'courses/batch_form.html', {'form': form, 'title': f'Edit Batch: {batch.batch_code}'})


def batch_delete(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        code = batch.batch_code
        batch.delete()
        messages.success(request, f"Batch {code} deleted.")
        return redirect('batch_list')
    return render(request, 'confirm_delete.html', {
        'object': batch,
        'cancel_url': 'batch_detail',
        'cancel_pk': batch.pk,
        'item_type': 'Batch'
    })


# ==========================================
# ENROLLMENTS
# ==========================================

def enrollment_list(request):
    batch_filter = request.GET.get('batch', '')
    status_filter = request.GET.get('status', '')

    enrollments = Enrollment.objects.select_related('student', 'batch', 'batch__course').order_by('-enrollment_date')

    if batch_filter:
        enrollments = enrollments.filter(batch_id=batch_filter)
    if status_filter:
        enrollments = enrollments.filter(status=status_filter)

    batches = Batch.objects.filter(status__in=['UPCOMING', 'ONGOING']).order_by('batch_code')

    context = {
        'enrollments': enrollments,
        'batches': batches,
        'batch_filter': batch_filter,
        'status_filter': status_filter,
    }
    return render(request, 'enrollments/enrollment_list.html', context)


def enrollment_create(request):
    batch_id = request.GET.get('batch_id')
    student_id = request.GET.get('student_id')

    initial_data = {}
    if batch_id:
        batch = get_object_or_404(Batch, pk=batch_id)
        initial_data['batch'] = batch
        initial_data['agreed_fee'] = batch.course.fee_amount
    if student_id:
        student = get_object_or_404(Student, pk=student_id)
        initial_data['student'] = student

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            messages.success(
                request,
                f"Student {enrollment.student.full_name} enrolled in {enrollment.batch.batch_code}."
            )
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(initial=initial_data)

    return render(request, 'enrollments/enrollment_form.html', {'form': form, 'title': 'Enroll Student in Batch'})


def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, "Enrollment record removed.")
        return redirect('enrollment_list')
    return render(request, 'confirm_delete.html', {
        'object': enrollment,
        'cancel_url': 'enrollment_list',
        'cancel_pk': None,
        'item_type': 'Enrollment'
    })


# ==========================================
# ATTENDANCE
# ==========================================

def attendance_overview(request):
    today = timezone.localdate()
    selected_date_str = request.GET.get('date', today.strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.date.fromisoformat(selected_date_str)
    except ValueError:
        selected_date = today

    batches = Batch.objects.filter(status__in=['UPCOMING', 'ONGOING']).order_by('batch_code')

    # Gather stats per batch for selected date
    batch_stats = []
    for b in batches:
        records = Attendance.objects.filter(batch=b, date=selected_date)
        total_enrolled = b.enrolled_count
        marked = records.count()
        present = records.filter(status='PRESENT').count()
        absent = records.filter(status='ABSENT').count()
        late = records.filter(status='LATE').count()
        batch_stats.append({
            'batch': b,
            'total_enrolled': total_enrolled,
            'marked': marked,
            'present': present,
            'absent': absent,
            'late': late,
            'is_fully_marked': (marked >= total_enrolled and total_enrolled > 0),
        })

    context = {
        'selected_date': selected_date,
        'batch_stats': batch_stats,
    }
    return render(request, 'attendance/attendance_overview.html', context)


def mark_attendance(request, batch_id):
    batch = get_object_or_404(Batch, pk=batch_id)
    today = timezone.localdate()
    date_str = request.GET.get('date', today.strftime('%Y-%m-%d'))
    try:
        att_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        att_date = today

    enrollments = batch.enrollments.filter(status='ENROLLED').select_related('student').order_by('student__student_id')

    if request.method == 'POST':
        att_date_post = request.POST.get('attendance_date', str(att_date))
        try:
            target_date = datetime.date.fromisoformat(att_date_post)
        except ValueError:
            target_date = att_date

        for enrollment in enrollments:
            student = enrollment.student
            status_val = request.POST.get(f'status_{student.id}', 'PRESENT')
            remarks_val = request.POST.get(f'remarks_{student.id}', '').strip()

            Attendance.objects.update_or_create(
                batch=batch,
                student=student,
                date=target_date,
                defaults={
                    'status': status_val,
                    'remarks': remarks_val,
                }
            )

        messages.success(request, f"Attendance for batch {batch.batch_code} on {target_date} saved.")
        return redirect('attendance_overview')

    # Existing records for initial state
    existing_records = {
        att.student_id: att
        for att in Attendance.objects.filter(batch=batch, date=att_date)
    }

    student_roster = []
    for enr in enrollments:
        att_record = existing_records.get(enr.student.id)
        current_status = att_record.status if att_record else 'PRESENT'
        current_remarks = att_record.remarks if att_record else ''
        student_roster.append({
            'student': enr.student,
            'current_status': current_status,
            'current_remarks': current_remarks,
        })

    context = {
        'batch': batch,
        'att_date': att_date,
        'student_roster': student_roster,
    }
    return render(request, 'attendance/mark_attendance.html', context)


# ==========================================
# FEES & BILLING
# ==========================================

def payment_list(request):
    payments = FeePayment.objects.select_related('enrollment__student', 'enrollment__batch').order_by('-payment_date', '-created_at')

    query = request.GET.get('q', '').strip()
    method = request.GET.get('method', '').strip()

    if query:
        payments = payments.filter(
            Q(receipt_number__icontains=query) |
            Q(enrollment__student__first_name__icontains=query) |
            Q(enrollment__student__last_name__icontains=query) |
            Q(enrollment__student__student_id__icontains=query) |
            Q(transaction_reference__icontains=query)
        )

    if method:
        payments = payments.filter(payment_method=method)

    context = {
        'payments': payments,
        'query': query,
        'method': method,
    }
    return render(request, 'fees/payment_list.html', context)


def payment_create(request):
    enrollment_id = request.GET.get('enrollment_id')
    initial_data = {}

    if enrollment_id:
        enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
        initial_data['enrollment'] = enrollment
        initial_data['amount'] = enrollment.balance_due

    # Generate sequential receipt number
    now_stamp = timezone.now().strftime('%Y%m')
    last_receipt = FeePayment.objects.order_by('-id').first()
    next_seq = (last_receipt.id + 1) if last_receipt else 1
    initial_data['receipt_number'] = f"VSI-TAX-{now_stamp}-{next_seq:04d}"
    initial_data['received_by'] = "Suresh Meena (Accounts Officer, Kota Center)"

    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"Fee payment receipt {payment.receipt_number} issued.")
            return redirect('payment_receipt', pk=payment.pk)
    else:
        form = FeePaymentForm(initial=initial_data)

    return render(request, 'fees/payment_form.html', {'form': form, 'title': 'Issue Fee Receipt / Record Payment'})


def payment_receipt(request, pk):
    payment = get_object_or_404(
        FeePayment.objects.select_related(
            'enrollment__student',
            'enrollment__batch',
            'enrollment__batch__course'
        ),
        pk=pk
    )
    return render(request, 'fees/receipt.html', {'payment': payment})


# ==========================================
# TESTS & MARKS
# ==========================================

def test_list(request):
    batch_filter = request.GET.get('batch', '')
    tests = Test.objects.select_related('batch', 'batch__course').order_by('-test_date')

    if batch_filter:
        tests = tests.filter(batch_id=batch_filter)

    batches = Batch.objects.all().order_by('batch_code')
    return render(request, 'tests/test_list.html', {'tests': tests, 'batches': batches, 'batch_filter': batch_filter})


def test_create(request):
    batch_id = request.GET.get('batch_id')
    initial_data = {}
    if batch_id:
        initial_data['batch'] = get_object_or_404(Batch, pk=batch_id)

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save()
            messages.success(request, f"Test '{test.title}' scheduled for batch {test.batch.batch_code}.")
            return redirect('test_detail', pk=test.pk)
    else:
        form = TestForm(initial=initial_data)

    return render(request, 'tests/test_form.html', {'form': form, 'title': 'Schedule New Test / Assessment'})


def test_detail(request, pk):
    test = get_object_or_404(Test.objects.select_related('batch', 'batch__course'), pk=pk)
    results = test.results.select_related('student').order_by('-marks_obtained')

    # Compute summary
    count = results.count()
    if count > 0:
        avg_marks = round(sum(r.marks_obtained for r in results) / count, 1)
        passed_count = sum(1 for r in results if r.is_passed)
        pass_percentage = round((passed_count / count) * 100, 1)
    else:
        avg_marks = 0
        pass_percentage = 0
        passed_count = 0

    context = {
        'test': test,
        'results': results,
        'submissions_count': count,
        'avg_marks': avg_marks,
        'passed_count': passed_count,
        'pass_percentage': pass_percentage,
    }
    return render(request, 'tests/test_detail.html', context)


def enter_marks(request, pk):
    test = get_object_or_404(Test.objects.select_related('batch'), pk=pk)
    enrollments = test.batch.enrollments.filter(status='ENROLLED').select_related('student').order_by('student__student_id')

    if request.method == 'POST':
        for enrollment in enrollments:
            student = enrollment.student
            marks_raw = request.POST.get(f'marks_{student.id}', '').strip()
            grade_val = request.POST.get(f'grade_{student.id}', '').strip()
            remarks_val = request.POST.get(f'remarks_{student.id}', '').strip()

            if marks_raw != '':
                try:
                    marks_dec = Decimal(marks_raw)
                    TestResult.objects.update_or_create(
                        test=test,
                        student=student,
                        defaults={
                            'marks_obtained': marks_dec,
                            'grade': grade_val,
                            'remarks': remarks_val,
                        }
                    )
                except Exception:
                    pass

        messages.success(request, f"Test marks updated for '{test.title}'.")
        return redirect('test_detail', pk=test.pk)

    existing_results = {r.student_id: r for r in test.results.all()}
    roster = []
    for enr in enrollments:
        res = existing_results.get(enr.student.id)
        roster.append({
            'student': enr.student,
            'marks': res.marks_obtained if res else '',
            'grade': res.grade if res else '',
            'remarks': res.remarks if res else '',
        })

    context = {
        'test': test,
        'roster': roster,
    }
    return render(request, 'tests/enter_marks.html', context)


# ==========================================
# NOTICES
# ==========================================

def notice_list(request):
    notices = Notice.objects.all().order_by('-published_date')
    return render(request, 'notices/notice_list.html', {'notices': notices})


def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save()
            messages.success(request, f"Notice '{notice.title}' published.")
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'notices/notice_form.html', {'form': form, 'title': 'Publish New Notice'})


def notice_update(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, f"Notice updated.")
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'notices/notice_form.html', {'form': form, 'title': f'Edit Notice: {notice.title}'})


def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice removed.")
        return redirect('notice_list')
    return render(request, 'confirm_delete.html', {
        'object': notice,
        'cancel_url': 'notice_list',
        'cancel_pk': None,
        'item_type': 'Notice'
    })
