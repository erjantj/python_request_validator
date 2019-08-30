from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from forms import ContactForm
from webob.multidict import MultiDict
import api_pb2
import pprint


response = api_pb2.ErrorResponse
contactFormRequest = api_pb2.ContactFormRequest()
contactFormRequest.subject = 'dasdasdasd'
contactFormRequest.message = '{TEST_KEY}, {TEST_KEY2} asd trefsd'
contactFormRequest.sender = 'yerzhan.torgaaasdaasdasdasdasdasdasdasdasds@evgmail.com'
contactFormRequest.active = True


data = {
	'subject': contactFormRequest.subject,
	'message': contactFormRequest.message,
	'sender': contactFormRequest.sender,
	'active': contactFormRequest.active,
}



form = ContactForm(data)
print('Validated:', form.validate())

errors = form.errors
print(errors)

errors_list = []
for field, messages in errors.items():
    error =  api_pb2.Error(field=field, messages=messages)
    errors_list.append(error)

response.errors = errors_list

print()
print(response.errors)
