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
			cursor.execute("SELECT first_name from customer WHERE customer_id = %s", [request.session['customer_id']])
			name = cursor.fetchone()
		with connection.cursor() as cursor:
			cursor.execute("SELECT title, description from trips WHERE customer_id = %s", [request.session['customer_id']])
			rows = cursor.fetchall()
		log_in = True
		return render(request, 'travel/home.html', {'rows':rows,'log_in':log_in,'first_name':name[0]})
	return redirect('user:login')

def addtrip(request):
	if 'customer_id' in request.session:
		with connection.cursor() as cursor:
			cursor.execute("SELECT first_name from customer WHERE customer_id = %s", [request.session['customer_id']])
			name = cursor.fetchone()
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
			with connection.cursor() as cursor:
				cursor.execute("SELECT max(trip_id) from trips WHERE customer_id = %s", [request.session['customer_id']])
				row = cursor.fetchone()
			return redirect('travel:updtrip',tripid=row[0])
		else:
			return render(request, 'travel/addtrip.html',{'log_in':True,'first_name':name[0]})
	return redirect('user:login')

def deltrip(request,tripid):
	if 'customer_id' in request.session:
		cursor = connections['default'].cursor()
		cursor.execute("DELETE from trips WHERE trip_id = %s", tripid)
		return redirect('travel:home')
	return redirect('user:login')


def updtrip(request,tripid):
	if 'customer_id' in request.session:
		with connection.cursor() as cursor:
			cursor.execute("SELECT first_name from customer WHERE customer_id = %s", [request.session['customer_id']])
			name = cursor.fetchone()
		if request.method == 'POST':
			title = request.POST["title"]
			description = request.POST["description"]
			drive_link = request.POST["drive_link"]
			start_date = request.POST["start_date"]
			end_date = request.POST["end_date"]
			cursor = connections['default'].cursor()
			cursor.execute("UPDATE trips SET title = %s, description = %s, drive_link = %s, start_date = %s, end_date = %s WHERE trip_id = %s",
					[title, description, drive_link, start_date, end_date, tripid])

		with connection.cursor() as cursor:
			cursor.execute("SELECT * from trips WHERE trip_id = %s", [tripid])
			row = cursor.fetchone()
		
		context = {
			'log_in': True,
			'first_name': name[0],
			'title': row[2],
			'description': row[3],
			'drive_link': row[4],
			'start_date': row[5],
			'end_date': row[6]
		}
		return render(request, 'travel/updtrip.html', context)
	return redirect('user:login')