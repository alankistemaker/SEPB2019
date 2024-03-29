from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()
User1 = get_user_model()

from .models import *
from django.contrib.auth.forms import UserCreationForm

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
        fields = "__all__"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        exclude = ["created_at", "updated_at", "students", "leaders"]


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class InternalSupervisorForm(ModelForm):
    class Meta:
        model = Internal_Supervisor
        fields = "__all__"
        exclude = ["created_at", "updated_at"]


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = "__all__"
        exclude = ["created_at", "updated_at"]
        labels = {
            "title": "Unit Title",
            "unit_code": "Unit Code",
            "BB_unit_code": "Blackboard Unit Code",
            "ulos": "Unit Learning Outcomes",
            "convenor": "Unit Convenor",
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "category", "year"]


class EditProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ["proposal", "group"]
        fields = "__all__"


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        exclude = ["client"]
        fields = "__all__"


class ProposalStageCreateForm(ModelForm):
    class Meta:
        model = Proposal_Stage
        fields = "__all__"


class StudentListForm(forms.Form):
    students = forms.ModelChoiceField(queryset=Student.objects.all().order_by("name"))


class InternalSupervisorListForm(forms.Form):
    internal_supervisors = forms.ModelChoiceField(
        queryset=Internal_Supervisor.objects.all().order_by("name")
    )


class ProposalStageCreateForm(ModelForm):
    class Meta:
        model = Proposal_Stage
        fields = "__all__"


class UnitListForm(forms.Form):
    units = forms.ModelChoiceField(queryset=Unit.objects.all().order_by("unit_code"))
    fields = "__all__"


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ["department"]
        fields = "__all__"


class EditClientContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class AddStudentGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["students"]
