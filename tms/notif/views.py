from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, transaction
from django.db import connections
from datetime import datetime, timedelta

# Create your views here.
from django.http import HttpResponse

def notecount(userid):
	with connection.cursor() as cursor:
		cursor.execute("SELECT time_ from notifications WHERE customer_id = %s ORDER BY time_ DESC", [userid])
		rows = cursor.fetchall()
	count = 0
	for row in rows:
		if row[0] > datetime.now():
			count += 1
	return count


def notify(request):
	if 'customer_id' in request.session:
		with connection.cursor() as cursor:
			cursor.execute("SELECT first_name from customer WHERE customer_id = %s", [request.session['customer_id']])
			name = cursor.fetchone()
		with connection.cursor() as cursor:
			cursor.execute("SELECT time_,category,trip_id,note_id from notifications WHERE customer_id = %s ORDER BY time_ DESC", [request.session['customer_id']])
			rows = cursor.fetchall()
		notifs = []
		for row in rows:
			notif_dict = {}
			if row[0] > datetime.now():
				time1 = row[0] + timedelta(hours=1)
				notif_dict["tripid"] = row[2]
				with connection.cursor() as cursor:
						cursor.execute("SELECT title, start_date from trips WHERE trip_id = %s", [row[2]])
						trip = cursor.fetchone()
				if row[1] == 0:
					notif_dict["header"] = "Attention!!"
					notif_dict["message"] = "PACK UP YOUR THINGS: Your trip titled " + trip[0] + " is going to start in 2 days i.e. from " + trip[1]
				elif row[1] == 1:
					notif_dict["header"] = "Best Wishes!!"
					notif_dict["message"] = "HAPPY JOURNEY: For Your trip titled " + trip[0]
				elif row[1] == 2:
					with connection.cursor() as cursor:
						cursor.execute("SELECT type from transportbooking WHERE trip_id = %s,departure = %s", [row[2],time1])
						transport = cursor.fetchone()
					notif_dict["header"] = "Hurry!!"
					notif_dict["message"] = trip[0] + ": You have your " + transport[0] + " in 1 hour i.e. at " + time1.time() + " . Buckle up faster for this ride"
				elif row[1] == 3:
					with connection.cursor() as cursor:
						cursor.execute("SELECT hotelid from hotelbooking WHERE trip_id = %s, checkin = %s", [row[2],time1])
						hotel = cursor.fetchone()
					with connection.cursor() as cursor:
						cursor.execute("SELECT name from hotel WHERE hotelid = %s", [hotel[0]])
						hotelname = cursor.fetchone()
					notif_dict["header"] = "Hurry!!"
					notif_dict["message"] = trip[0] + ": You have your " + hotelname[0] + " hotel checkin in 1 hour i.e. at " + time1.time() + " . Buckle up faster for this ride"
				elif row[1] == 4:
					with connection.cursor() as cursor:
						cursor.execute("SELECT itineraryid from itinerarybooking WHERE trip_id = %s,visit_time = %s", [row[2],time1])
						itinerary = cursor.fetchone()
					with connection.cursor() as cursor:
						cursor.execute("SELECT name from itinerary WHERE itineraryid = %s", [itinerary[0]])
						itineraryname = cursor.fetchone()
					notif_dict["header"] = "Hurry!!"
					notif_dict["message"] = trip[0] + ": You have your " + itinerary[0] + " visiting time in 1 hour i.e. at " + time1.time() + ". Buckle up faster for this adventure"
				notifs.append(notif_dict)
				cursor = connections['default'].cursor()
				cursor.execute("DELETE from notifications WHERE note_id = %s", row[3])

		context = {'log_in': True, 'ndict': notif_dict, 'first_name':name[0]}
		return render(request, 'notif/notifications.html', context)
	return redirect('user:login')