from dateutil import parser
import phonenumbers
import re

from . import database
from . import config

class Person(object):
    def __init__(self, first_name, last_name, phone_number, email_address, address, birth_date, id=None):
        self._id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email_address = email_address
        self.address = address
        self.birth_date = birth_date

        if self._id is None:
            self._insert_db()

    def to_dict(self):
        '''

        :return: Dictionary representing all attributes of object.
        '''
        return {k[1:]:v for k, v in self.__dict__.items()}

    def _insert_db(self):
        '''
        Initially insert person to relational database

        :return:
        '''
        to_insert = self.to_dict()
        to_insert.pop('id')

        sql = f'''
            INSERT INTO {config.person_table} 
            ({', '.join(list(to_insert.keys()))})
            VALUES
            ({['%s']*len(to_insert)})
        '''

        with database.get_conn() as conn:
            conn.execute('START TRANSACTION;')
            conn.execute(sql, tuple(to_insert.values()))
            id = conn.execute('SELECT LAST_INSERT_ID() as id;')
            conn.execute('COMMIT;')
            
        self._id = id

    def _update_db(self, key):
        '''
        Update database based on attribute in setter function that calls this.

        :param key:
        :return:
        '''
        if self._id is None:
            return

        sql = f'''
            UPDATE {config.person_table}
            SET {key} = %s
            WHERE id = {self._id}
              '''
        
        with database.get_conn() as conn:
            conn.execute(sql, (self.__dict__[f'_{key}'],))

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name
        self._update_db('first_name')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name
        self._update_db('last_name')

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        phone_number = phonenumbers.parse(phone_number, 'US')

        self._phone_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        self._update_db('phone_number')

    @property
    def email_address(self):
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        if not re.match(config.EMAIL_REGEX, email_address):
            raise Exception('Invalid email address.')

        self._email_address = email_address
        self._update_db('email_address')

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address
        self._update_db('address')

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date):
        self._birth_date = parser.parse(birth_date).date()
        self._update_db('birth_date')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self):
        raise NotImplementedError('Cannot change the database id')
