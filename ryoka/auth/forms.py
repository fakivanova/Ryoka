from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, ValidationError
from wtforms.validators import Required, Length, EqualTo, Regexp
from ..models import User

class LoginForm(FlaskForm):
    username = StringField('Позывной', validators=[Required(), Length(1, 64)])
    password = PasswordField('Секретное слово', validators=[Required()])
    submit = SubmitField('Есть!')

class RegistrationForm(FlaskForm):
    username = StringField('Позывной', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-zА-Яа-я][A-Za-zА-Яа-я0-9]*$', 0, 
                                                          'Первая буква позывного - буква латинского или русского алфавита. Вторая буква позывного - буква латинского или русккого алфивита или цифра!')])
    rank = StringField('Звание', validators=[Required(), Length(1, 64),
                                                   Regexp('^[А-Яа-я]*$', 0, 'Неверное звание!')])
    password = PasswordField('Секретное слово', 
                             validators=[Required(), EqualTo('password2',
                                                             'Секретное слово нужно повторить правильно!')])
    password2 = PasswordField('Секретное слово ещё раз', validators=[Required()])
    submit = SubmitField('Есть!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Данный позывной уже числится за военнослужущим!')

