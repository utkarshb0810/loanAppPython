from django.db import models


class LoanMaster(models.Model):
    loan_id = models.AutoField(primary_key=True)
    pan_number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.loan_id}"


class Analysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(LoanMaster, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    # file= "The analysis is being performed and will be submitted in to the database."
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    output_file = models.CharField(max_length=255)

    def __str__(self):
        return f"Analysis {self.analysis_id} for Loan {self.loan.loan_id}"
    
    


class AnalysisLock(models.Model):
    loan = models.OneToOneField(LoanMaster, on_delete=models.CASCADE)
    lock_acquired_time = models.DateTimeField()

    def __str__(self):
        return f"Lock for Loan {self.loan.loan_id}"


def document_upload_to(instance, filename):
    
    return f'documents/loan_{instance.loan.loan_id}/{filename}'


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    loan = models.ForeignKey(LoanMaster, on_delete=models.CASCADE)
    bank_account_number = models.CharField(max_length=20)
    file_path = models.FileField(upload_to=document_upload_to)
    analysis = models.ForeignKey(Analysis, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Document {self.document_id} for Loan {self.loan.loan_id}"