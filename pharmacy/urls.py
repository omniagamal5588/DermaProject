from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
#from . import views
from pharmacy.views import *

urlpatterns=[

  path('register/',PharmacyRegistrationView.as_view(),name='PharmacyRegister'),
  path('login/',PharmacyLoginView.as_view(),name='login'),
  path('profile/', PharmacyProfileView.as_view(), name='profile'),
  path('editProfile/', PharmacyProfileView.as_view(), name='profile'),
  path('resetPassword/', RestPasswordView.as_view(), name='resetPassword'),
  path('forgetPassword/', ForgetPasswordView.as_view(), name='forgetPassword'),
  path('medicines/',MedicineDetailes.as_view(),name='medicine'),
  path('medicines/<int:id>/',MedicineInfo.as_view()),
  path('medicines/<int:id>/offers/',OffersDetailes.as_view(),name='offers'),
  path('submitSubscription/',submitSubscriptionView.as_view()),
  path('logout/',LogOutView.as_view(),name='logout'),
  path('SubscribePlan/',SubscriptionPlanView.as_view(),name='subscertionType'),
  # path('viewSubPlan/',SubscriptionPlanView.as_view(),name='subscertionType'),
  path('medicinesUserView/',MedicineView.as_view(),name='medicineView'),
  path('offersUserView/',OfferView.as_view(),name='offersView')
]
