from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, DateField, SelectMultipleField, \
    IntegerField, validators
from db.person import Person
from db.alien import Alien
from db.ship import Ship
from wtforms.fields.html5 import DateTimeLocalField
import datetime


class AdvanceForm(Form):

    def validate(self):
        return True


class GetExperiment(AdvanceForm):
    N = IntegerField("Choose N")

    def validate(self, alive_id):
        return True

    def submit(self, data):
        return Person().get_experiment(data['person'], data['N']), 'excursion'


class GetExcursion(AdvanceForm):
    alien = SelectField('Choose Aliens', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        return True

    def submit(self, data):
        return Person().get_excursion(data['person'], data['alien']), 'excursion'


class GetKillAndStill(AdvanceForm):

    def validate(self, alive_id):
        return True

    def submit(self, data):
        return Person().get_killed_and_still(data['person']), 'alien'


class KilledForm(AdvanceForm):
    datetime_start = StringField('Choose first time', validators=[validators.DataRequired()])
    datetime_finish = StringField('Choose second time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(KilledForm, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_start.data, "%Y-%m-%d")
            my_date = datetime.datetime.strptime(self.datetime_finish.data, "%Y-%m-%d")
        except:
            self.datetime_start.errors = []
            self.datetime_start.errors.append("Please use %Y-%m-%d standard and N should be integer")
            return False
        return True

    def submit(self, data):
        return Person().get_killed(data['person'], data['datetime_start'], data['datetime_finish']), 'alien'


class GetNStilledForm(AdvanceForm):
    N = IntegerField("Choose N")
    datetime_start = StringField('Choose first time', validators=[validators.DataRequired()])
    datetime_finish = StringField('Choose second time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(GetNStilledForm, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_start.data, "%Y-%m-%d")
            my_date = datetime.datetime.strptime(self.datetime_finish.data, "%Y-%m-%d")
            n = int(self.N.data)
        except:
            self.datetime_start.errors = []
            self.datetime_start.errors.append("Please use %Y-%m-%d standard and N should be integer")
            return False
        return True

    def submit(self, data):
        return Person().get_stolen(data['person'], data['N'], data['datetime_start'], data['datetime_finish']), 'alien'


class GetVisited(AdvanceForm):
    datetime_start = StringField('Choose first time', validators=[validators.DataRequired()])
    datetime_finish = StringField('Choose second time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(GetVisited, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_start.data, "%Y-%m-%d")
            my_date = datetime.datetime.strptime(self.datetime_finish.data, "%Y-%m-%d")
        except:
            self.datetime_start.errors = []
            self.datetime_start.errors.append("Please use %Y-%m-%d standard")
            return False
        return True

    def submit(self, data):
        return Person().get_visited(data['person'], data['datetime_start'], data['datetime_finish']), 'ship'


class KillAlien(AdvanceForm):
    datetime_ = StringField('Choose first time', validators=[validators.DataRequired()])
    alien = SelectField('Choose Aliens', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(KillAlien, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_.data, "%Y-%m-%d")
            if not Alien().check_alive(int(self.alien.data)):
                self.alien.errors = []
                self.alien.errors.append("Alien already dead or he will be killed in future")
                return False
        except:
            self.datetime_.errors = []
            self.datetime_.errors.append("Please use %Y-%m-%d standard")

            return False
        return True

    def submit(self, data):
        Person().kill_alien(data['person'], data['alien'], data['datetime_'])


class EscapeForm(AdvanceForm):
    datetime_ = StringField('Choose first time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(EscapeForm, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_.data, "%Y-%m-%d")
            if Person().get_ship_specific_time(alive_id, my_date)[0] == -1:
                self.datetime_.errors = []
                self.datetime_.errors.append("Person should be on the ship")

                return False
        except:
            self.datetime_.errors = []
            self.datetime_.errors.append("Please use %Y-%m-%d standard and N should be integer")

            return False
        return True

    def submit(self, data):
        Person().escape_from(data['person'], data['datetime_'])


class GetNStillForm(AdvanceForm):
    N = IntegerField("Choose N")
    datetime_start = StringField('Choose first time', validators=[validators.DataRequired()])
    datetime_finish = StringField('Choose second time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(GetNStillForm, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_start.data, "%Y-%m-%d")
            my_date = datetime.datetime.strptime(self.datetime_finish.data, "%Y-%m-%d")
            n = int(self.N.data)
        except:
            self.datetime_start.errors = []
            self.datetime_start.errors.append("Please use %Y-%m-%d standard and N should be integer")
            return False
        return True

    def submit(self, data):
        return Alien().get_stolen(data['alien'], data['N'], data['datetime_start'], data['datetime_finish']), 'person'


class ExcursionForm(AdvanceForm):
    person = SelectMultipleField('Choose People', validators=[validators.DataRequired()])
    datetime_ = StringField('Choose still time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(ExcursionForm, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_.data, "%Y-%m-%d")
        except:
            self.datetime_.errors = []
            self.datetime_.errors.append("Please use %Y-%m-%d standard")
            return False
        return True

    def submit(self, data):
        Alien().make_excursion(data['alien'], data['person'], data['datetime_'])


class StillForm(AdvanceForm):
    person = SelectField('Choose Person', validators=[validators.DataRequired()])
    ship = SelectField('Choose Ship', validators=[validators.DataRequired()])
    datetime_ = StringField('Choose still time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(StillForm, self).validate():
            return False

        try:
            my_date = datetime.datetime.strptime(self.datetime_.data, "%Y-%m-%d")
            if Person().get_ship_specific_time(self.person.data, my_date)[0] != -1:
                self.datetime_.errors = []
                self.datetime_.errors.append("This person already in ship at this time")
                return False
        except:
            print(self.datetime_.errors)
            self.datetime_.errors = []
            self.datetime_.errors.append("Please use %Y-%m-%d standard")

            return False
        return True

    def submit(self, data):
        Alien().still_person(data['alien'], data['person'], data['ship'], data['datetime_'])


class TransferForm(AdvanceForm):
    person = SelectField('Choose Person', validators=[validators.DataRequired()])
    ship = SelectField('Choose Ship', validators=[validators.DataRequired()])
    datetime_ = StringField('Choose still time', validators=[validators.DataRequired()])

    def validate(self, alive_id):
        if not super(TransferForm, self).validate():
            return False
        try:
            my_date = datetime.datetime.strptime(self.datetime_.data, "%Y-%m-%d")
            if Person().get_ship_specific_time(self.person.data, my_date)[0] == -1:
                self.datetime_.errors = []
                self.datetime_.errors.append("Person should be on ship at this time")
                return False
        except:
            print(self.datetime_.errors)
            self.datetime_.errors = []
            self.datetime_.errors.append("Please use %Y-%m-%d standard")

            return False
        return True

    def submit(self, data):
        Alien().transfer_person(data['alien'], data['person'], data['ship'], data['datetime_'])


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
