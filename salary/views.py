# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.admin import site

from functools import wraps
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

@need_login
def index(request):
    return render_to_response('index.html', RequestContext(request))

report_types = {}
def report(type_name):
    def wrapper(f):
        f = need_login(f)
        report_types[f.__name__] = (f, type_name)
        return f
    return wrapper

@report(u'全部合同')
def contracts(request):
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
        [easyxf(ss % (colors[3], 'False'), num_format_str=u'YYYY年MM月DD日')] * 4
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
    datexf = easyxf(ss % (colors[1], 'False'), num_format_str=u'YYYY年MM月DD日')
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
    wm(0, 0, l, c(0), u'合同提点', stb[2])
    cell_styles.extend([st[2]]*(c(0)-l+1))
    # end header

    for i, con in enumerate(Contract.objects.select_related(depth=1).order_by('-id')):
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
        '''
            1, 2, 3, 4,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f',
            4, 3, 2, 1,

            11, 22, 33, 44, 55, 66, 77
        ]
        '''

        from collections import defaultdict as dd
        class dummy(object):
            def __getattribute__(self, v):
                return None
        exp = {i:dummy() for i in range(1, 5)}
        for e in con.expenditures.all():
            exp[e.type] = e

        l.extend([
            exp[1].budget, exp[2].budget, exp[3].budget, exp[4].budget,
            exp[1].amount1, exp[1].granttime1, exp[1].amount2, exp[1].granttime2,
            exp[2].amount1, exp[2].granttime1, exp[2].amount2, exp[2].granttime2,
            exp[3].amount1, exp[3].granttime1, exp[3].amount2, exp[3].granttime2,
            exp[4].amount1, exp[4].granttime1, exp[4].amount2, exp[4].granttime2,
            exp[1].materialfee, exp[2].materialfee, exp[3].materialfee, exp[4].materialfee,
        ])

        l.extend(range(7))



        for j, v in enumerate(l):
            w(i+2, j, v, cell_styles[j])

    f = StringIO()
    wb.save(f)
    rsp = HttpResponse(f.getvalue(), content_type='application/vnd.ms-excel')
    rsp['Content-Disposition'] = 'attachment; filename=contracts.xls'
    return rsp

@need_login
def reports(request, type):
    try:
        f = report_types[type]
    except KeyError:
        raise Http404()
    return f[0](request)
