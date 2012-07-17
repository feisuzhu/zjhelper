# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'basesalary']
    search_fields = ['name']

class CommissionInline(admin.TabularInline):
    model = Commission

class ContractAdmin(admin.ModelAdmin):
    list_display = [
        'customer_name', 'address', 'designer',
        'bussiness_staff', 'date_signed', 'area',
        'all_included', 'designfee_paid',
    ]
    search_fields = [
        'customer_name', 'address', 'designer__name',
        'bussiness_staff__name',
    ]
    list_filter = [
        'designer', 'bussiness_staff', 'all_included',
    ]
    inlines = [CommissionInline]

class CommissionAdmin(admin.ModelAdmin):
    list_display = [
        'staff', 'type', 'contract', 'granttime', 'amount',
    ]
    list_filter = [
        'type'
    ]

reg = admin.site.register
reg(Staff, StaffAdmin)
reg(Contract, ContractAdmin)
reg(Commission, CommissionAdmin)
