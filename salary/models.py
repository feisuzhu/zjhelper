# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Staff(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"员工"

    GENDER_CHOICES = (
        (1, u'男'),
        (2, u'女'),
        #(3, u'秀吉'),
    )

    name = models.CharField(u"姓名", max_length=10)
    gender = models.IntegerField('性别', choices=GENDER_CHOICES)
    position = models.CharField(u'职位', max_length=10)
    basesalary = models.DecimalField(u'基本工资', max_digits=8, decimal_places=2)

    def __unicode__(self):
        return self.name

class Customer(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"客户"

    name = models.CharField(u'客户姓名', max_length=10)
    phone = models.CharField(u'电话', max_length=20)
    arrive_time = models.DateField(u'到店时间')
    source = models.CharField(u'客户来源', max_length=20)
    region = models.CharField(u'区域', max_length=20)
    salesman = models.ForeignKey(Staff, verbose_name=u'接待业务员', related_name='customers_salesman')
    designer = models.ForeignKey(Staff, verbose_name=u'接待设计师', related_name='customers_designer')

    def __unicode__(self):
        return self.name

class CustomerComment(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"客户备注"

    customer = models.ForeignKey(Customer, verbose_name=u'客户', related_name='comments')
    date = models.DateField(u'备注时间')
    text = models.TextField(u'备注内容')

    def __unicode__(self):
        return u'%s - 备注内容' % self.name

class Contract(models.Model):

    class Meta:
        verbose_name_plural = verbose_name = u'合同'

    customer = models.ForeignKey(Customer, verbose_name=u'客户', related_name='contracts')
    address = models.CharField(u'工程地址', max_length=60)
    designer = models.ForeignKey(Staff, verbose_name = u'设计师', related_name = 'contracts_designer')
    salesman = models.ForeignKey(Staff, verbose_name = u'业务人员', related_name = 'contracts_salesman')
    date_signed = models.DateField(u'合同签订日期')
    date_start = models.DateField(u'合同开工日期', null=True, blank=True)
    date_finish = models.DateField(u'合同竣工日期', null=True, blank=True)
    directfee = models.DecimalField(u'直接费', max_digits=11, decimal_places=2)
    directfee_discount = models.DecimalField(u'直接费（折）', max_digits=11, decimal_places=2)
    managefee = models.DecimalField(u'管理费', max_digits=11, decimal_places=2)
    managefee_discount = models.DecimalField(u'管理费（折）', max_digits=11, decimal_places=2)
    designfee = models.DecimalField(u'设计费', max_digits=11, decimal_places=2)
    designfee_discount = models.DecimalField(u'设计费（折）', max_digits=11, decimal_places=2)
    materialfee = models.DecimalField(u'主材费', max_digits=11, decimal_places=2)
    directfee_actual = models.DecimalField(u'直接费(实际)', max_digits=11, decimal_places=2, null=True, blank=True)
    materialfee_actual = models.DecimalField(u'主材费(实际)', max_digits=11, decimal_places=2, null=True, blank=True)
    area = models.PositiveIntegerField(u'面积')
    all_included = models.BooleanField(u'全包')

    earnest_paid = models.DecimalField(u'已付定金', max_digits=11, decimal_places=2, null=True, blank=True)
    designfee_paid = models.DecimalField(u'已付设计费', max_digits=11, decimal_places=2, null=True, blank=True)
    managefee_paid = models.DecimalField(u'已付管理费', max_digits=11, decimal_places=2, null=True, blank=True)
    generalfee1_paid = models.DecimalField(u'已付首期款', max_digits=11, decimal_places=2, null=True, blank=True)
    generalfee2_paid = models.DecimalField(u'已付二期款', max_digits=11, decimal_places=2, null=True, blank=True)
    generalfee3_paid = models.DecimalField(u'已付三期款', max_digits=11, decimal_places=2, null=True, blank=True)
    generalfee4_paid = models.DecimalField(u'已付尾款', max_digits=11, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.customer.name, self.address)

class Commission(models.Model):

    class Meta:
        verbose_name_plural = verbose_name = '合同提点'
        unique_together = ('contract', 'type', 'staff')

    TYPE_CHOICES = (
        (1, u'设计师提点1'),
        (2, u'设计师提点2'),
        (3, u'业务员提点'),
        (4, u'工程经理提点'),
        (5, u'工程管理员提点'),
        (6, u'材料经理提点'),
    )

    contract = models.ForeignKey(Contract, verbose_name = u'合同', related_name = 'commissions')
    type = models.IntegerField(u'类型', choices = TYPE_CHOICES)
    staff = models.ForeignKey(Staff, verbose_name = u'员工', related_name = 'commissions')
    granttime = models.DateField(u'发放时间')
    amount = models.DecimalField(u'数额', max_digits=11, decimal_places=2)

    def __unicode__(self):
        return u'%s 提点' % self.staff.name

class Expenditure(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u"合同支出"
        unique_together = ('contract', 'type')

    TYPE_CHOICES = (
        (1, u'水电'),
        (2, u'木工'),
        (3, u'瓦工'),
        (4, u'油漆工'),
    )

    contract = models.ForeignKey(Contract, verbose_name = u'合同', related_name = 'expenditures')
    type = models.IntegerField(u'类型', choices=TYPE_CHOICES)
    budget = models.DecimalField(u'预算', max_digits=11, decimal_places=2)
    amount1 = models.DecimalField(u'首期款', max_digits=11, decimal_places=2, null=True, blank=True)
    granttime1 = models.DateField(u'首期款发放时间', null=True, blank=True)
    amount2 = models.DecimalField(u'尾款', max_digits=11, decimal_places=2, null=True, blank=True)
    granttime2 = models.DateField(u'尾款发放时间', null=True, blank=True)
    materialfee = models.DecimalField(u'材料费', max_digits=11, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return u'%s - 支出' % self.get_type_display()

class PrimaryMaterial(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u'主材类型'

    name = models.CharField(u'名称', max_length=80)
    reference_price = models.DecimalField(u'参考单价', max_digits=11, decimal_places=2)

    def __unicode__(self):
        return self.name

def percentage_validator(v):
    if not 0.0 <= v <= 1.0:
        raise ValidationError(u'请输入0-1之间的纯小数')

class PMExpenditure(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = u'合同支出 - 主材'
        unique_together = ('contract', 'type')

    contract = models.ForeignKey(Contract, verbose_name = u'合同', related_name = 'pm_expenditures')
    type = models.ForeignKey(PrimaryMaterial, verbose_name = u'主材类型', related_name = 'expenditures')
    unitprice_budget = models.DecimalField(u'主材单价预算', max_digits=11, decimal_places=2)
    amount_budget = models.PositiveIntegerField(u'数量预算')
    unitprice_actual = models.DecimalField(u'实际主材单价', max_digits=11, decimal_places=2, null=True, blank=True)
    amount_actual = models.PositiveIntegerField(u'实际数量', null=True, blank=True)
    commission_rate = models.FloatField(u'设计师返点比例', validators=[percentage_validator])

    def __unicode__(self):
        return u'%s - 合同主材支出' % self.type.name
