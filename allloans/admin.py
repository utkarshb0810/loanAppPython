from django.contrib import admin

# Register your models here.
from .models import LoanMaster,Analysis,AnalysisLock,Document

admin.site.register(Analysis)
admin.site.register(LoanMaster)
admin.site.register(Document)
admin.site.register(AnalysisLock)