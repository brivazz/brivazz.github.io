from django.urls import path

from .views import FileAPIView, FileUploadedAPIView

app_name = 'api'

urlpatterns = [path('upload/', FileAPIView.as_view()), path('files/', FileUploadedAPIView.as_view())]
