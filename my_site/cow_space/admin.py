from django.contrib import admin
from cow_space.models import Member, SeatBooking, TopupLog, Zone


class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'money']
    extra = 1


class SeatBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'zone', 'time_in',
                    'time_out', 'total_price', 'create_date', 'create_by']
    extra = 1


class TopupLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'amount', 'topup_date', 'topup_by']
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'first_name' ,]
    extra = 1


class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'money']
    extra = 1


# Register your models here.
#admin.site.unregister(User)

admin.site.register(Member, MemberAdmin)
admin.site.register(SeatBooking)
admin.site.register(TopupLog)
admin.site.register(Zone)

