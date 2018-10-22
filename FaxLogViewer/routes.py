from flask import render_template, flash, redirect, url_for
from FaxLogViewer import app, mysql
from FaxLogViewer.Forms import LoginForm, RegistrationForm, SearchForm


@app.route('/')



@app.route('/home', methods=['GET', 'POST'])
def home():
	form = SearchForm()
	if form.validate_on_submit():
		datestart = form.DateStart.data
		dateend = form.DateEnd.data
		criteria = form.criteria.data
		if form.LogType.choices == 1:
			flash(" Incoming Start date: " + str(start) + " End date: " + str(end) + " Search data: " + data)
			#return url_for(incoming(datestart, dateend, criteria))
		elif form.LogType.choices == 2:
			flash(" Outgoing Start date: " + str(start) + " End date: " + str(end) + " Search data: " + data)
			#return url_for(outgoing(datestart, dateend, criteria))
		else:
			flash('No log type was selected!')

	return render_template('home.html', title='Search', form=form)


@app.route('/incoming')
def incoming():   #start, end, data
	cur = mysql.connection.cursor()
	#flash("Start date: " + str(start) + " End date: " + str(end) + " Search data: " + data)
	result = cur.execute("SELECT ifid, oid, rcvd_timestamp, state, recipient_name, num_pages, delivery_results, "
						 "caller_name FROM faxlogs_db.incoming_faxes ORDER BY ifid DESC LIMIT 100")

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


@app.route('/outgoing')
def outgoing(): #start, end, data
	cur = mysql.connection.cursor()
	#flash("Start date: " + str(start) + " End date: " + str(end) + " Search data: " + data)
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
