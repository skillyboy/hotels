from django.contrib import admin
from . models import Category, Rooms ,Reservation, Payment

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','image')
    
class RoomsAdmin (admin.ModelAdmin):
    list_display = ('id','category','name','price','image','minn','maxn','booked','available','paid_order','description')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id','user','amount','paid_order','description','nights','check_in','check_out')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','user','amount','pay_code','paid_order','first_name','last_name','phone')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Rooms,RoomsAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Payment,PaymentAdmin)