from django import forms

class RepaymentForm(forms.Form):
    akpab_file = forms.FileField()
    month = forms.ChoiceField(choices=[
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ])
    year = forms.IntegerField()  # Add the year field
