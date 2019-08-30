
import types
import re

from wtforms import StringField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import validators
from wtforms.compat import with_metaclass
from wtforms.form import FormMeta
from wtforms.form import BaseForm
from wtforms.meta import DefaultMeta
from wtforms.fields.core import UnboundField
from wtforms.validators import ValidationError

from webob.multidict import MultiDict


def html_template(form, field):
    pattern = '{([0-9A-Za-z_ ]+)}'
    matches = re.findall(pattern, field.data)
    allowed_placeholders = set(['TEST_KEY'])

    for placeholder in matches:
        if not placeholder in allowed_placeholders:
            raise ValidationError('Invalid placeholder {}'.format(placeholder))


class RuleException(Exception):
    """"""


class Form(with_metaclass(FormMeta, BaseForm)):

    _DATA_TYPES = {
        'boolean': BooleanField,
        'password': PasswordField
    }

    _RULES_MAP = {
        'email': validators.Email,
        'required': validators.InputRequired,
        'len': validators.Length
    }

    def __init__(self, formdata=None):
        self.boot()
        self._setup_unbound_fields()
        super(Form, self).__init__(self._unbound_fields)
        self.process(MultiDict(formdata))

    def boot(self):
        pass

    def rules(self):
        return []

    def _setup_unbound_fields(self):
        for field_name, field_rules in self.rules().items():
            field_type, validators = self._parse_rules(field_name, field_rules)

            field = (field_name, UnboundField(field_type, field_name, validators))
            self._unbound_fields.append(field)

    def _parse_rules(self, field_name, rules):
        field_type = None
        validators = []

        for rule in rules:
            rule_name = rule
            rule_params = {}
            if isinstance(rule, tuple):
                rule_name, rule_params = rule

            if rule_name in self._DATA_TYPES:
                # Parse data type
                if not field_type:
                    field_type = self._DATA_TYPES[rule_name]
                else:
                    raise RuleException('Multiple data types defined for field: "{}"'.format(field_name))
            else:
                # Parse validator
                validator = self._RULES_MAP.get(rule_name, None)
                if not validator:
                    raise RuleException('Undefined rule: "{}"'.format(rule_name))

                if isinstance(validator, types.FunctionType):
                    validators.append(validator)
                else:
                   validators.append(validator(**rule_params))

        field_type = StringField if not field_type else field_type
        return (field_type, validators)

    def register(self, rule_name, rule_function):
        self._RULES_MAP[rule_name] = rule_function

