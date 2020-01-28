from flask import Flask, url_for, render_template, request, redirect, flash, session, send_file
import requests
import urllib # Python URL functions
import urllib.request as urllib2 # Python URL functions
from flask_pymongo import PyMongo
from functools import wraps
import datetime
import xlsxwriter




app = Flask(__name__)

app.secret_key = "ggz_k99e51#-2$1$vd^6s71gpn04$m%$y@8j_9k^6&do0k%6=8"

app.config['MONGO_DBNAME'] = "ATY_FRESH"
app.config['MONGO_URI'] = "mongodb://localhost:27017/ATY_FRESH"

mongo = PyMongo(app)

 

    

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#--------------------------------------------- HOME PAGE ------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#--------------------------------------------- REGISTER PAGE ------------------------------------------------
# @app.route('/register', methods = ['GET','POST'])
# def register():
#    return render_template('register.html')
# class Register(form):
# 	username = TextField('Username', [validators.Length(min=4, max=20)])
# 	email = TextField('Email Id', [validators.Length(min=10, max=50)])
# 	password = PasswordField('Password', [validators.Required(),
# 											validators.EqualTo('confirm', message ="Passwords must match." )])
# 	confirm = PasswordField('Repeat Password')
# 	mob_no = TextField('Mobile No.',[validators.length(min=10, max=10)])
# 	accept_tos =BooleanField("I accpet the <a href="">Terms & Conditions</a>.", [validators.Required()]) 

# @app.route('/register/', methods=['GET','POST'])
# def register():
# 	try:
# 		form = Register(request.form)

# 		if request.method == "POST" and form.validate():
# 			username = form.username.data 
# 			email = form.email.data 

# 			password = (form.password.data) 
# 			mob_no = form.mob_no.data
# 			users = mongo.db.new_users
# 			existing_user = users.find_one({'username' : username})

# 			if existing_user is None:
# 				users.insert({'username': username, 'email': email,'password': password, 'mob_no': mob_no})
# 				flash("Thanks for Register")
# 				session['logged_in'] = True 
# 				session['username'] = username
# 				return redirect(url_for('login'))
# 			flash("User already exists. Try again")
# 			return render_template("register.html", form=form)

# 		return render_template("register.html", form=form)

# 	except Exception as e:
# 		return(str(e))



#-------------------------------------------- PRODUCTS GALLERY ------------------------------------------

@app.route('/products_avanee_agro', methods=['GET', 'POST'])
def products_AG():
    return render_template('products.html')


#-------------------------------------------- CONTACT PAGE -----------------------------------------------

@app.route('/contact_avanee_agro', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


#-------------------------------------------- ABOUT US PAGE ------------------------------------------------

@app.route('/about_avanee_agro', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


#-----------------------------------------LOGIN PAGE-----------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login_user = mongo.db.users.find_one({"username" : request.form['username']})
        if login_user:
            if login_user['password'] == request.form['password']:
                if login_user['user'] == 'admin':
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    return redirect(url_for('dashboard_admin', user=login_user['username']))
                elif login_user['user'] == 'sales':
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    return redirect(url_for('dashboard_sell', user=login_user['username']))
                else:
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    return redirect(url_for('dashboard_purchase', user=login_user['username']))
        return "Invalid Username Password"
    return render_template('login.html')


# --------------------------------------------- LOGOUT PAGE -----------------------------------------------

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('index'))


#-------------------------------------------- PURCHASE SECTION --------------------------------------------

@app.route('/dashboard_purchase/<user>', methods = ['GET', 'POST'])
@login_required
def dashboard_purchase(user=None):
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")
    login_user = mongo.db.users.find_one({'username': user})
    products = mongo.db.products.find()
    farmers = mongo.db.farmers.find()
    transport = mongo.db.transport.find()
    if request.method == "POST":
        date = request.form['date']
        date = date.replace('/', '-')
        time = now.strftime("%H:%M")
        year = now.strftime("%Y")
        day = now.strftime("%d")
        month = now.strftime("%m")
        if request.form["button"]=="loose":
            farmer = request.form['farmer']
            product = request.form['product']
            quantity = request.form['quantity']
            # farmer_phone = request.form['farmer_phone']
            details = mongo.db.purchase_details
            details.insert({"farmer": request.form['farmer'], "product": request.form['product'], "amount": "0",
            "grade": request.form['grade'], "quantity": request.form['quantity'], "unit": request.form['unit'], "rate": "NA",
            "transport": request.form['transport'], "date":date, "time":time, "year":year, "day":day, "month":month})
        
            # # Sending SMS to Farmers
            # msg = "Hello "+farmer+", Purchase on "+date+" is:\n Product: "+product+", Tray:"+quantity+"."
            # values = {'authkey':'245023APhpm41yHx5bd5bcca', 'mobiles':farmer_phone, 'message':msg, 'sender':'AVNGRP', 'route':'4'}
            # url = "http://api.msg91.com/api/sendhttp.php"
            # postdata = urllib.urlencode(values)
            # req = urllib2.Request(url, postdata)
            # response = urllib2.urlopen(req)
            # print(response.read())
            return render_template('team/purchase.html', products = products, farmers = farmers, transport = transport, user=user, login_user=login_user, today=today)
        elif request.form["button"]=="regular":
            farmer = request.form['farmer']
            product = request.form['product']
            quantity = request.form['quantity']
            details = mongo.db.purchase_details
            details.insert({"farmer": request.form['farmer'], "product": request.form['product'], "amount": "0",
            "grade": request.form['grade'], "quantity": request.form['quantity'], "unit": request.form['unit'], "rate": "NA",
            "transport": request.form['transport'], "date":date, "time":time, "year":year, "day":day, "month":month})
        
            # # Sending SMS to Farmers
            # msg = "Hello "+farmer+", Purchase on "+date+" is:\n Product: "+product+", Tray:"+quantity+"."
            # values = {'authkey':'245023APhpm41yHx5bd5bcca', 'mobiles':farmer_phone, 'message':msg, 'sender':'AVNGRP', 'route':'4'}
            # url = "http://api.msg91.com/api/sendhttp.php"
            # postdata = urllib.urlencode(values)
            # req = urllib2.Request(url, postdata)
            # response = urllib2.urlopen(req)
            # print(response.read())  
            return render_template('team/purchase.html', products = products, farmers = farmers, transport = transport, user=user, login_user=login_user, today=today)  
    return render_template('team/purchase.html', products = products, farmers = farmers, transport = transport, user=user, login_user=login_user, today=today)


@app.route('/farmers_purchase/<user>', methods = ['GET', 'POST'])
@login_required
def farmers_purchase(user=None):
    hello = mongo.db.farmers
    f = hello.find()
    login_user = mongo.db.users.find_one({'username': user})

    if request.method == "POST":
        farmer = mongo.db.farmers
        farmer.insert({"first_name": request.form['first_name'], "last_name": request.form['last_name'],
        "address": request.form['address'], "email": request.form['email'], "contact": request.form['contact'], "balance": request.form['balance']})
    return render_template('team/farmer_purchase.html', f=f, login_user=login_user)


#--------------------------------------------------DISTRIBUTION SECTION--------------------------------------

@app.route('/dashboard_sell/<user>', methods = ['GET', 'POST'])
@login_required
def dashboard_sell(user=None):
    now = datetime.datetime.now()
    today = now.strftime("%d-%m-%Y")
    products = mongo.db.products.find()
    customers = mongo.db.customers.find()
    login_user = mongo.db.users.find_one({'username': user})
    if request.method == "POST":
        # Information taken from Form
        now = datetime.datetime.now()
        if request.form["button"]=="loose":
            customer = request.form['customer']
            quantity = request.form['quantity']
            rate = request.form['rate']
            product = request.form['product']
            unit = request.form['unit']
            date = request.form['date']
            date = date.replace('/',"-")
            # information related to transaction from collection amount_details
            amount_details = mongo.db.customers.find_one({"nick_name" : customer})
            amount = str(int(quantity) * int(rate))
            balance = str(int(amount_details['balance']) + int(amount))
            amount_details['balance'] = balance
            mongo.db.customers.save(amount_details)

            # insert data into collection Sales_details
            sales = mongo.db.sales_details
            sales.insert({'customer': customer, 'product': product, "received" : "0",
            "quantity": quantity, "unit": unit, "rate": rate, "amount": amount, "balance": balance,
            "date": date, "time": now.strftime("%H:%M")})

            # customer Information for
            customer_info = mongo.db.customers.find_one({"nick_name": customer}) 
            cust_phone = customer_info['contact']
		
            # Create Message for Sending SMS
		
            # msg = "Hello "+customer+", Your Order on "+date+" is:\n Product: "+product+", Box: "+unit+", Tray:"+quantity+",\n Rate: "+rate+",\n Total Amount: Rs."+amount+"\n Remaining Balance to Pay: Rs."+balance+"\n - AVANI GROUP."
            # values = {'authkey':'245023APhpm41yHx5bd5bcca', 'mobiles':cust_phone, 'message':msg, 'sender':'AVNGRP', 'route':'4'}
            # url = "http://api.msg91.com/api/sendhttp.php"
            # postdata = urllib.urlencode(values)
            # req = urllib2.Request(url, postdata)
            # response = urllib2.urlopen(req)
            # print(response.read())
            return render_template('team/sell.html', products = products, customers = customers, user=user, login_user=login_user, today=today)
        elif request.form["button"]=="regular":
            customer = request.form['customer']
            quantity = request.form['quantity']
            rate = request.form['rate']
            product = request.form['product']
            unit = request.form['unit']
            date = request.form['date']
            date = date.replace('/',"-")
            # information related to transaction from collection amount_details
            amount_details = mongo.db.customers.find_one({"nick_name" : customer})
            amount = str(int(quantity) * int(rate))
            balance = str(int(amount_details['balance']) + int(amount))
            amount_details['balance'] = balance
            mongo.db.customers.save(amount_details)

            # insert data into collection Sales_details
            sales = mongo.db.sales_details
            sales.insert({'customer': customer, 'product': product, "received" : "0",
            "quantity": quantity, "unit": unit, "rate": rate, "amount": amount, "balance": balance,
            "date": date, "time": now.strftime("%H:%M")})

            # customer Information for
            customer_info = mongo.db.customers.find_one({"nick_name": customer}) 
            cust_phone = customer_info['contact']
		
            # Create Message for Sending SMS
		
            # msg = "Hello "+customer+", Your Order on "+date+" is:\n Product: "+product+", Box: "+unit+", Tray:"+quantity+",\n Rate: "+rate+",\n Total Amount: Rs."+amount+"\n Remaining Balance to Pay: Rs."+balance+"\n - AVANI GROUP."
            # values = {'authkey':'245023APhpm41yHx5bd5bcca', 'mobiles':cust_phone, 'message':msg, 'sender':'AVNGRP', 'route':'4'}
            # url = "http://api.msg91.com/api/sendhttp.php"
            # postdata = urllib.urlencode(values)
            # req = urllib2.Request(url, postdata)
            # response = urllib2.urlopen(req)
            # print(response.read())
            return render_template('team/sell.html', products = products, customers = customers, user=user, login_user=login_user, today=today)
    return render_template('team/sell.html', products = products, customers = customers, user=user, login_user=login_user, today=today)


@app.route('/profile/<user>', methods=['GET', 'POST'])
@login_required
def profile(user):
    login_user = mongo.db.users.find_one({'username': user})
    if request.method == "POST":
        details['full_name'] = request.form['full_name']
        details['address'] = request.form['address']
        details['email'] = request.form['email']
        details['contact'] = request.form['contact']
        mongo.db.users.save(details)
        return render_template('team/profile.html', user=user, login_user = login_user)
    return render_template('team/profile.html', user=user, login_user = login_user)


@app.route('/team_expenses/<user>', methods = ['GET', 'POST'])
@login_required
def team_expenses(user):
    login_user = mongo.db.users.find_one({'username': user})
    return render_template('team/sell_expenses.html', user=user, login_user = login_user)

#---------------------------------------------ADMIN SECTION----------------------------------------------

@app.route('/dashboard_admin/<user>', methods = ['GET', 'POST'])
@login_required
def dashboard_admin(user=None):
    # now = datetime.datetime.now()
    # date = now.strftime("%d-%m-%Y")
    # details_p = mongo.db.purchase_details.find({'date': date})
    # details_s = mongo.db.sales_details.find({'date': date})
    # if request.method == "POST":
    #     date = request.form['date']
    #     date = date.replace('/', '-')
    #     details_p = mongo.db.purchase_details.find({'date': date})
    #     details_s = mongo.db.sales_details.find({'date': date})
    #     return render_template('admin/admin_dashboard.html', details_p = details_p, details_s = details_s, date=date, user=user)
    return render_template('admin/admin_dashboard.html')

@app.route('/edit/<time>/<user>', methods = ['GET','POST'])
@login_required
def edit(time, user):
    details= mongo.db.purchase_details.find_one({'time': time})
    if request.method == "POST":
        details['farmer'] = request.form['farmer']
        details['product'] = request.form['product']
        details['grade'] = request.form['grade']
        details['quantity'] = request.form['quantity']
        details['rate'] = request.form['rate']
        details['transport'] = request.form['transport']
        details['amount'] = int(request.form['rate']) * int(request.form['quantity'])
        mongo.db.purchase_details.save(details)
        return redirect(url_for('dashboard_admin', user=user))
    return render_template('admin/edit.html', details=details)
# ----------------------------------------Farmers---------------------------------------------- #
@app.route('/farmers', methods = ['GET', 'POST'])
@login_required
def farmers():
    hello = mongo.db.farmers
    f = hello.find()

    if request.method == "POST":
        farmer = mongo.db.farmers
        farmer.insert({"first_name": request.form['first_name'], "last_name": request.form['last_name'],
        "address": request.form['address'], "email": request.form['email'], "contact": request.form['contact'], "balance": request.form['balance']})
    return render_template('admin/admin_farmers.html', f=f)

# ----------------------------------------Customers---------------------------------------------- #
@app.route('/customers', methods = ['GET', 'POST'])
@login_required
def customers():
    hello = mongo.db.customers
    c = hello.find()

    if request.method == "POST":
        customer = mongo.db.customers
        customer.insert({"cust_name": request.form['cust_name'], "nick_name": request.form['nick_name'], "company" : request.form['company'],
        "address": request.form['address'], "email": request.form['email'], "contact": request.form['contact'], 'balance': request.form['balance']})
    return render_template('admin/admin_customers.html', c = c)

# ----------------------------------------Products---------------------------------------------- #
@app.route('/products', methods = ['GET', 'POST'])
@login_required
def products():
    hello = mongo.db.products
    p = hello.find()

    if request.method == "POST":
        product = mongo.db.products
        product.insert({"product_name": request.form['product_name'], "type": request.form['type'], "unit": request.form['unit'], "subunit": request.form['sub_unit']})
    return render_template('admin/admin_products.html', p = p)

# ----------------------------------------Team---------------------------------------------- #
@app.route('/team', methods = ['GET', 'POST'])
@login_required
def team():
    hello = mongo.db.users
    sales = hello.find({'user' : 'sales'})
    purchase = hello.find({'user' : 'purchase'})
    transport = mongo.db.transport.find()
    expense = mongo.db.expense.find()
    if request.method == "POST":
        if request.form['btn'] == "Sales":
            user = mongo.db.users
            user.insert({"full_name": request.form['sales_full_name'], 'address' : request.form['sales_address'], 'email' : request.form['sales_email'],
            "contact": request.form['sales_contact'],"birthdate":request.form['sales_birthdate'],'username': request.form['sales_username'], 'password' : request.form['sales_password'], 'user': 'sales'})
        elif request.form['btn'] == "Purchase":
            user = mongo.db.users
            user.insert({"full_name": request.form['purchase_full_name'], 'address' : request.form['purchase_address'], 'email' : request.form['purchase_email'],
            "contact": request.form['purchase_contact'], 'username': request.form['purchase_username'], 'password' : request.form['purchase_password'], 'user': 'purchase'})
        elif request.form['btn'] == "Transport":
            vehicle = mongo.db.transport
            vehicle.insert({"transport_type": request.form['transport_type'], "full_name": request.form['transport_full_name'], 'address' : request.form['transport_address'], 'contact' : request.form['transport_contact'],
            "vehicle_name": request.form['vehicle_name'], 'vehicle_type': request.form['vehicle_type'], 'vehicle_no' : request.form['vehicle_no']})
        elif request.form['btn'] == "Expense":
            user = mongo.db.expense
            user.insert({"expense_date":request.form['expense_date'], "expense_team_name":request.form['expense_team_name'],"expense_person":request.form['expense_person'],"expense_amount":request.form["expense_amount"],"expense_amount_type":request.form['expense_amount_type'],"expense_reason":request.form['expense_reason']})
    return render_template('admin/admin_team.html', sales = sales, purchase = purchase, transport = transport, expense = expense, team = team)
 
# ----------------------------------------Payment---------------------------------------------- #
@app.route('/payments', methods = ["POST", "GET"])
@login_required
def payments():
    customers = mongo.db.customers.find()
    farmers = mongo.db.farmers.find()
    team = mongo.db.users.find()
    payments = mongo.db.payments
    sales = mongo.db.sales_details
    if request.method == "POST":
        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        if request.form['btn'] == "customer_entry":
            customer = request.form['customer']
            received = request.form['customer_amount']
            bank = request.form['bank']
            date = request.form['customer_date']
            amount_details = mongo.db.customers.find_one({"nick_name" : customer})
            balance = int(amount_details['balance']) - int(received)
            amount_details['balance'] = balance
            mongo.db.customers.save(amount_details)
            payments.insert({"customer": customer, "received_amount": received, "bank": bank, "date": date})
            sales.insert({'customer': customer, 'product': "NA", "received" : received,
        "quantity": "0", "unit": "0", "rate": "0", "amount": "0", "balance": balance,
        "date": date})
            return render_template('admin/admin_payments.html', customers= customers, farmers = farmers, team = team)

        elif request.form['btn'] == "farmer_entry":
            farmer = request.form['farmer']
            paid = request.form['farmer_amount']
            date = request.form['farmer_date']
            amount_details = mongo.db.farmers.find_one({"first_name" : farmer})
            balance = int(amount_details['balance']) - int(paid)
            amount_details['balance'] = balance
            mongo.db.farmers.save(amount_details)
            payments.insert({"farmer": farmer, "paid_amount": paid, "date": date})
            sales.insert({'farmer': farmer, 'product': "NA", "paid_amount" : paid,
        "quantity": "0", "unit": "0", "rate": "0", "amount": "0", "balance": balance,
        "date": date})
            return render_template('admin/admin_payments.html', customers= customers, farmers = farmers, team = team)

        elif request.form['btn'] == "team":
            member = request.form['member']
            amount = request.form['team_amount']
            amount_type = request.form['amount_type']
            comment = request.form['comment']
            date = request.form['team_date'] 


    return render_template('admin/admin_payments.html', customers= customers, farmers = farmers, team = team)

# ----------------------------------------Customer ledger---------------------------------------------- #
@app.route('/customer_ledger', methods=["GET", "POST"])
@login_required
def customer_ledger():
    customers = mongo.db.customers.find()
    if request.method == "POST":
        customer = request.form['customer']
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        excel(customer, fromdate,todate)
        details = mongo.db.sales_details.find({'date':{ '$gte' : fromdate, '$lte' : todate }, "customer": customer})
        excel(customer, fromdate,todate)
        return render_template('admin/admin_ledger_report.html', details=details, customers=customers, customer=customer)
    
    return render_template('admin/admin_ledger_report.html', customers=customers)

# ----------------------------------------Admin Stock---------------------------------------------- #
@app.route('/admin_stock', methods=["GET", "POST"])
@login_required
def admin_stock():
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    return render_template('admin/admin_stock.html')
# ----------------------------------------Admin Sell---------------------------------------------- #
@app.route('/admin_sell', methods=["GET", "POST"])
@login_required
def admin_sell(user=None):
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    details_s = mongo.db.sales_details.find({'date': date})
    if request.method == "POST":
          date = request.form['date']
          date = date.replace('/', '-')
          details_s = mongo.db.sales_details.find({'date': date})
    return render_template('admin/admin_sell.html',details_s = details_s, date=date, user=user)
    # return render_template('admin/admin_sell.html')
# ----------------------------------------Admin Purchase---------------------------------------------- #
@app.route('/admin_purchase', methods=["GET", "POST"])
@login_required
def admin_purchase(user=None):
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    details_p = mongo.db.purchase_details.find({'date': date})
    if request.method == "POST":
        date = request.form['date']
        date = date.replace('/', '-')
        details_p = mongo.db.purchase_details.find({'date': date})
        
    return render_template('admin/admin_purchase.html', details_p = details_p, date=date, user=user)
    # return render_template('admin/admin_purchase.html')    
# ----------------------------------------Farmer Ledger---------------------------------------------- #
@app.route('/farmer_ledger', methods=["GET", "POST"])
@login_required
def farmer_ledger():
    farmers = mongo.db.farmers.find()
    if request.method == "POST":
        farmer = request.form['farmer']
        fromdate = request.form['fromdate']
        todate = request.form['todate']
        details = mongo.db.purchase_details.find({'date':{ '$gte' : fromdate, '$lte' : todate }, "farmer": farmer})
        return render_template('admin/admin_ledger_report.html', details=details, farmers=farmers, farmer=farmer)
    
    return render_template('admin/admin_ledger_report.html', farmers=farmers)



def excel(cust, d1, d2):
    details = mongo.db.sales_details.find({'date':{ '$gte' : d1, '$lte' : d2 }, "customer": cust})
    cust_details = mongo.db.customers.find_one({'nick_name': cust})
    row = 5
    col = 3
    farmers = mongo.db.farmers.find()
    customers = mongo.db.customers.find()
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('static/excels/Expenses02.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True, 'font_size': 16})
    

    # Add a number format for cells with money.

    # Write some data headers.
    worksheet.write('D2', 'Ledger Report of '+ cust_details['nick_name'] , bold)
    worksheet.write('D5', 'Date', bold)
    worksheet.write('E5', 'ITEM', bold)
    worksheet.write('F5', 'Unit', bold)
    worksheet.write('G5', 'Quantity', bold)
    worksheet.write('H5', 'Rate', bold)
    worksheet.write('I5', 'Amount', bold)
    worksheet.write('J5', 'Received', bold)
    


    # Iterate over the data and write it out row by row.
    for i in details:
        worksheet.write(row, col, i['date'])
        worksheet.write(row, col + 1, i['product'])
        worksheet.write(row, col + 2, i['unit'])
        worksheet.write(row, col + 3, int(i['quantity']))
        worksheet.write(row, col + 4, int(i['rate']))
        worksheet.write(row, col + 5, int(i['amount']))
        worksheet.write(row, col + 6, int(i['received']))
        row += 1

    worksheet.write(row, 3, 'Remaining Balance',       bold)
    worksheet.write(row, 8, int(cust_details['balance']), bold)
    workbook.close()
    return render_template('admin/admin_ledger_report.html', customers=customers, farmers = farmers)

@app.route('/LedgerReport')
def get_excel():
    return send_file('static/excels/Expenses02.xlsx', attachment_filename="LedgerReport.xlsx")
    return redirect(url_for('customer_ledger'))

if __name__ == '__main__':
    app.run(debug=True)