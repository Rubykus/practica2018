import datetime
import pytz
from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)
    from_date = forms.DateTimeField(label='From date(year-month-day hour:minutes)')
    to_date = forms.DateTimeField(label='To date(year-month-day hour:minutes)')

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")
        print(from_date)

        if from_date and to_date:
            current_date = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
            if from_date < current_date or to_date < current_date:
                raise forms.ValidationError("Dates should be greater then сurrnt date")
            if from_date > to_date:
                raise forms.ValidationError("'from_date' shouldn't be greater then 'to_date'")
