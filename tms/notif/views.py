from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, transaction
from django.db import connections
from datetime import datetime
# from .forms import signupform

# Create your views here.
from django.http import HttpResponse

def notify(request):
	if 'customer_id' in request.session:
		with connection.cursor() as cursor:
			cursor.execute("SELECT first_name from customer WHERE customer_id = %s", [request.session['customer_id']])
			name = cursor.fetchone()
		with connection.cursor() as cursor:
			cursor.execute("SELECT time_,category,trip_id from notifications WHERE customer_id = %s ORDER BY time_ DESC", [request.session['customer_id']])
			rows = cursor.fetchall()

		for row in rows:
			

		context = {
			'log_in': True,

		}
		return render(request, 'notif/notify.html', context)
	return redirect('user:login')