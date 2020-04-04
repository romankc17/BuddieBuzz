import json
from django.http import  HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Profile
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method=='POST':
        u_form = CreateUserForm(request.POST)
        print('before validation')
        if u_form.is_valid():
            user_ = u_form.cleaned_data.get('username')
            u_form.save()
            messages.success(request, 'Account created for '+user_)
            return redirect('login')
        else:
            for error in u_form.error_messages:
                print(error)
                messages.error(request, error)
    else:
        u_form = CreateUserForm()
    context={'u_form':u_form}
    return render(request, 'account/register.html', context)

@login_required
def profile_view(request, the_slug):
    profile = get_object_or_404 (Profile,user=User.objects.get(username=the_slug))
    try:
        current_user = Profile.objects.get(user = request.user)
    except:
        raise Http404('Create a Profile to view others Profile.')
    context={'profile':profile,
             'current_user':current_user,
             'is_followed':current_user.follows(profile),
             }
    return render(request, 'account/profile.html',context )

def follow_unfollow(request):
    current_user = Profile.objects.get(user = request.user)
    profile = Profile.objects.get(user = User.objects.get(username=request.POST.get('profile_user')))
    if current_user.follows(profile):
        current_user.unfollow_to(profile)
    else:
        current_user.follow_to(profile)
    data={
        'profile':profile.user.username,
        'current_user': current_user.user.username,
        'is_followed': current_user.follows(profile),
    }
    if request.is_ajax():
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404()

@login_required # (decorators) login required if not redirected to login page
def profile_update(request):
	if request.method=='POST':
		u_form = UserUpdateForm(request.POST, instance = request.user)
		 #request post data and populate the form with updated user

		p_form = ProfileUpdateForm(request.POST, #request post data
								    request.FILES, #request image file uploaded by users
								    instance = request.user.profile) # populate the form with updated profile

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!!')
			return redirect('profile')


	else:
		u_form = UserUpdateForm(instance = request.user) #populate the form with current user
		p_form = ProfileUpdateForm(instance = request.user.profile) #populate the form with current profile


	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'account/profile_update.html', context)




