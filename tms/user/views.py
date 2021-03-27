from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection, transaction
from django.db import connections
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

def register(request):
	if 'customer_id' in request.session:
		messages.error(request, f'Please Logout First')
		return redirect('user:profile')
	context = {}
	if request.method == 'POST':
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		gender = request.POST["gender"]
		address = request.POST["address"]
		mobile = request.POST["mobile"] 
		emailid = request.POST["email"]
		password = request.POST["password"]
		confirm_password = request.POST["confirm_password"]
		date_of_birth = request.POST["dob"]
		if len(mobile) != 10:
			messages.error(request, f'Mobile No. should be of exactly 10 digits')
			return render(request, 'user/register.html', context)
		if password != confirm_password:
			messages.error(request, f'Password and Confirm Password do not match')
			context = {
				'log_in': False
			}
			return render(request, 'user/register.html', context)
		cursor = connections['default'].cursor()
		try:
			cursor.execute("INSERT INTO customer(first_name, last_name, gender, address, mobile, emailid, password, dob)  VALUES (%s, %s, %s,%s,%s,%s,%s,%s)",
					   [first_name, last_name, gender, address, mobile, emailid, password, date_of_birth])
		except Exception as error:
			error_str = str(error)
			if 'customer_chk_2' in error_str:
				messages.error(request, f'Mobile No. in Wrong Format')
			if 'customer_chk_3' in error_str:
				messages.error(request, f'Email ID in Wrong Format')
			return render(request, 'user/register.html',{'log_in':False})
		return redirect('user:login')
	else:
		gender_list = ["Male","Female","Other"]
		return render(request, 'user/register.html',{'genders':gender_list,'log_in':False})


def login(request):
	if 'customer_id' in request.session:
		messages.error(request, f'Please Logout First')
		return redirect('user:profile')
	context = {}
	if request.method == 'POST':
		emailid = request.POST["email"]
		password = request.POST["password"]
		with connection.cursor() as cursor:
			cursor.execute("SELECT * from customer WHERE emailid = %s AND password = %s", [emailid, password])
			row = cursor.fetchone()
			if row is None:
				messages.error(request, f'User Not found! If you are new you may register first.')
				context = {
					'message': 'The email address or mobile number you entered is not connected to an account',
					'type': 'error',
					'log_in': False
				}
				return render(request, 'user/login.html', {'log_in': False})

			request.session['customer_id'] = row[0]  
			return redirect('travel:home')

	else:
		return render(request, 'user/login.html',{'log_in': False})


def logout(request):
	if 'customer_id' in request.session:
		del request.session['customer_id']
		return redirect('user:login')
	else:
		return redirect('user:login')


def profile(request):
	context = {}
	if 'customer_id' in request.session:
		if request.method == 'POST':
			first_name = request.POST["first_name"]
			last_name = request.POST["last_name"]
			emailid = request.POST["email"]
			address = request.POST["address"]
			mobile = request.POST["mobile"]
			gender = request.POST["gender"]
			password=request.POST["password"]
			if len(mobile) != 10:
				messages.error(request, f'Mobile No. should be of exactly 10 digits')
				return render(request, 'user/register.html', context)
			cursor = connections['default'].cursor()
			try:
				cursor.execute(
					"UPDATE customer SET first_name = %s, last_name = %s, emailid = %s, mobile = %s, address = %s,password=%s",
					[first_name, last_name, emailid, mobile, address,password])
			except Exception as error:
				error_str = str(error)
				if 'customer_chk_2' in error_str:
					messages.error(request, f'Mobile No. in Wrong Format')
				if 'customer_chk_3' in error_str:
					messages.error(request, f'Email ID in Wrong Format')

		# print(first_name, last_name, email)
		with connection.cursor() as cursor:
			cursor.execute("SELECT * from customer WHERE customer_id = %s", [request.session['customer_id']])
			row = cursor.fetchone()
		context = {
			'log_in': True,
			'first_name': row[1],
			'last_name': row[2],
			'gender': row[3],
			'address': row[4],
			'mobile': row[5],
			'email': row[6],
			'password' : row[7],
			'dob': row[8]
		}
		return render(request, 'user/profile.html', context)
	return redirect('user:login')
