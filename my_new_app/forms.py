from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User, Exercise, ExerciseType

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
                         validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ExerciseForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ExerciseForm, self).__init__(*args, **kwargs)
        # Get choices from ExerciseType table
        exercise_types = ExerciseType.query.order_by(ExerciseType.name).all()
        self.exercise_type.choices = [(str(t.id), t.name) for t in exercise_types]

    exercise_type = SelectField('Exercise', validators=[DataRequired()])
    sets = IntegerField('Sets', validators=[DataRequired()])
    reps = IntegerField('Reps', validators=[DataRequired()])
    weight = FloatField('Weight (lbs)', validators=[DataRequired()])
    submit = SubmitField('Add Exercise')

class WorkoutForm(FlaskForm):
    date = DateField('Workout Date', validators=[DataRequired()])
    submit = SubmitField('Start Workout')