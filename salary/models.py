# -*- coding: utf-8 -*-

from django.db import models

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

class Contract(models.Model):

    class Meta:
        verbose_name_plural = verbose_name = u'合同'

    customer_name = models.CharField(u'客户姓名', max_length=10)
    address = models.CharField(u'工程地址', max_length=60)
    designer = models.ForeignKey(Staff, verbose_name = u'设计师', related_name = 'contracts_designer')
    bussiness_staff = models.ForeignKey(Staff, verbose_name = u'业务人员', related_name = 'contracts_bussiness')
    date_signed = models.DateField(u'签订合同日期')
    directfee = models.DecimalField(u'直接费', max_digits=11, decimal_places=2)
    directfee_discount = models.DecimalField(u'直接费（折）', max_digits=11, decimal_places=2)
    managefee = models.DecimalField(u'管理费', max_digits=11, decimal_places=2)
    managefee_discount = models.DecimalField(u'管理费（折）', max_digits=11, decimal_places=2)
    designfee = models.DecimalField(u'设计费', max_digits=11, decimal_places=2)
    designfee_discount = models.DecimalField(u'设计费（折）', max_digits=11, decimal_places=2)
    materialfee = models.DecimalField(u'主材费', max_digits=11, decimal_places=2)
    directfee_actual = models.DecimalField(u'直接费(实际)', max_digits=11, decimal_places=2)
    materialfee_actual = models.DecimalField(u'主材费(实际)', max_digits=11, decimal_places=2)
    area = models.IntegerField(u'面积')
    all_included = models.BooleanField(u'全包')

    earnest_paid = models.DecimalField(u'已付定金', max_digits=11, decimal_places=2)
    designfee_paid = models.DecimalField(u'已付设计费', max_digits=11, decimal_places=2)
    managefee_paid = models.DecimalField(u'已付管理费', max_digits=11, decimal_places=2)
    generalfee1_paid = models.DecimalField(u'已付首期款', max_digits=11, decimal_places=2)
    generalfee2_paid = models.DecimalField(u'已付二期款', max_digits=11, decimal_places=2)
    generalfee3_paid = models.DecimalField(u'已付三期款', max_digits=11, decimal_places=2)
    generalfee4_paid = models.DecimalField(u'已付尾款', max_digits=11, decimal_places=2)

    waterelectricity_budget = models.DecimalField(u'水电项目预算', max_digits=11, decimal_places=2)
    carpenter_budget = models.DecimalField(u'木工预算', max_digits=11, decimal_places=2)
    bricklayer_budget = models.DecimalField(u'瓦工预算', max_digits=11, decimal_places=2)
    painter_budget = models.DecimalField(u'油漆工预算', max_digits=11, decimal_places=2)
    material_budget = models.DecimalField(u'主材预算', max_digits=11, decimal_places=2)

    def __unicode__(self):
        return u'【合同】%s' % self.customer_name

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
        return u'【提点】%s' % self.staff.name

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
    amount1 = models.DecimalField(u'首期款', max_digits=11, decimal_places=2)
    granttime1 = models.DateField(u'首期款发放时间')
    amount2 = models.DecimalField(u'尾款', max_digits=11, decimal_places=2)
    granttime2 = models.DateField(u'尾款发放时间')
    materialfee = models.DecimalField(u'材料费', max_digits=11, decimal_places=2)
