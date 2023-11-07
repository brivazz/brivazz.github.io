from django.urls import path

from .views import FileAPIView, FileUploadedAPIView

urlpatterns = [path('upload/', FileAPIView.as_view()), path('files/', FileUploadedAPIView.as_view())]
