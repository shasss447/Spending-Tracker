from django.shortcuts import render,HttpResponse
from .form import UploadFileForm
from .models import UploadFile
from .utility.ocr import data_extractor,graph_data,insight,budget,analytics_data
import io
import base64
import matplotlib.pyplot as plt


def home(request):
    if request.method=='POST':
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            uploaded_file=request.FILES['file']
            if uploaded_file.content_type=='application/pdf':
                file_instance=UploadFile(file=uploaded_file)
                file_instance.save()
                try:
                    extracted_data=data_extractor(uploaded_file.name)
                    return HttpResponse(extracted_data)
                except Exception as e:
                    return HttpResponse(f'error :{str(e)}')
            else:
                return HttpResponse('upload pdf')
    else:
        form=UploadFileForm()
    return render(request,'base.html',{'form':form})

def show_graph(request):
    date,total=graph_data()
    plt.figure(figsize=(8, 5))
    plt.bar(date, total, color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Total Spent')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    html = f"""
    <h1>Total Spent Over the Last 7 Days</h1>
    <img src="data:image/png;base64,{string}" alt="Graph">
    <br>
    """
    return HttpResponse(html)

def set_budget(request):
    if request.method == "GET":
        budget_value = request.GET.get("budget")
        try:
            budget_left=budget(budget_value)
            request.session['budget_left'] = budget_left    
            return render(request, "base.html", {
                "budget": budget_value,
                "budget_left": budget_left
            })
        except ValueError:
            return render(request,'base.html',{'error':'Invalid budget value. Please enter a number.'})
    return render(request, "base.html")

def insights(request):
    if request.method=="GET":
        try:
            budget=request.GET.get('budget',0)
            print(budget)
            if int(budget)  ==0:
                raise ValueError("Budget cannot be 0")
            response=insight(budget)
            return render(request,'base.html',{'insights':response})
        except ValueError as e:
            return HttpResponse(str(e))
    return HttpResponse(response)    
        

def analytics(request):
    dates,ess,noness=analytics_data()
    x = range(len(dates))

    plt.figure(figsize=(8, 6))
    plt.bar([pos-0.1 for pos in x],ess,width=0.2,label='Essentials',color='blue',)
    plt.bar([pos + 0.1 for pos in x],noness,width=0.2,label='Non-Essentials',color='red',)
    plt.xticks(x, [date.strftime('%Y-%m-%d') for date in dates], rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Money Spent')
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    html = f"""
    <h3>Total Spent Over the Last 7 Days</h3>
    <img src="data:image/png;base64,{string}" alt="Graph">
    <br>
    """
    return HttpResponse(html)
