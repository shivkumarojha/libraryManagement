from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, fullName=None):
        # Create and saves a user with the given email and password
        
        if not email:
            raise ValueError('Users Must have an Email address')
        user = self.model(email=(self.normalize_email(email)), fullName=fullName)
        user.set_password(password)
        user.save(using=(self._db))
        return user
    
    # Create a super user and set the email, name and password for him
    def create_superuser(self, email, password, fullName):
        user = self.create_user(email, password=password, fullName=fullName)
        user.staff = True
        user.admin = True
        user.student = True
        user.save(using=(self._db))
        return user
    
    # Create a staff account
    def create_staffuser(self, email, password, fullName):
        user = self.create_user(email, password=password, fullName=fullName)
        user.staff = True
        user.active = False
        user.save(using=(self._db))
        return user

    # Create a student account
    def create_studentuser(self, email, password, fullName):
        user = self.create_user(email, password=password, fullName=fullName)
        user.student = True
        user.active = False
        user.save(using=(self._db))
        return user
    
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=254, unique=True)
    fullName = models.CharField(max_length=255,
                                null=False,
                                blank=False)
    active = models.BooleanField(default=True)
    admin =models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName']
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.fullName
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_student(self):
        return self.student
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):    
        return self.active
    


class ClassName(models.Model):
    class Meta:
        ordering = ['className']
    className = models.CharField(max_length=100, 
                                  null=False, blank=False, 
                                  unique=True)

    def __str__(self):
        return self.className

class Section(models.Model):
    class Meta:
        ordering = ('className','section')
        # verbose_name_plural = 'sections'
    className = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    section = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f'{self.className} {self.section}'
    
    
# class Subject(models.Model):
#     course = models.ForeignKey(Course,on_delete=models.CASCADE)
#     semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
#     subject = models.CharField(max_length=400,null=False,blank=False)
#     def __str__(self):
#         return self.subject



class StaffProfile(models.Model):
    user = models.OneToOneField((settings.AUTH_USER_MODEL), on_delete=models.CASCADE)

    contactNo = models.CharField(max_length=10, 
                                 null=False, blank=False, 
                                 unique=True)
    
    def __str__(self):
        return self.user.fullName
    
    
    
    
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE)
    fatherName = models.CharField(max_length=50, null=False, blank=False)
    contactNumberRegex = RegexValidator(regex = r"^[0-9]{10}$")
    contactNo = models.CharField(validators = [contactNumberRegex],
                                 max_length=10, null=True, blank=True, 
                                 unique=True)
    className = models.ForeignKey(ClassName, null=True, 
                               on_delete=(models.SET_NULL))
    section = models.ForeignKey(Section, 
                                 null=True, on_delete=(models.SET_NULL))

    def __str__(self):
        return self.user.fullName
    