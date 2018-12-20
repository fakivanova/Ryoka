from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Regexp

class DiseaseForm(FlaskForm):
    name = StringField('Название болезни', validators=[Required(), Length(1, 256)])
    submit = SubmitField('Есть!')

class EquipmentForm(FlaskForm):
    name = StringField('Название Аппаратуры', validators=[Required(), Length(1, 256)])
    submit = SubmitField('Есть!')

