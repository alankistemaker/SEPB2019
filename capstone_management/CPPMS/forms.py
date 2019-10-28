from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model
User1 = get_user_model()
from django.contrib.auth.forms import UserCreationForm 
from .models import Proposal_Status,Proposal_Stage

# Login Form
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
# Add User
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    class Meta:
        model = User1
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = User1
        fields = ["username", "first_name", "last_name", "email"]


class ProposalStatusForm(ModelForm):
    class Meta:
        model = Proposal_Status
        fields ='__all__'

class ProposalStageCreateForm(ModelForm):
    class Meta:
        model = Proposal_Stage
        fields ='__all__'