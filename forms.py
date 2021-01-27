from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PDFForm(FlaskForm):
	'''Using this to disable CSRF protection for this form
	the form doesn't need to be secure, and should work without cookies enabled
	From: https://stackoverflow.com/questions/15649027/wtforms-csrf-flask-fieldlist/55024901#55024901
	'''
	class Meta:
		csrf = False

	pdf = FileField('Upload PDF', validators = [FileAllowed(['pdf'])])
	pages = StringField('Pages to Merge',
						validators = [DataRequired(), Length(min = 1, max = 50)])
	

	submit = SubmitField('Submit')