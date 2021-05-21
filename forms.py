from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, DateField, validators
from db.person import Person
from db.alien import Alien
from db.ship import Ship
from wtforms.fields.html5 import DateTimeLocalField
import datetime


class AdvanceForm(Form):

    def validate(self):
        return True


class StillForm(AdvanceForm):
    person = SelectField('Choose Person', validators=[validators.DataRequired()])
    ship = SelectField('Choose Ship', validators=[validators.DataRequired()])
    datetime_ = StringField('Choose still time', validators=[validators.DataRequired()])

    def validate(self):
        if not super(StillForm, self).validate():
            return False

        try:
            my_date = datetime.datetime.strptime(self.datetime_.data, "%Y-%m-%d")
            print(my_date)
        except:
            print(self.datetime_.errors)
            self.datetime_.errors = []
            self.datetime_.errors.append("Please use %Y-%m-%d standard")
            return False
        return True

    def submit(self, data):
        print(data)
        Alien().still_person(data['alien'], data['person'], data['ship'], data['datetime_'])


class AddFormShip(Form):
    name = StringField('Name', [validators.DataRequired()])

    def validate(self):
        if not super(AddFormShip, self).validate():
            return False
        if Ship().check_ship(self.name.data):
            msg = "Ship with such name and surname already exists"
            self.name.errors.append(msg)
            return False
        return True


class AddFormPerson(Form):
    name = StringField('Name', [validators.DataRequired()])
    surname = StringField('Surname', [validators.DataRequired()])
    url = StringField('URL to photo')

    def validate(self):
        if not super(AddFormPerson, self).validate():
            return False
        if Person().check_person(self.name.data, self.surname.data):
            msg = "Person with such name and surname already exists"
            self.name.errors.append(msg)
            self.surname.errors.append(msg)
            return False
        return True


class AddFormAlien(Form):
    name = StringField('Name', [validators.DataRequired()])
    surname = StringField('Surname', [validators.DataRequired()])
    url = StringField('URL to photo')

    def validate(self):
        if not super(AddFormAlien, self).validate():
            return False
        if Alien().check_alien(self.name.data, self.surname.data):
            msg = "Alien with such name and surname already exists"
            self.name.errors.append(msg)
            self.surname.errors.append(msg)
            return False
        return True
