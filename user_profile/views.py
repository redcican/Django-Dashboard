from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def user_profile_view(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'values': profile,
    }

    if request.method == 'GET':
        return render(request, 'user_profile/profile.html', context)

    if request.method == 'POST':
        # bio = request.POST['bio']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        country = request.POST['country']
        postal_code = request.POST['postal_code']
        about_me = request.POST['about_me']

        # profile.bio = bio
        profile.first_name = first_name
        profile.last_name = last_name
        profile.address = address
        profile.country = country
        profile.postal_code = postal_code
        profile.about_me = about_me

        profile.save()

        messages.success(request, "Updated profile successfully")
        return redirect('profile')
