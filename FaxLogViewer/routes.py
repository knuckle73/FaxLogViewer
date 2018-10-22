from flask import render_template, flash, redirect, url_for
from FaxLogViewer import app, mysql
from FaxLogViewer.Forms import LoginForm, RegistrationForm, SearchForm
from datetime import timedelta





@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')


@app.route('/search', methods=['GET', 'POST'])
def search():
	form = SearchForm()
	#if form.validate_on_submit():
	datestart = form.DateStart.data
	if not form.DateEnd.data:
		dateend = datestart
	else:
		dateend = form.DateEnd.data
	criteria = form.criteria.data
	searchinfo = '{} {} {}'.format(datestart, dateend, criteria)
	print("Length before passing to function: ", len(searchinfo))
	if form.LogType.data == "1":
		print("Incoming - Start date: " + str(datestart) + " End date: " + str(dateend) + " Search data: " + criteria)
		return redirect(url_for('incoming', data=searchinfo))
	elif form.LogType.data == "2":
		print("Outgoing - Start date: " + str(datestart) + " End date: " + str(dateend) + " Search data: " + criteria)
		return redirect(url_for('outgoing', data=searchinfo))
	else:
		flash('No log type was selected!')
	return render_template('search.html', title='Search', form=form)

@app.route('/incoming/<data>', methods=['GET', 'POST'])
def incoming(data):
	cur = mysql.connection.cursor()
	print("Variable type: ", type(data))
	print("Length after passing: ", len(data))
	print(" Incoming - Start date: " + data[1] + " End date: " + data[2] + " Search data: " + data[3])
	criteria = (data[1], data[2])
	result = cur.execute("SELECT ifid, oid, rcvd_timestamp, state, recipient_name, num_pages, delivery_results, "
						 "caller_name FROM faxlogs_db.incoming_faxes WHERE rcvd_timestamp >= %s AND rcvd_timestamp < %s", criteria)

	incoming = cur.fetchall()

	cur.close()

	if result > 0:
		return render_template('incoming.html', incoming=incoming)
	else:
		msg = 'No Records Found'
		return render_template('incoming.html', msg=msg)


@app.route('/rcvd/<string:id>/')
def rcvd(id):
	# Create cursor
	cur = mysql.connection.cursor()

	# Get article
	cur.execute("SELECT ifid, extension, rcvd_timestamp, state, recipient_name, num_pages, archive_filename, "
				"caller_name FROM faxlogs_db.incoming_faxes WHERE ifid = %s", [id])

	detail = cur.fetchone()

	cur.close()

	return render_template('rcvd.html', detail=detail)


@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing(): #start, end, data
	cur = mysql.connection.cursor()
	print("Outgoing - Start date: " + str(data[1]) + " End date: " + str(data[2]) + " Search data: " + data[3])
	result = cur.execute("SELECT ofid, oid, sent_timestamp, state, username, sender_name FROM "
						 "faxlogs_db.outbound_faxes ORDER BY ofid DESC LIMIT 100")

	outgoing = cur.fetchall()

	cur.close()

	if result > 0:
		return render_template('outgoing.html', outgoing=outgoing)
	else:
		msg = 'No Records Found'
		return render_template('outgoing.html', msg=msg)


@app.route('/sent/<string:id>/')
def sent(id):
	# Create cursor
	cur = mysql.connection.cursor()

	# Get article
	cur.execute("SELECT sent_timestamp, sender_name, sender_fax, sender_email, state, fsched_code, rcpt_name, "
				"rcpt_fax, pages, subject, comments FROM faxlogs_db.outbound_faxes WHERE ofid = %s", [id])

	detail = cur.fetchone()

	cur.close()

	return render_template('sent.html', detail=detail)


@app.route('/calls')
def calls():
	# Create cursor
	cur = mysql.connection.cursor()

	# Get article
	result = cur.execute("SELECT clid, call_timestamp, direction FROM faxlogs_db.call_logs ORDER BY clid DESC LIMIT "
						 "100")

	calls = cur.fetchall()

	cur.close()

	if result > 0:
		return render_template('calls.html', calls=calls)
	else:
		msg = 'No Records Found'
		return render_template('calls.html', msg=msg)


@app.route('/call/<string:id>/')
def call(id):
	# Create cursor
	cur = mysql.connection.cursor()

	# Get article
	cur.execute("SELECT * FROM faxlogs_db.call_logs WHERE clid = %s", [id])

	call = cur.fetchone()

	cur.close()
	return render_template('call.html', call=call)


@app.route('/register')
def register():
	form = RegistrationForm()
	return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', title='Login', form=form)
