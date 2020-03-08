from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.utils import timezone

from datetime import datetime

from cow_space.models import Member, SeatBooking, TopupLog, Zone
import math

# custom function for search tab
def search_tab(request):
    context = {}

    if request.method == "GET":
        member_id = request.GET.get('member_id')
    elif request.method == "POST":
        member_id = request.POST.get('member_id')

    context['member_id'] = member_id

    member = None
    if member_id:
        try:
            member = Member.objects.get(pk=member_id)
            seat_log = SeatBooking.objects.filter(
                member=member.pk).order_by('-time_in')
            context['member'] = member
            context['seat_log'] = seat_log
        except Member.DoesNotExist:
            context['error'] = 'Member not found!!'
            context['member_id'] = ''
        except ValueError:
            context['error'] = 'Wrong Member ID!!'
            context['member_id'] = ""

    zone_type = Zone.zone_type
    context['zone_type'] = zone_type

    return context, member_id, member


# Create your views here.
@login_required
@permission_required('cow_space.view_seatbooking')
@permission_required('cow_space.view_member')
def index(request):
    context, member_id, member = search_tab(request)

    return render(request, 'cow_space/index.html', context=context)


@login_required
@permission_required('cow_space.add_seatbooking')
def check_in(request):
    context, member_id, member = search_tab(request)
    context['redirect_to'] = 'index'

    if member:
        book = SeatBooking.objects.filter(
            member=member, time_out__isnull=True).order_by('time_in').last()

        if not book:
            zone_type = request.POST.get('zone_type')
            zone = Zone.objects.get(title=zone_type)

            if member.money >= zone.price:
                book = SeatBooking.objects.create(
                    member=member,
                    zone=zone,
                    create_by=request.user
                )
                book.save()
                context['success'] = "Checked In."
            else:
                context['error'] = "Not enougth money!"

        else:
            context['error'] = "Member didn't checked out!"

    else:
        context['error'] = 'Need Member ID!!'

    return render(request, 'cow_space/index.html', context=context)
    # return redirect('index')


@login_required
@permission_required('cow_space.change_seatbooking')
@permission_required('cow_space.change_member')
def check_out(request):
    context, member_id, member = search_tab(request)
    context['redirect_to'] = 'index'

    if member:
        book = SeatBooking.objects.filter(
            member=member, time_out__isnull=True).order_by('time_in').last()

        if book:
            book.time_out = timezone.now()
            price = book.zone.price * \
                math.ceil((book.time_out - book.time_in).seconds/3600)
            member.money -= price
            book.total_price = price

            # print(price)

            book.save()
            member.save()
            context['success'] = "Checked Out."
        else:
            context['error'] = "Member didn't checked in!"

    else:
        context['error'] = 'Need Member ID!!'

    return render(request, 'cow_space/index.html', context=context)
    # return redirect('index')


@login_required
@permission_required('cow_space.change_member')
@permission_required('cow_space.add_topuplog')
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
            tup_log = TopupLog.objects.filter(
                member=member).order_by('-topup_date')
            context['member'] = member
            context['member_id'] = member_id
            context['tup_log'] = tup_log
        except Member.DoesNotExist:
            context['error'] = 'Member not found!!'
            context['member_id'] = None
            return render(request, template_name='cow_space/topup.html', context=context)
        except Member.ValueError:
            context['error'] = 'Wrong Member ID!!'

        if add_mon:
            context['success'] = ""
            if member.money < -40:
                add_mon -= 20
                context['success'] += " (Charged 20฿)"

            member.money += add_mon
            context['success'] = "Top up: " + \
                str(add_mon) + "฿ completed." + context['success']

            tuplog = TopupLog.objects.create(
                member=member,
                amount=add_mon,
                topup_by=request.user
            )

            tuplog.save()
            member.save()

    # print(member_id)
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
    context = {}
    logout(request)
    context['success'] = "Logged out."
    # return redirect('login')
    return render(request, template_name="cow_space/login.html", context=context)


@login_required
@permission_required('cow_space.add_member')
def register(request):
    context, member_id, member = search_tab(request)
    context['redirect_to'] = 'index'

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        if fname and lname:
            # Check if database had this member
            try:
                check_mem = Member.objects.get(
                    first_name=fname, last_name=lname)
                context['error'] = "This member already exist! (ID: " + str(
                    check_mem.pk) + ")"
                context['fname'] = fname
                context['lname'] = lname
                context['member_id'] = check_mem.pk

            except Member.DoesNotExist:
                member = Member.objects.create(
                    first_name=fname,
                    last_name=lname,
                    money=100
                )
                context['member_id'] = member.pk
                context['member'] = member
                member.save()
                context['success'] = "Register compleated! Id: " + \
                    str(member.pk)
                return render(request, template_name='cow_space/index.html', context=context)

    return render(request, template_name='cow_space/register.html', context=context)
