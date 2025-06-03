from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .models import LoanMaster, Document, Analysis, AnalysisLock
from .forms import DocumentForm
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import time




def upload_document(request, loan_id):
    loan = get_object_or_404(LoanMaster, pk=loan_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.loan = loan
            pdf_file = request.FILES['file_path']
            loan_folder = os.path.join(settings.MEDIA_ROOT, f'loan_{loan.loan_id}')
            if not os.path.exists(loan_folder):
                os.makedirs(loan_folder)
            fs = FileSystemStorage(location=loan_folder)
            filename = fs.save(pdf_file.name, pdf_file)
            file_url = fs.url(filename)
            document.file_path = os.path.join(f'loan_{loan.loan_id}', filename)  # Save the relative file path to the document
            document.save()
            return redirect('loan_detail', loan_id=loan.loan_id)
    else:
        form = DocumentForm()
    return render(request, 'allloans/upload_document.html', {'form': form, 'loan': loan})

def start_analysis(request, loan_id):
    loan = get_object_or_404(LoanMaster, pk=loan_id)
    try:
        lock = AnalysisLock.objects.create(loan=loan, lock_acquired_time=timezone.now())
    except:
        return HttpResponse("Analysis is already in progress for this loan.")

    documents=Document.objects.filter(loan=loan, analysis__isnull=True)
    analysis_start_time= timezone.now()
    analysis_result = 'Analysis rtimeesult'
    
    analysis_end_time = timezone.now()
    
    analysis = Analysis.objects.create(
        loan=loan,
        start_time=analysis_start_time,
        end_time=analysis_end_time,  
        status='Completed',
        output_file= analysis_result  
    )
    
    time.sleep(60)
    


    Document.objects.filter(loan=loan, analysis__isnull=True).update(analysis=analysis)
    
    

   
    lock.delete()

    return HttpResponse("Analysis completed.")

def loan_detail(request, loan_id):
    loan = get_object_or_404(LoanMaster, pk=loan_id)
    documents = Document.objects.filter(loan=loan)
    return render(request, 'allloans/loan_detail.html', {'loan': loan, 'documents': documents})

def display_loans(request):
    loans = LoanMaster.objects.all()
    return render(request, 'allloans/display_loans.html', {'loans': loans})


def loan_document(request, loan_id):
    loan = get_object_or_404(LoanMaster, pk=loan_id)
    documents = Document.objects.filter(loan=loan)
    return render(request, 'allloans/loan_document.html', {'loan': loan, 'documents': documents})