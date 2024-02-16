from django import forms
from .models import Wpis, Komentarz, Profile

class WpisForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'width': '200px'}))
    class Meta:
        model = Wpis
        fields = ['content']  # lista pól, które chcesz uwzględnić w formularzu
    def __init__(self, *args, **kwargs):
        super(WpisForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['style'] = 'width: 200px;'

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['content']

class BioForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio']
    def __init__(self, *args, **kwargs):
        super(BioForm, self).__init__(*args, **kwargs)
        # Wypełnij pola formularza danymi użytkownika
        if self.instance:
            try:
                self.fields['bio'].initial = self.instance.profile.bio
            except:
                self.fields['bio'].initial = self.instance.bio
