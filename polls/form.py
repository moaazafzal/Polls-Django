from django import forms
from .models import Question,Choice




class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = [
            'question_text',
            'pub_date',


        ]


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = [
            'question',
            'choice_text',
            'votes',


        ]
        # def clean_title(self):
        #     myvote= self.cleaned_data.get('votes')
        #     if myvote==:

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass