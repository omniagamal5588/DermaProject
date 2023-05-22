from django.urls import path,include
from pharmacy.views import PharmacyRegistrationView,PharmacyLoginView,RestPasswordView,PharmacyProfileView,MedicineDetailes,MedicineInfo,OffersDetailes

urlpatterns=[

  path('pharmacyRegister/',PharmacyRegistrationView.as_view(),name='PharmacyRegister'),
  path('pharmacyLogin/',PharmacyLoginView.as_view(),name='login'),
  path('pharmacyProfile/', PharmacyProfileView.as_view(), name='profile'),
  path('resetPassword/', RestPasswordView.as_view(), name='resetPassword'),
  path('medicine/',MedicineDetailes.as_view(),name='medicine'),
  path('med/<int:id>/',MedicineInfo.as_view()),
  path('offers/',OffersDetailes.as_view(),name='offers'),
  ]