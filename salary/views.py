# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.admin import site
from django import forms

from functools import wraps, partial
from StringIO import StringIO

from .models import *

from xlwt import Workbook, easyxf

def need_login(f):
    @wraps(f)
    def wrapper(request, *a, **k):
        if not site.has_permission(request):
            return site.login(request)
        return f(request, *a, **k)
    return wrapper

report_types = {}
def report(type_name):
    def wrapper(f):
        f = need_login(f)
        report_types[f.__name__] = (f, type_name)
        return f
    return wrapper

@report(u'全部合同')
def contracts(request, start, finish):
    wb = Workbook(style_compression=2)
    s = wb.add_sheet(u'全部合同')
    s.panes_frozen = True
    s.horz_split_pos = 2

    # header
    ss = u'''
        pattern: pattern solid, fore_color %d;
        align: horizontal center, vertical center;
        font: bold %s, name 微软雅黑, height 180;
        borders: left thin, right thin, top thin, bottom thin;
    '''
    stb = []
    st = []
    cell_styles = []
    colors = [1, 41, 43, 47, 44]
    for i in colors:
        stb.append(easyxf(ss % (i, 'True')))
        st.append(easyxf(ss % (i, 'False')))

    wm = s.write_merge
    w = s.write

    def counter():
        class ctr: pass
        ctr.value = -1
        def _ctr(add=True):
            if add: ctr.value += 1
            return ctr.value
        return _ctr

    c = counter()

    wm(0, 1, c(), c(0), u'序号', stb[0])
    cell_styles.append(st[0])

    wm(0, 1, c(), c(0), u'客户姓名', stb[1])
    cell_styles.append(st[1])

    wm(0, 1, c(), c(0), u'设计师', stb[2])
    wm(0, 1, c(), c(0), u'业务员', stb[2])
    cell_styles.extend([st[2]]*2)

    l = c(0) + 1
    w(1, c(), u'合同签订日期', stb[3])
    w(1, c(), u'合同开工日期', stb[3])
    w(1, c(), u'合同竣工日期', stb[3])
    w(1, c(), u'实际竣工日期', stb[3])
    cell_styles.extend(
        [easyxf(ss % (colors[3], 'False'), num_format_str=u'YYYY-MM-DD')] * 4
    )
    w(1, c(), u'直接费', stb[3])
    w(1, c(), u'直接费（折）', stb[3])
    w(1, c(), u'直接费(实际)', stb[3])
    w(1, c(), u'管理费', stb[3])
    w(1, c(), u'管理费（折）', stb[3])
    w(1, c(), u'设计费', stb[3])
    w(1, c(), u'设计费（折）', stb[3])
    w(1, c(), u'主材费', stb[3])
    w(1, c(), u'主材费(实际)', stb[3])
    wm(0, 0, l, c(0), u'合同基本信息', stb[3])
    cell_styles.extend([st[3]]*(c(0)-l+1-4))

    l = c(0) + 1
    w(1, c(), u'已付定金', stb[4])
    w(1, c(), u'已付设计费', stb[4])
    w(1, c(), u'已付管理费', stb[4])
    w(1, c(), u'已付首期款', stb[4])
    w(1, c(), u'已付二期款', stb[4])
    w(1, c(), u'已付三期款', stb[4])
    w(1, c(), u'已付尾款', stb[4])
    wm(0, 0, l, c(0), u'客户付款状态', stb[4])
    cell_styles.extend([st[4]]*(c(0)-l+1))

    l = c(0) + 1
    datexf = easyxf(ss % (colors[1], 'False'), num_format_str=u'YYYY-MM-DD')
    w(1, c(), u'水电预算', stb[1])
    w(1, c(), u'木工预算', stb[1])
    w(1, c(), u'瓦工预算', stb[1])
    w(1, c(), u'油漆预算', stb[1])
    cell_styles.extend([st[1]]*4)
    w(1, c(), u'水电人工费首期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'水电人工费二期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'木工人工费首期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'木工人工费二期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'瓦工人工费首期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'瓦工人工费二期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'油漆工人工费首期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    w(1, c(), u'油漆工人工费二期款', stb[1])
    w(1, c(), u'发放时间', stb[1])
    cell_styles.extend([st[1], datexf]*8)
    w(1, c(), u'水电材料费', stb[1])
    w(1, c(), u'木工材料费', stb[1])
    w(1, c(), u'瓦工材料费', stb[1])
    w(1, c(), u'油漆材料费', stb[1])
    cell_styles.extend([st[1]]*4)
    wm(0, 0, l, c(0), u'合同支出', stb[1])

    l = c(0) + 1
    w(1, c(), u'设计费发放', stb[2])
    w(1, c(), u'设计师提点', stb[2])
    w(1, c(), u'业务员提点', stb[2])
    w(1, c(), u'组长提点', stb[2])
    w(1, c(), u'工程管理员提点', stb[2])
    w(1, c(), u'工程经理提点', stb[2])
    w(1, c(), u'材料经理提点', stb[2])
    w(1, c(), u'市场经理提点', stb[2])
    w(1, c(), u'设计经理提点', stb[2])
    wm(0, 0, l, c(0), u'合同提点', stb[2])
    cell_styles.extend([st[2]]*(c(0)-l+1))
    # end header

    for i, con in enumerate(Contract.objects.filter(date_signed__range=[start, finish]).select_related(depth=1).order_by('-id')):
        l = [
            con.id,
            con.customer.name,
            con.designer.name,
            con.salesman.name,

            con.date_signed,
            con.date_start,
            con.date_finish,
            con.date_finish_actual,
            con.directfee,
            con.directfee_discount,
            con.directfee_actual,
            con.managefee,
            con.managefee_discount,
            con.designfee,
            con.designfee_discount,
            con.materialfee,
            con.materialfee_actual,

            con.earnest_paid,
            con.designfee_paid,
            con.managefee_paid,
            con.generalfee1_paid,
            con.generalfee2_paid,
            con.generalfee3_paid,
            con.generalfee4_paid,
        ]

        from collections import defaultdict as dd
        class dummy(object):
            def __getattribute__(self, v):
                return None
        dummy = dummy()
        e = {j:dummy for j in range(1, 20)}
        for exp in con.expenditures.all():
            e[exp.type] = exp

        l.extend([
            e[1].budget, e[2].budget, e[3].budget, e[4].budget,
            e[1].amount1, e[1].granttime1, e[1].amount2, e[1].granttime2,
            e[2].amount1, e[2].granttime1, e[2].amount2, e[2].granttime2,
            e[3].amount1, e[3].granttime1, e[3].amount2, e[3].granttime2,
            e[4].amount1, e[4].granttime1, e[4].amount2, e[4].granttime2,
            e[1].materialfee, e[2].materialfee, e[3].materialfee, e[4].materialfee,
        ])

        c = {j:dummy for j in xrange(1, 20)}
        for com in con.commissions.all():
            c[com.type] = com

        if c[1].amount is None:
            designer_com = None
        else:
            designer_com = c[1].amount
            if c[2].amount is not None:
                designer_com += c[2].amount

        l.extend([
            c[3].amount,
            designer_com,
            c[4].amount,
            c[8].amount,
            c[6].amount,
            c[5].amount,
            c[7].amount,
            c[9].amount,
            c[10].amount,
        ])

        for j, v in enumerate(l):
            if v is not None:
                w(i+2, j, v, cell_styles[j])

    f = StringIO()
    wb.save(f)
    rsp = HttpResponse(f.getvalue(), content_type='application/vnd.ms-excel')
    rsp['Content-Disposition'] = 'attachment; filename=contracts.xls'
    return rsp

def _last_month(dt):
    from datetime import date
    d = date.today()
    y, m = d.year, d.month
    m -= dt
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, 1).strftime('%Y-%m-%d')

class ReportForm(forms.Form):
    report_type = forms.ChoiceField(
        label=u'报表类型',
        choices=[(type, name) for type, (_, name) in report_types.items()],
    )
    date_start = forms.DateField(label=u'开始日期', initial=partial(_last_month, 2))
    date_finish = forms.DateField(label=u'结束日期', initial=partial(_last_month, 1))

@need_login
def reports(request):
    form = ReportForm(request.POST)
    if not form.is_valid():
        return render_to_response('index.html', RequestContext(request, dict(report_form=form)))

    meth = report_types[form.cleaned_data['report_type']][0]
    start = form.cleaned_data['date_start']
    finish = form.cleaned_data['date_finish']
    return meth(request, start, finish)

@need_login
def index(request):
    return render_to_response('index.html', RequestContext(request, dict(report_form=ReportForm())))
