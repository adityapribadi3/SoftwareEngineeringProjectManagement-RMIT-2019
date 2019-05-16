



@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))

		# Create Cursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(Name, email, password) VALUES(%s, %s, %s)",
					(name, email, password))

		# Commit cursor
		mysql.connection.commit()

		# Close Connection
		cur.close()
