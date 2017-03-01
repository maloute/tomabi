from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Button, Div, Reset
from django import forms
from models import Manga, Parser
from tomabi_app.parser.mangapanda import MangaPandaParser

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'}))


class AddMangaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMangaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal form-label-left post-form'
        self.helper.label_class = 'control-label col-md-3 col-sm-3 col-xs-12'
        self.helper.field_class = 'col-md-6 col-sm-6 col-xs-12'
        self.helper.layout.append(
            Div(
                Div(
                    Submit( 'save', 'Save', css_class = 'btn btn-success' ),
                    Reset( 'reset', 'Reset', css_class = 'btn btn-default'),
                    css_class = 'col-md-6 col-sm-6 col-xs-12 col-md-offset-3',
                    ),
                    css_class = 'form-group',
                )
            )
        super(AddMangaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Manga
        exclude = ['user']


class AddParserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddParserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal form-label-left post-form'
        self.helper.label_class = 'control-label col-md-3 col-sm-3 col-xs-12'
        self.helper.field_class = 'col-md-6 col-sm-6 col-xs-12'
        self.helper.layout.append(
            Div(
                Div(
                    Submit( 'save', 'Save', css_class = 'btn btn-success' ),
                    Reset( 'reset', 'Reset', css_class = 'btn btn-default'),
                    css_class = 'col-md-6 col-sm-6 col-xs-12 col-md-offset-3',
                    ),
                    css_class = 'form-group',
                )
            )
        super(AddParserForm, self).__init__(*args, **kwargs)

    def clean_methodname(self):
        data = self.cleaned_data['methodname']
        try:
            globals()[data]()
        except KeyError:
            raise forms.ValidationError("Method name does not exists in the parser directory or import failed !")
        except TypeError:
            return data

    class Meta:
        model = Parser
        exclude = ['']
