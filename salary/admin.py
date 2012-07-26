# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'position', 'basesalary']
    search_fields = ['name']

class CommissionInline(admin.TabularInline):
    model = Commission

class ExpenditureInline(admin.TabularInline):
    model = Expenditure

class PMExpenditureInline(admin.TabularInline):
    model = PMExpenditure

class ContractAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'address', 'designer',
        'bussiness_staff', 'date_signed', 'area',
        'all_included', 'designfee_paid',
    ]
    search_fields = [
        'customer__name', 'address', 'designer__name',
        'bussiness_staff__name',
    ]
    list_filter = [
        'designer', 'bussiness_staff', 'all_included',
    ]
    date_hierarchy = 'date_signed'
    inlines = [
        PMExpenditureInline,
        ExpenditureInline,
        CommissionInline,
    ]

    fieldsets = (
        (u'基本信息', {
            'fields': (
                ('customer', 'address'),
                ('designer', 'bussiness_staff'),
                ('date_signed', 'date_start', 'date_finish'),
                ('directfee', 'directfee_discount', 'directfee_actual'),
                ('managefee', 'managefee_discount'),
                ('designfee', 'designfee_discount'),
                ('materialfee', 'materialfee_actual'),
                ('area', 'all_included'),
            )
        }),
        (u'客户付款状态', {
            'fields': (
                ('earnest_paid', 'designfee_paid', 'managefee_paid'),
                ('generalfee1_paid', 'generalfee2_paid', 'generalfee3_paid', 'generalfee4_paid'),
            )
        }),
    )

class CommissionAdmin(admin.ModelAdmin):
    list_display = [
        'staff', 'type', 'contract', 'granttime', 'amount',
    ]
    list_filter = [
        'type'
    ]

class ExpenditureAdmin(admin.ModelAdmin):
    list_display = [
        'contract', 'type',
        'amount1', 'granttime1', 'amount2', 'granttime2',
        'materialfee',
    ]

    list_filter = [
        'type'
    ]

class PMExpenditureAdmin(admin.ModelAdmin):
    list_display = [
        'contract', 'type', 'unitprice_budget',
        'amount_budget', 'unitprice_actual', 'commission_rate',
        'amount_actual'
    ]

    list_filter = ['type']

class CustomerAdmin(admin.ModelAdmin):
    list_display =[
        'name', 'phone', 'arrive_time', 'source', 'region',
        'receptionist'
    ]

    list_filter = [
        'source', 'region'
    ]

class PrimaryMaterialAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'reference_price'
    ]

reg = admin.site.register
reg(Staff, StaffAdmin)
reg(Customer, CustomerAdmin)
reg(Contract, ContractAdmin)
reg(Commission, CommissionAdmin)
reg(Expenditure, ExpenditureAdmin)
reg(PrimaryMaterial, PrimaryMaterialAdmin)
reg(PMExpenditure, PMExpenditureAdmin)
