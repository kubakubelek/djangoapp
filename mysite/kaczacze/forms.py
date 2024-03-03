from django import forms
from .models import Wpis, Komentarz, Profile

class WpisForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%;'}),label='')
    class Meta:
        model = Wpis
        fields = ['content']  # lista pól, które chcesz uwzględnić w formularzu

    def __init__(self, *args, **kwargs):
        super(WpisForm, self).__init__(*args, **kwargs)


class KomentarzForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%;', 'rows':'2', 'cols':'58.5'}),label='')
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

class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']