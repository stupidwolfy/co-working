from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from cow_space.models import Member, SeatBooking

# Create your views here.


@login_required
@permission_required('cow_space.add_seatbooking')
@permission_required('cow_space.change_seatbooking')
@permission_required('cow_space.view_seatbooking')
@permission_required('cow_space.view_member')
def index(request):
    context = {}

    member_id = request.GET.get('member_id')
    context['member_id'] = member_id

    if member_id:
        try:
            member = Member.objects.get(pk=member_id)
            seat_log = SeatBooking.objects.filter(member=member.pk)
            context['member'] = member
            context['seat_log'] = seat_log
        except Member.DoesNotExist:
            context['error'] = 'Member not found!!'

    return render(request, template_name='cow_space/index.html', context=context)


@login_required
@permission_required('cow_space.change_member')
def topup(request):
    context = {}
    add_mon = None

    if request.method == "GET":
        member_id = request.GET.get('member_id')
        context['member_id'] = member_id
    
    elif request.method == "POST":
        member_id = request.POST.get('member_id')
        add_mon = float(request.POST.get('add_mon'))
        
    if member_id:
        try:
            member = Member.objects.get(pk=member_id)
            context['member'] = member
            context['member_id'] = member_id
        except Member.DoesNotExist:
            context['error'] = 'Member not found!!'
    
    if add_mon:
        mon = member.money
        if mon < -40:
            member.money += add_mon - 20
        else:
            member.money += add_mon
        member.save()

    print(member_id)
    return render(request, template_name='cow_space/topup.html', context=context)


def cow_login(request):
    context = {}

    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=user, password=pwd)

        if user:
            login(request, user)
            return redirect('index')
        else:
            context = {'username': user,
                       'password': pwd,
                       'error': 'Wrong username or password'}

    return render(request, template_name='cow_space/login.html', context=context)


@login_required
def cow_logout(request):
    logout(request)
    return redirect('login')


@login_required
def change_pwd(request):
    context = {}

    if request.method == 'POST':
        user = request.user
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        if pwd1 == pwd2:
            user.set_password(pwd1)
            context['red'] = 'Password not matched!'
        else:
            context['green'] = 'Password changed.'

    return render(request, template_name='change_pwd.html', context=context)


@login_required
@permission_required('cow_space.add_member')
def register(request):
    context = {}

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        #mon = request.POST.get('mon')

        # Check if database had this member
        try:
            check_mem = Member.objects.get(first_name=fname, last_name=lname)
            context['error'] = "This member already exist!"

        except Member.DoesNotExist:
            member = Member.objects.create(
                first_name=fname,
                last_name=lname,
                money=100
            )
            context['member_id'] = member.pk
            member.save()
            return render(request, template_name='cow_space/index.html', context=context)

    return render(request, template_name='cow_space/register.html', context=context)

