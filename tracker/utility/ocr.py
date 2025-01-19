import pdfplumber
import re
import spacy
from datetime import datetime
from ..models import Date,Items
from ..models import Date,Items
from django.db.models import Sum,F
from .utils import response


ner=spacy.load("en_core_web_sm")
path='./media/uploads/'

categories = {
    1: [
        'Fruits', 'Vegetables', 'Dairy', 'Bread', 'Eggs', 'Atta', 'Rice',
        'Oil', 'Dals', 'Meats', 'Fish', 'Masala', 'Dry Fruits', 'Breakfast',
        'Sauces', 'Grocery', 'Kitchen', 'Tea', 'Coffee'
    ],
    2: [
        'Packaged', 'Ice Cream', 'Frozen Food', 'Sweet', 'Cold Drinks',
        'Munchies', 'Biscuits'
    ]
}

def f(product):
    word=ner(product)
    category=[]
    for _,v in categories.items():
        sim=[]
        for i in v:
            x=-1
            for w in word:
                x=max(x,w.similarity(ner(i)))
            sim.append(x)
        category.append([max(sim),sim.index(max(sim))])
    if category[0][0]>category[1][0]:
        return categories[1][category[0][1]]
    else:
        return categories[2][category[1][1]]
    
def data_extractor(file_name):
    try:
        with pdfplumber.open(path+file_name) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                
        rows = text.split("\n")
        
        date_pattern = r"(\d{2}-\d{2}-\d{4})"
        item_pattern = r"\d+\s([a-zA-Z0-9\s\(\)&,.]+)\d{8}"
        total_amount_pattern = r"([\d\.]+)\s*$"
        invoice_value_pattern = r"Invoice Value\s+([\d\.]+)"
        qty_pattern = r"^\d+\s[a-zA-Z0-9\s\(\)&,.]+?\d{8}\s+(\d+)\s"
        
        extracted_date = None
        items = []
        invoice_value = None
        
        for row in rows:
            date_match = re.search(date_pattern, row)
            item_match = re.search(item_pattern, row)
            qty_match = re.search(qty_pattern, row)
            amount_match = re.search(total_amount_pattern, row)
            invoice_value_match = re.search(invoice_value_pattern, row)
            
            if date_match:
                extracted_date = date_match.group(0)
                
            if item_match and amount_match:
                item_name = item_match.group(1).strip()
                quantity= int(qty_match.group(1))
                total_amount = amount_match.group(1).strip()
                items.append({"Item Name": item_name, "Quantity":quantity,"Category":f(item_name), "Total Amount": total_amount})
            
            if invoice_value_match:
                invoice_value = invoice_value_match.group(1)

        Date.objects.create(date=datetime.strptime(extracted_date, "%d-%m-%Y").date(),Total_items=len(items),Total_spent=invoice_value)
        for item in items:
            date_obj, _ = Date.objects.get_or_create(date=datetime.strptime(extracted_date, "%d-%m-%Y").date())
            Items.objects.create(Name=item['Item Name'],Quantity=item['Quantity'],Price=item['Total Amount'],Category=item['Category'],date=date_obj)
        return "Data Uploaded Successfully"
    
            
    except Exception as e:
        raise Exception(f"Error processing PDF:{str(e)}")
    

def graph_data():
    last_7=Date.objects.order_by('-date')[:7].values('date','Total_spent')
    dates=[entry['date']for entry in last_7]
    total=[entry['Total_spent']for entry in last_7]
    date=[date.strftime('%Y-%m-%d')for date in dates]
    return date,total


def budget(budget):
    last_30=Date.objects.order_by('-date')[:30].aggregate(Sum('Total_spent'))['Total_spent__sum']
    return int(budget)-int(last_30)

def insight(budget):
    total_spent=Date.objects.order_by('-date')[:30].aggregate(Sum('Total_spent'))['Total_spent__sum']
    last_30d=Date.objects.order_by('-date')[:30].values_list('date',flat=True)
    last_30i=Items.objects.filter(date__in=last_30d).values_list('Name','Quantity','Price')
    insights= response(budget,total_spent,last_30i)
    return insights

def find(category):
    for k,v in categories.items():
        if category in v:
            return k

def analytics_data():
    last_30=Date.objects.order_by('-date')[:30].values_list('date',flat=True)
    last_30i=Items.objects.filter(date__in=last_30).values_list('Category','Price','Quantity')
    spending_per_date_category =last_30i.values_list('date', 'Category').annotate(total_spent=Sum(F('Price') * F('Quantity'))).order_by('date', 'Category')

    spending={}
    for entry in spending_per_date_category:
        date,category,amount=entry
        print(date,category,amount)
        if date not in spending:
            spending[date]={'essential':0,'non-essential':0}
        base_category=find(category)
        if base_category==1:
            spending[date]['essential']+=amount
        else:
            spending[date]['non-essential']+=amount
    
    dates=list(spending.keys())
    essential=[spending[date]['essential']for date in dates]
    non_essential=[spending[date]['non-essential']for date in dates]
    
    return dates,essential,non_essential