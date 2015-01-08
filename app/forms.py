from flask.ext.wtf import Form
from wtforms.fields import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Regexp, Length


class LocationForm(Form):
    """
    Form to receive a user's location.
    """
    temp_choice = SelectField(
        label='Temp choice',
        description='A choice between hot or cold',
        choices=[('hot', 'hot'), ('cold', 'cold')],
        validators=[
            DataRequired('Please select a temp choice.')
        ]
    )
    location = StringField(
        label='Location',
        description='A zip code using five numbers.',
        validators=[
            DataRequired('Please enter your zip code.'),
            Length(max=5, message='Zip codes of five digits only.'),
            # Regexp('[/d]{5}')
        ]
    )
    submit = SubmitField(
        label='Submit'
    )
