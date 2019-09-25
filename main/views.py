from django.shortcuts import get_object_or_404,render,redirect

from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm




@login_required(login_url="/login/")
def Dashboard(request):

    usernamer = request.user.first_name +' '+ request.user.last_name
    return render(request, 'dashboard.html',{'usernamer':usernamer})


def logout_view(request):
	logout(request)
	return redirect("/login/")

def login_view(request):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		if request.user.is_authenticated:
			print("user is Authenticated")
		else:
			print("user is not Authenticated")
		return redirect("/")
	return render(request,"login.html",{"form":form})


@login_required(login_url="/login/")
def change_password(request):
    usernamer = request.user.first_name +' '+ request.user.last_name
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            #msg= 'Your password was successfully updated!'
            return redirect("/logout/")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,'usernamer':usernamer
    })