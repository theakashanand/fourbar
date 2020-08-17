from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

class PositionAnalysis(FlaskForm):
    a = FloatField('a', validators = [DataRequired()])
    b = FloatField('b', validators = [DataRequired()])
    c = FloatField('c', validators = [DataRequired()])
    d = FloatField('d', validators = [DataRequired()])
    theta2 = FloatField('theta 2', validators = [DataRequired()])
    
    submit = SubmitField('Submit')

class VelAccAnalysis(FlaskForm):
    a = FloatField('a', validators = [DataRequired()])
    b = FloatField('b', validators = [DataRequired()])
    c = FloatField('c', validators = [DataRequired()])
    d = FloatField('d', validators = [DataRequired()])
    theta2 = FloatField('theta 2', validators = [DataRequired()])
    theta3 = FloatField('theta 3', validators = [DataRequired()])
    theta4 = FloatField('theta 4', validators = [DataRequired()])
    omega2 = FloatField('omega 2', validators = [DataRequired()])
    alpha2 = FloatField('alpha 2',default=0)
    submit = SubmitField('Submit')

