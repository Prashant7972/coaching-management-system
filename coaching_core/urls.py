from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/new/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Faculty
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/new/', views.faculty_create, name='faculty_create'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('faculty/<int:pk>/edit/', views.faculty_update, name='faculty_update'),
    path('faculty/<int:pk>/delete/', views.faculty_delete, name='faculty_delete'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Batches
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/new/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('batches/<int:pk>/edit/', views.batch_update, name='batch_update'),
    path('batches/<int:pk>/delete/', views.batch_delete, name='batch_delete'),

    # Enrollments
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/new/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/delete/', views.enrollment_delete, name='enrollment_delete'),

    # Attendance
    path('attendance/', views.attendance_overview, name='attendance_overview'),
    path('attendance/batch/<int:batch_id>/mark/', views.mark_attendance, name='mark_attendance'),

    # Fees & Billing
    path('fees/', views.payment_list, name='payment_list'),
    path('fees/new/', views.payment_create, name='payment_create'),
    path('fees/receipt/<int:pk>/', views.payment_receipt, name='payment_receipt'),

    # Tests
    path('tests/', views.test_list, name='test_list'),
    path('tests/new/', views.test_create, name='test_create'),
    path('tests/<int:pk>/', views.test_detail, name='test_detail'),
    path('tests/<int:pk>/marks/', views.enter_marks, name='enter_marks'),

    # Notices
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/new/', views.notice_create, name='notice_create'),
    path('notices/<int:pk>/edit/', views.notice_update, name='notice_update'),
    path('notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
]
