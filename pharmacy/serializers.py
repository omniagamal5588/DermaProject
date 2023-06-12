from rest_framework import serializers
from pharmacy.models import Pharmacy,Medicine,Pharmacy_medicine,Subscription
# from . import utils
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError


#PharmacyRegisterSerializer
class PharmacyRegistrationSerializer(serializers.ModelSerializer):

  class Meta:
    model =Pharmacy
    fields=['name','email', 'phone_number', 'location', 'password','description','pharmacy_image']
    extra_kwargs={
      'password':{'write_only':True}
    }

# Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    #password2 = attrs.get('password2')


    email = attrs.get('email', None)
    if Pharmacy.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email')})
    return super().validate(attrs)
  def create(self, validate_data):
    return Pharmacy.objects.create_user(**validate_data)

#login pharmacy serializer
class PharmacyLoginSeraializer(serializers.ModelSerializer):
  class Meta:
    model=Pharmacy
    fields=['email','password']


#Pharmacy Profile
class PharmacyProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Pharmacy
    fields = ['id', 'email', 'name','location','phone_number','pharmacy_image','description']


class ResetPasswordSerializerPharma(serializers.Serializer):
  old_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  new_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    model = Pharmacy
    fields = ['email','old_password', 'new_password']

#MedicineSerializer
class MedicineSerializer(serializers.ModelSerializer):
  class Meta:
    model=Medicine
    fields=['id','serial_number','medicine_name','medicine_description','medicine_price', 'medicine_image']

#Phamacy_medicine
class PharmacyMedicineSerializer(serializers.ModelSerializer):
  pharmacy_id = PharmacyProfileSerializer(read_only=True, allow_null=True)
  medicine_id = MedicineSerializer(read_only=True, allow_null=True)
  class Meta:
    model=Pharmacy_medicine
    # fields= "__all__"
    fields = ['id', 'pharmacy_id', 'medicine_id', 'offer']


#SubscriptionPlanSerializer
class SubscriptionPlanSerializer(serializers.ModelSerializer):
  class Meta:
    model=Subscription
    fields=['id','price','subscription_type','duration']



