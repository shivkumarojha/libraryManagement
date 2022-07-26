from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClassName, Section, StudentProfile, StaffProfile 

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','fullName', 'admin', 'staff', 'student', 'active')
    list_editable = ('active',)
    list_filter = ('admin', 'staff','student','active')
    search_fields = ('fullName__startswith',)
admin.site.register(User, UserAdmin)

class ClassNameAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClassName, ClassNameAdmin)
admin.site.register(Section)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_userName','fatherName', 'contactNo', 'className', 'section')
    def get_userName(self, obj):
        return obj.user.fullName
    get_userName.short_description = 'Student Name' # Short description for column name in admin
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(StaffProfile)