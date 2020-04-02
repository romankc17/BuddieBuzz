import json

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Profile
from .forms import CreateProfileForm,CreateUserForm,UserCreationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('logout')
    if request.method=='POST':
        p_form = CreateProfileForm(request.POST)
        u_form = CreateUserForm(request.POST)
        print('before validation')
        if u_form.is_valid():
            u_form=u_form.save(commit=False)
            # u_id = u_form.cleaned_data.get('id')
            if p_form.is_valid():

                first_name=p_form.cleaned_data.get('first_name')
                middle_name=p_form.cleaned_data.get('middle_name')
                last_name=p_form.cleaned_data.get('last_name')
                gender=p_form.cleaned_data.get('gender')
                dob = (request.POST['dob'])
                country = p_form.cleaned_data['country']
                phone_number = request.POST['phone']
                profile = Profile(user=u_form,
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        gender=gender,
                        dob=dob,
                        country=country,
                        phone_number=phone_number,

                            )
                u_form.save()
                profile.save()
                # user = u_form.cleaned_data.get('username')
                # messages.success(request, 'Account created for '+user)
            return redirect('login')
    else:
        p_form = CreateProfileForm()
        u_form = CreateUserForm()

    return render(request, 'account/register.html', {'p_form':p_form, "u_form":u_form,})

@login_required
def profile_view(request, the_slug):
    profile = get_object_or_404 (Profile,user=User.objects.get(username=the_slug))
    current_user = Profile.objects.get(user = request.user)
    context={'profile':profile,
             'current_user':current_user,
             'is_followed':current_user.follows(profile),
             }
    return render(request, 'account/profile.html',context )

# def follow_unfollow(request):
#     current_user = Profile.objects.get(user = request.user)
#     profile = Profile.objects.get(user = User.objects.get(username=request.POST.get('profile_user')))
#     if current_user.follows(profile):
#         current_user.unfollow_to(profile)
#     else:
#         current_user.follow_to(profile)
#     context={
#         'profile':profile,
#         'current_user': current_user,
#         'is_followed': current_user.follows(profile),
#     }
#     if request.is_ajax():
#         html=render_to_string('account/follow_unfollow.html', context, request=request)
#
#         return JsonResponse({'form':html})

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







