from wtforms import Form, BooleanField, StringField, PasswordField, validators
from db.person import Person
from db.alien import Alien


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
