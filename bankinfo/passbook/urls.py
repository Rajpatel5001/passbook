from django.urls import path

from .views import passbookVIEW,postentry,exportUSerApiView

app_name = 'passbook'

urlpatterns = [
    path('user/',passbookVIEW.as_view(),name="passbookurl"),
    path('user/<str>',passbookVIEW.as_view(),name="passbookurl"),
    path('usercreate/',postentry.as_view(),name="passbookentry"),
    path('export/', exportUSerApiView.as_view(), name='exportuserscsv'),
]