
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('loan/<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('loan/<int:loan_id>/upload/', views.upload_document, name='upload_document'),
    path('loan/<int:loan_id>/start_analysis/', views.start_analysis, name='start_analysis'),
    path('loans/', views.display_loans, name='display_loans'),
    path('admin/', admin.site.urls),
    path('loan/<int:loan_id>/documents/', views.loan_document, name='loan_document'), 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)