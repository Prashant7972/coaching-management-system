from django.contrib import admin
from .models import (
    Student, Faculty, Course, Batch, Enrollment,
    Attendance, FeePayment, Test, TestResult, Notice
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'phone', 'email', 'status', 'enrollment_date')
    list_filter = ('status', 'gender', 'enrollment_date')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'phone', 'parent_name')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'first_name', 'last_name', 'qualification', 'specialization', 'status')
    list_filter = ('status', 'joining_date')
    search_fields = ('faculty_id', 'first_name', 'last_name', 'email', 'specialization')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'duration_weeks', 'fee_amount', 'status')
    list_filter = ('status',)
    search_fields = ('course_code', 'name')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_code', 'name', 'course', 'faculty', 'start_date', 'max_capacity', 'status')
    list_filter = ('status', 'course', 'start_date')
    search_fields = ('batch_code', 'name', 'room_number')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'batch', 'agreed_fee', 'discount', 'status', 'enrollment_date')
    list_filter = ('status', 'batch', 'enrollment_date')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id', 'batch__batch_code')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'batch', 'student', 'status')
    list_filter = ('date', 'status', 'batch')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id', 'batch__batch_code')


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'enrollment', 'amount', 'payment_date', 'payment_method', 'received_by')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('receipt_number', 'enrollment__student__first_name', 'enrollment__student__last_name', 'transaction_reference')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'batch', 'test_date', 'total_marks', 'passing_marks')
    list_filter = ('test_date', 'batch')
    search_fields = ('title', 'batch__batch_code')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'student', 'marks_obtained', 'grade')
    list_filter = ('test__batch', 'test')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id', 'test__title')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_group', 'priority', 'published_date', 'is_active')
    list_filter = ('target_group', 'priority', 'is_active', 'published_date')
    search_fields = ('title', 'content')
