from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .forms import CreatePollForm
from .models import Poll
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
# for celery
import datetime
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models.functions import Now
from django.utils import timezone
from datetime import datetime, timedelta


def Login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)

        print(user)
        if user is not None:
            print("LOGIN SUCCESSFULL")
            auth.login(request, user)
            return redirect('home')
        else:            
            messages.info(request,'invalidddddddd credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')



@login_required(login_url='login')
def home(request):

    Poll.objects.filter(dateTime__lte=Now()-timedelta(days=1)).delete()
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'home.html', context)



@login_required(login_url='login')
def profile(request):
    return render(request, 'accounts/details.html')



@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'create.html', context)


@periodic_task(run_every=crontab(minute='*/5'))
def delete_old_orders():
    d = timezone.now() - datetime.timedelta(hours=24)
    #get expired orders
    orders = Poll.objects.filter(timestamp__lt=d)
    #delete them
    orders.delete()


@login_required(login_url='login')
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        elif selected_option == 'option4':
            poll.option_four_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'vote.html', context)


@login_required(login_url='login')
def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'results.html', context)


@login_required(login_url='login')
def delete(request, poll_id):
    poll_id = int(poll_id)
    try:
        poll_id = Poll.objects.get(id = poll_id)
    except Poll.DoesNotExist:
        return redirect('home')
    poll_id.delete()
    print("Delete successfull")
    return redirect('home')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request,'Username taken')
            return redirect('register')


        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect('register')

        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('login')

        return render(request, 'accounts/index.html')
    
    else:
        print('else')
        return render(request,'accounts/register.html')


@login_required(login_url='login')
def Logout(request):
    auth.logout(request)
    return redirect('home')
