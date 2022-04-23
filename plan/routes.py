from plan import app
from flask import render_template, request, redirect, url_for, flash
from plan.models import Todo, User
from plan import db
from plan.forms import SignupForm, SigninForm
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/tasks', methods= ['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        add_name = request.form['name']
        add_description = request.form['description']
        add_id = current_user.id
        new_task = Todo(name = add_name, description = add_description, owner=add_id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added!", category='success')
    return render_template('tasks.html', user = current_user)

@app.route('/tasks/new', methods = ['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        add_name = request.form['name']
        add_description = request.form['description']
        add_id= current_user.id
        new_task = Todo(name = add_name, description = add_description, owner=add_id)
        db.session.add(new_task)
        db.session.commit()
        return render_template('tasks.html', user = current_user)
    else:
        return render_template('new_task.html')

@app.route('/tasks/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form['name']
        task.description = request.form['description']
        db.session.commit()
        return redirect('/tasks')
    else:
        return render_template('edit.html', task=task)

@app.route('/tasks/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/tasks')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash (f'Account created successfully!', category='success')
        return redirect('/home')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        attempted_user= User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are signed in as: {attempted_user.username}", category='success')
            return redirect('/home')
        else:
            flash('Username and password are not match! Please  try again')
    return render_template('signin.html', form=form, user = current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been signed out!")
    return redirect(url_for('home_page'))

@app.route('/tasks/done/<int:id>')
def task_done (id):
    task = Todo.query.get_or_404(id)
    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True
    db.session.commit()
    return redirect('/tasks')
