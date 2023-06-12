from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

#  Custom User Manager
class UserManager(BaseUserManager):
   def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

#  Custom User Model
class Pharmacy(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name=models.CharField(max_length=200, verbose_name='Name')
  location=models.CharField(max_length=200, verbose_name='Location')
  phone_number=models.CharField(max_length=15, verbose_name='Phone number')
  description=models.CharField(max_length=255,verbose_name='Description')
  pharmacy_image=models.ImageField(upload_to='pharmacy_pictures', null=True ,verbose_name='Pharmacy Image')
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  #REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email


#Subscription Class
class Subscription(models.Model):
    price=models.IntegerField(null=False)
    subscription_type = models.CharField( max_length=255,null=False)
    duration=models.IntegerField(null=False)




class Subscription_Pharmacy(models.Model):
    pharmacy_id=models.ForeignKey(Pharmacy,on_delete=models.CASCADE)
    subscription_id=models.ForeignKey(Subscription,on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)


class Medicine(models.Model):
  serial_number=models.CharField(max_length=255)
  medicine_name=models.CharField(max_length=255)
  medicine_description=models.TextField()
  medicine_price=models.DecimalField(max_digits=6, decimal_places=2)
  medicine_image=models.ImageField(upload_to='medicine_pictures', null=True ,verbose_name='Medicine Image')
  pharmacy_id=models.CharField(Pharmacy,max_length=255,default=True)


class Pharmacy_medicine(models.Model):
  pharmacy_id=models.ForeignKey(Pharmacy,on_delete=models.CASCADE)
  medicine_id=models.ForeignKey(Medicine,on_delete=models.CASCADE)
  offer = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])



#   def __str__(self):
#     return self.medicine_name
  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
