# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Staff(models.Model):

    class Meta:
        verbose_name = u"员工"
        verbose_name_plural = u"员工"

    name = models.CharField(u"姓名", max_length=10)
    #gender = models.IntegerField('性别')
    basesalary = models.FloatField(u'基本工资')

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
    directfee_beforediscount = models.DecimalField(u'直接费', max_digits=11, decimal_places=2)
    directfee_afterdiscount = models.DecimalField(u'直接费（折）', max_digits=11, decimal_places=2)
    managefee_beforediscount = models.DecimalField(u'管理费', max_digits=11, decimal_places=2)
    managefee_afterdiscount = models.DecimalField(u'管理费（折）', max_digits=11, decimal_places=2)
    designfee_beforediscount = models.DecimalField(u'设计费', max_digits=11, decimal_places=2)
    designfee_afterdiscount = models.DecimalField(u'设计费（折）', max_digits=11, decimal_places=2)
    area = models.IntegerField(u'面积')
    all_included = models.BooleanField(u'全包')
    designfee_paid = models.DecimalField(u'已付设计费', max_digits=11, decimal_places=2)

    '''
    designer_commission_paid = models.DecimalField('已付设计师提点')
    designer_commission_granttime1 = models.DateField('设计师提点发放时间1')
    designer_commission_granttime2 = models.DateField('设计师提点发放时间2')
    bussiness_commission_paid = models.DecimalField('已付业务员提点')
    bussiness_commission_granttime = models.DateField('业务员提点发放时间')
    '''

    def __unicode__(self):
        return u'【合同】%s' % self.customer_name

class Commission(models.Model):

    class Meta:
        verbose_name_plural = verbose_name = '提点'

    TYPE_CHOICES = (
        (1, u'设计师提点1'),
        (2, u'设计师提点2'),
        (3, u'业务员提点'),
        (4, u'工程经理提点'),
    )

    contract = models.ForeignKey(Contract, verbose_name = u'合同', related_name = 'commissions')
    type = models.IntegerField(u'类型', choices = TYPE_CHOICES)
    staff = models.ForeignKey(Staff, verbose_name = u'员工', related_name = 'commissions')
    granttime = models.DateField(u'发放时间')
    amount = models.DecimalField(u'数额', max_digits=11, decimal_places=2)

    def __unicode__(self):
        return u'【提点】%s' % self.staff.name
