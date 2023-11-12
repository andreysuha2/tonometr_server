from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from diary import views

urlpatterns = [ 
               path('records/', views.DiaryRecordList.as_view()),
               path('records/<int:pk>', views.DiaryRecordDetails.as_view())
            ]