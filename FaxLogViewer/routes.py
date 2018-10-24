from flask import render_template, flash, redirect, url_for
from FaxLogViewer import app, mysql
from FaxLogViewer.Forms import LoginForm, RegistrationForm, SearchForm

app.config['SECRET_KEY'] = 'b48fb44860e75665aa4ec29c703bae6d'


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', title='Home')


@app.route('/search', methods=['GET', 'POST'])
def search():
	form = SearchForm()
	if form.submit():
		datestart = str(form.DateStart.data)
		if not form.DateEnd.data:
			dateend = datestart
		else:
			dateend = str(form.DateEnd.data)
		criteria = form.criteria.data
		searchinfo = "{},{},{}".format(datestart, dateend, criteria)
		if form.LogType.data == "1":
			return redirect(url_for('incoming', data=searchinfo))
		elif form.LogType.data == "2":
			return redirect(url_for('outgoing', data=searchinfo))
		else:
			flash('No log type was selected!')
	return render_template('search.html', title='Search', form=form)


@app.route('/incoming/<string:data>', methods=['GET', 'POST'])
def incoming(data):
	cur = mysql.connection.cursor()

	criteria = data.split(',')
	searchdates = (criteria[0], criteria[1])

	result = cur.execute("SELECT ifid, oid, rcvd_timestamp, state, recipient_name, "
						 "caller_name FROM faxlogs_db.incoming_faxes WHERE rcvd_timestamp >= %s AND rcvd_timestamp < %s", searchdates)

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


@app.route('/outgoing/<string:data>', methods=['GET', 'POST'])
def outgoing(data):
	cur = mysql.connection.cursor()

	criteria = data.split(',')
	searchdates = (criteria[0], criteria[1])

	result = cur.execute("SELECT ofid, oid, sent_timestamp, rcpt_fax, state, username, sender_name FROM "
						 "faxlogs_db.outbound_faxes WHERE sent_timestamp >= %s AND sent_timestamp < %s", searchdates)

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


@app.route("/register")
def register():
	form = RegistrationForm()
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	##if current_user.is_authenticated:
	##	return redirect(url_for('home'))

	form = LoginForm()

	if form.submit():
		print(form.email.data, " ", form.password.data)
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('search'))
			##user = User.query.filter_by(email=form.email.data).first()
			##if user and bcrypt.check_password_hash(user.password, form.password.data):
			##	login_user(user, remember=form.remember.data)
			##	next_page = request.args.get('next')
			##	return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			print(form.validate_on_submit())
			print(form.email.data, " ", form.password.data)
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	#logout_user()
	return redirect(url_for('home'))
