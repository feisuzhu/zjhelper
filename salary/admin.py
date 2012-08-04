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
        'salesman', 'date_signed', 'area',
        'all_included', 'designfee_paid',
    ]
    search_fields = [
        'customer__name', 'address', 'designer__name',
        'salesman__name',
    ]
    list_filter = [
        'designer', 'salesman', 'all_included',
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
                ('customer', 'address', 'area', 'all_included'),
                ('designer', 'salesman', 'projmgr', 'projadmin', 'materialmgr'),
                ('date_signed', 'date_start', 'date_finish', 'date_start_actual', 'date_finish_actual'),
                ('directfee', 'directfee_discount', 'directfee_actual'),
                ('managefee', 'managefee_discount'),
                ('designfee', 'designfee_discount'),
                ('materialfee', 'materialfee_actual'),
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
        'staff', 'type', 'contract', 'granttime', 'amount', 'tag'
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

class CustomerCommentInline(admin.TabularInline):
    model = CustomerComment

class CustomerAdmin(admin.ModelAdmin):
    list_display =[
        'name', 'phone', 'arrive_time', 'source', 'region',
        'salesman', 'designer'
    ]

    list_filter = [
        'source', 'region'
    ]
    inlines = [CustomerCommentInline]

class PrimaryMaterialAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'reference_price'
    ]

class OtherSalaryAdmin(admin.ModelAdmin):
    list_display = ['staff', 'reason', 'amount', 'granttime']
    date_hierarchy = 'granttime'
    search_fields = ['staff__name', 'reason']
    list_filter = ['staff']

reg = admin.site.register
reg(Staff, StaffAdmin)
reg(Customer, CustomerAdmin)
reg(Contract, ContractAdmin)
reg(Commission, CommissionAdmin)
reg(Expenditure, ExpenditureAdmin)
reg(PrimaryMaterial, PrimaryMaterialAdmin)
reg(PMExpenditure, PMExpenditureAdmin)
reg(OtherSalary, OtherSalaryAdmin)
