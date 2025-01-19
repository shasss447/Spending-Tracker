from django.db import models

# Create your models here.
class UploadFile(models.Model):
    file=models.FileField(upload_to='uploads/')
    uploadede_at=models.DateTimeField(auto_now_add=True)

class Date(models.Model):
    date=models.DateField(blank=False,primary_key=True)
    Total_items=models.IntegerField(blank=False)
    Total_spent=models.FloatField(blank=False)


class Items(models.Model):
    Name=models.CharField(max_length=100,blank=False)
    Quantity=models.IntegerField(blank=False)
    Price=models.FloatField(blank=False)
    Categories=models.TextChoices("Categories","Vegetables Junk")
    Category=models.CharField(blank=False,choices=Categories,max_length=10)
    Platform_choice=models.TextChoices("Platform_choice","Zepto Blinkit Instamart")
    Platform=models.CharField(blank=True,default="Zepto",choices=Platform_choice,max_length=10)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)