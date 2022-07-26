from django.contrib.auth.decorators import login_required, user_passes_test

admin_login_required = user_passes_test(lambda user: user.is_admin, login_url='/')
def admin_user_required(view_func):
    decorated_view_func = login_required(admin_login_required(view_func))
    return decorated_view_func


# Decorator for Staff login
staff_login_required = user_passes_test(lambda user: user.is_staff, login_url='/')
def staff_user_required(view_func):
    decorated_view_func = login_required(staff_login_required(view_func))
    return decorated_view_func

#  Decorator for student login
student_login_required = user_passes_test(lambda user: user.is_student, login_url='/')
def student_user_required(view_func):
    decorated_view_func = login_required(student_login_required(view_func))
    return decorated_view_func

