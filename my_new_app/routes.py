from flask import render_template, url_for, flash, redirect, request, send_from_directory, current_app
from flask_login import login_user, current_user, logout_user, login_required
from . import app, db
from .forms import RegistrationForm, LoginForm, WorkoutForm, ExerciseForm
from .models import User, Workout, Exercise, ExerciseType
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    current_app.logger.info('Home route accessed')
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
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
    
    # If workout doesn't exist, redirect to home
    if not workout:
        flash('That workout no longer exists.', 'info')
        return redirect(url_for('home'))
    
    form = ExerciseForm()
    if form.validate_on_submit():
        exercise_type_id = int(form.exercise_type.data)
        exercise = Exercise(
            workout_id=workout.id,
            exercise_type_id=exercise_type_id,
            sets=form.sets.data,
            reps=form.reps.data,
            weight=form.weight.data
        )
        db.session.add(exercise)
        db.session.commit()
        
        exercise_type = ExerciseType.query.get(exercise_type_id)
        flash(f'{exercise_type.name} added to workout!', 'success')
        return redirect(url_for('workout', workout_id=workout.id))
    
    return render_template('workout.html', 
                         title='Workout',
                         workout=workout,
                         form=form)

@app.route("/exercise_progress")
@login_required
def exercise_progress():
    current_app.logger.info('Exercise progress route accessed')
    exercise_type_id = request.args.get('exercise_type')
    
    # Get all exercise types for the dropdown
    exercise_types = ExerciseType.query.order_by(ExerciseType.name).all()
    
    if exercise_type_id:
        # Get all exercises of this type for the current user
        history = Exercise.query.join(Workout).filter(
            Workout.user_id == current_user.id,
            Exercise.exercise_type_id == exercise_type_id
        ).order_by(Workout.date).all()
        
        selected_exercise = ExerciseType.query.get(exercise_type_id)
        selected_exercise_name = selected_exercise.name if selected_exercise else None
        
        # Prepare data for plotting
        dates = [exercise.workout.date.strftime('%m/%d/%y') for exercise in history]
        weights = [float(exercise.weight) for exercise in history]
    else:
        history = []
        dates = []
        weights = []
        selected_exercise_name = None

    return render_template('exercise_progress.html',
                         exercise_types=exercise_types,
                         selected_exercise=selected_exercise_name,
                         history=history,
                         dates=dates,
                         weights=weights)

@app.route('/static/sw.js')
def sw():
    return send_from_directory('static', 'sw.js')

@app.route("/delete_exercise/<int:exercise_id>", methods=['POST'])
@login_required
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    workout = Workout.query.get(exercise.workout_id)
    
    if workout.user_id != current_user.id:
        flash('You cannot delete this exercise.', 'danger')
        return redirect(url_for('home'))
    
    # Get exercise type name before deleting
    exercise_type_name = exercise.exercise_type.name if exercise.exercise_type else None
    
    db.session.delete(exercise)
    db.session.commit()
    flash('Exercise deleted!', 'success')
    
    # If coming from exercise progress page, return there
    if 'exercise_progress' in request.referrer:
        return redirect(url_for('exercise_progress', exercise_type=exercise.exercise_type_id))
    return redirect(url_for('workout', workout_id=workout.id))

@app.route("/delete_workout/<int:workout_id>", methods=['POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    
    # Verify the workout belongs to the current user
    if workout.user_id != current_user.id:
        flash('You cannot delete this workout.', 'danger')
        return redirect(url_for('home'))
    
    # Delete all associated exercises first
    Exercise.query.filter_by(workout_id=workout.id).delete()
    
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/update_workout_date/<int:workout_id>", methods=['POST'])
@login_required
def update_workout_date(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('You cannot modify this workout.', 'danger')
        return redirect(url_for('home'))
    
    new_date = request.form.get('date')
    if new_date:
        workout.date = datetime.strptime(new_date, '%Y-%m-%d')
        db.session.commit()
        flash('Workout date updated!', 'success')
    
    return redirect(url_for('workout', workout_id=workout.id))

@app.errorhandler(404)
def not_found_error(error):
    flash('The page you requested does not exist.', 'info')
    return redirect(url_for('home'))