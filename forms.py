from utils import Form
from utils import html_template


class ContactForm(Form):

    def boot(self):
        self.register('html_template', html_template)

    def rules(self):
        return {
            'subject': ['required', ('len', {'min':3, 'max':50}),],
            'message': ['required', ('len', {'min':3, 'max':50}), 'html_template'],
            'sender': ['required', 'email'],
            'active': ['required', 'boolean']
        }

    

