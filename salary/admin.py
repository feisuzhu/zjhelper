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
    date_hierarchy = 'date_signed'
    inlines = [CommissionInline, ExpenditureInline]

    fieldsets = (
        (u'基本信息', {
            'fields': (
                ('customer_name', 'address'),
                ('designer', 'bussiness_staff', 'date_signed'),
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
        (u'合同预算', {
            'fields': (
                ('waterelectricity_budget', 'carpenter_budget', 'bricklayer_budget', 'painter_budget'),
                'material_budget',
            )
        })
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
        'contract', 'type'
    ]

reg = admin.site.register
reg(Staff, StaffAdmin)
reg(Contract, ContractAdmin)
reg(Commission, CommissionAdmin)
reg(Expenditure, ExpenditureAdmin)
