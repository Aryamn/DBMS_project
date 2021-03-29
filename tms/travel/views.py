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
			if end_date < datetime.datetime.now().date():
				messages.error(request, f'Trip cannot be added as it already ended!')
			cursor = connections['default'].cursor()
			cursor.execute("INSERT INTO trips(title, description, drive_link, start_date, end_date, customer_id)  VALUES (%s, %s, %s,%s,%s,%s,%s)",
					   [title, description, drive_link, start_date, end_date, request.session['customer_id']])
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
			cursor.execute("SELECT place_name from location natural join travels WHERE trip_id = %s", [tripid])
			loc_row = cursor.fetchall()
		context = {
			'log_in': True,
			'first_name': name[0],
			'title': row[2],
			'description': row[3],
			'drive_link': row[4],
			'start_date': row[5],
			'end_date': row[6],
			'locations':loc_row
		}
		return render(request, 'travel/updtrip.html', context)
	return redirect('user:login')

def updtransport(request,tripid):
	if 'customer_id' in request.session:
		if request.is_ajax and request.method == "POST":
			cnt = request.POST.getlist('transport_cnt')
			print(cnt)
			print(cnt[0])
			for i in range(0,cnt):
				type_t = request.POST["type"]
				from_loc = request.POST["from"]
				to_loc = request.POST["to"]
				trans_name = request.POST["trans_name"]
				cost = request.POST["cost"]
				departure = request.POST["departure"]
				arrival = request.POST["arrival"]
				# ticket_photo = request.POST["ticket"]
				if arrival < departure:
					messages.error(request, f'Transport Booking {cnt+1}: You cannot arrive before departing!!')
				else:
					cursor = connections['default'].cursor()
					cursor.execute("INSERT INTO transportbooking(type,from_loc,to_loc,trans_name,cost,departure,arrival,trip_id)  VALUES (%s, %s, %s,%s,%s,%s,%s,%s)",
						   [type_t,from_loc,to_loc,trans_name,cost,departure,arrival, tripid])
			return redirect('travel:updtrip',tripid=tripid)
		return redirect('travel:updtrip',tripid=tripid)

def updlocation(request,tripid):
	if 'customer_id' in request.session:
		if request.is_ajax and request.method == "POST":
			cnt = request.POST.getlist('transport_cnt')
			print(cnt)
			print(cnt[0])
			for i in range(0,cnt):
				place_name = request.POST["place_name"]
				# ticket_photo = request.POST["ticket"]
				cursor = connections['default'].cursor()
				cursor.execute("SELECT location_id from location WHERE place_name = %s", [place_name])
				row = cursor.fetchone()
				location_id=row[0]
				cursor.execute("INSERT INTO travels(location_id,trip_id)  VALUES (%s,%s)",
						[location_id, tripid])
			return redirect('travel:updtrip',tripid=tripid)
		return redirect('travel:updtrip',tripid=tripid)
			
# def updhotel(request,tripid):



# def upditinerary(request,tripid):
