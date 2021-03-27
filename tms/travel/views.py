from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, transaction
from django.db import connections
from datetime import datetime
# from .forms import signupform

# Create your views here.
from django.http import HttpResponse

def home(request):
	if 'customer_id' in request.session:
		with connection.cursor() as cursor:
			cursor.execute("SELECT title, description from trips WHERE customer_id = %s", [request.session['customer_id']])
			rows = cursor.fetchall()
		with connection.cursor() as cursor:
			cursor.execute("SELECT first_name from customer WHERE customer_id = %s", [request.session['customer_id']])
			row = cursor.fetchone()
		log_in = True
		return render(request, 'travel/home.html', {'rows':rows,'log_in':log_in,'first_name':row[0]})

def addtrip(request):
	if 'customer_id' in request.session:
		if request.method == "POST":
			title = request.POST["title"]
			description = request.POST["description"]
			drive_link = request.POST["drive_link"]
			start_date = request.POST["start_date"]
			end_date = request.POST["end_date"]
			status = 0
			cursor = connections['default'].cursor()
			cursor.execute("INSERT INTO trips(title, description, drive_link, start_date, end_date, status, customer_id)  VALUES (%s, %s, %s,%s,%s,%s,%s)",
					   [title, description, drive_link, start_date, end_date, status, request.session['customer_id']])
			return redirect('travel:home')
		else:
			return render(request, 'travel/addtrip.html',{'log_in':True})
