from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email',
					'street', 'number_house', 'apartment', 'paid',
					'created', 'updated']   
    # list_display_links = ('first_name',) 
        
	list_filter = ['paid', 'created', 'updated']   
	inlines = [OrderItemInline]
	