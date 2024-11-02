from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from . import app, db
from .forms import RegistrationForm, LoginForm, WorkoutForm, ExerciseForm
from .models import User, Workout, Exercise

EXERCISE_TYPES = [
    'Dumbbell chest press',
    'Dumbbell bicep curls',
    'Single dumbbell triceps raise',
    'Dumbbell overhead press',
    'Lat pull downs',
    'Rows',
    'Leg press',
    'Calf press'
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/new_workout", methods=['GET', 'POST'])
@login_required
def new_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(date=form.date.data, user=current_user)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('workout', workout_id=workout.id))
    return render_template('new_workout.html', title='New Workout', form=form)

@app.route("/workout/<int:workout_id>", methods=['GET', 'POST'])
@login_required
def workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user != current_user:
        flash('You cannot access this workout.', 'danger')
        return redirect(url_for('home'))
    
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise_type = request.form.get('exercise_type')
        exercise = Exercise(
            workout_id=workout.id,
            exercise_type=exercise_type,
            sets=form.sets.data,
            reps=form.reps.data,
            weight=form.weight.data
        )
        db.session.add(exercise)
        db.session.commit()
        flash(f'{exercise_type} added to workout!', 'success')
        return redirect(url_for('workout', workout_id=workout.id))
    
    return render_template('workout.html', 
                         title='Workout',
                         workout=workout,
                         form=form,
                         exercise_types=EXERCISE_TYPES)