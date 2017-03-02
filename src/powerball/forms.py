from django import forms
from django.core.exceptions import ValidationError
from django.forms import MultiValueField
from django.utils.datastructures import MultiValueDict
from django.core import validators
from .models import Drawentry
from django.forms import modelformset_factory


class ArrayFieldSelectMultiple(forms.SelectMultiple):
    """This is a Form Widget for use with a Postgres ArrayField. It implements
    a multi-select interface that can be given a set of `choices`.

    You can provide a `delimiter` keyword argument to specify the delimeter used.

    """

    def __init__(self, *args, **kwargs):
        # Accept a `delimiter` argument, and grab it (defaulting to a comma)
        self.delimiter = kwargs.pop("delimiter", ",")
        super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

    def render_options(self, choices, value):
        # value *should* be a list, but it might be a delimited string.
        if isinstance(value, str):  # python 2 users may need to use basestring instead of str
            value = value.split(self.delimiter)
        return super(ArrayFieldSelectMultiple, self).render_options(choices, value)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            # Normally, we'd want a list here, which is what we get from the
            # SelectMultiple superclass, but the SimpleArrayField expects to
            # get a delimited string, so we're doing a little extra work.
            return self.delimiter.join(data.getlist(name))
        return data.get(name, None)

#class PowerballField(forms.IntegerField):



#PowerballForm = modelformset_factory(Drawentry, exclude=('user',))
class PowerballForm(forms.Form):
    def clean(self):
        """
        In here you can validate the two fields
        raise ValidationError if you see anything goes wrong.
        for example if you want to make sure that field1 != field2
        """
        field1 = self.cleaned_data['ball1']
        field2 = self.cleaned_data['ball2']
        field3 = self.cleaned_data['ball3']
        field4 = self.cleaned_data['ball4']
        field5 = self.cleaned_data['ball5']


        if len(set([field1, field2, field3, field4, field5])) < 5:
            # This will raise the error in field1 errors. not across all the form
            self.add_error("ball1","Balls has to be unique")

        return self.cleaned_data

    def __init__(self,*args, **kwargs):
        if 'userdraw' in kwargs:
            userdraw = kwargs.pop('userdraw')
        else:
            userdraw = None
        super(PowerballForm, self).__init__(*args, **kwargs)
        self.balls = [None] *5
        self.powerball = None
        if userdraw:
            self.balls = userdraw.balls
            self.powerball = userdraw.powerball
        for i in range(5):
            self.fields['ball'+str(i+1)] = forms.IntegerField(
                label='ball'+str(i+1),
                 min_value=1,
                max_value=69, initial=self.balls[i])
        self.fields['powerball'] = forms.IntegerField(label='powerball',
                                                  min_value=1,
                                        max_value=26, initial=self.powerball)



