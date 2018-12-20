from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import Required, Length, Regexp

class DiseaseForm(FlaskForm):
    name = StringField('Название болезни', validators=[Required(), Length(1, 256)])
    submit = SubmitField('Есть!')

class EquipmentForm(FlaskForm):
    name = StringField('Название Аппаратуры', validators=[Required(), Length(1, 256)])
    submit = SubmitField('Есть!')

class EmployeeForm(FlaskForm):
    name = StringField('ФИО', validators=[Required(), Length(1, 256)])
    experience = IntegerField('Стаж', validators=[Required()])
    degree = SelectField('Учёная степень', coerce=int, choices=[])
    submit = SubmitField('Есть!')
    
class EmployeeEquipmentForm(FlaskForm):
    name = SelectField('ФИО', coerce=int, choices=[])
    equipment = SelectField('Аппаратура', coerce=int, choices=[])
    submit = SubmitField('Есть!')

class EmployeeDiseaseForm(FlaskForm):
    name = SelectField('ФИО', coerce=int, choices=[])
    disease = SelectField('Специализация болезни', coerce=int, choices=[])
    submit = SubmitField('Есть!')
