# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.admin import site
from django import forms
from django.db import transaction
from django.db.models import Q, F, Sum
from django.core.exceptions import ValidationError

from functools import wraps, partial
from StringIO import StringIO
from decimal import Decimal

from .models import *

from xlwt import Workbook, easyxf

def need_login(f):
    @wraps(f)
    def wrapper(request, *a, **k):
        if not site.has_permission(request):
            return site.login(request)
        return f(request, *a, **k)
    return wrapper

def both_end(year, month):
    from datetime import date

    month -= 1
    while month < 0:
        year -= 1
        month += 12
    while month > 11:
        year += 1
        month -= 12
    month += 1

    start = date(year, month, 1)

    for day in xrange(31, 27, -1):
        try:
            stop = date(start.year, start.month, day)
            break
        except ValueError:
            pass

    return start, stop

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
    w(1, c(), u'实际开工日期', stb[3])
    w(1, c(), u'实际竣工日期', stb[3])
    cell_styles.extend(
        [easyxf(ss % (colors[3], 'False'), num_format_str=u'YYYY-MM-DD')] * 5
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
    cell_styles.extend([st[3]]*(c(0)-l+1-5))

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
    w(1, c(), u'设计师主材返点', stb[2])
    w(1, c(), u'业务员提点', stb[2])
    w(1, c(), u'工程管理员提点', stb[2])
    w(1, c(), u'工程经理提点', stb[2])
    w(1, c(), u'材料经理提点', stb[2])
    wm(0, 0, l, c(0), u'合同提点', stb[2])
    cell_styles.extend([st[2]]*(c(0)-l+1))
    # end header

    qs = Contract.objects.filter(
        date_signed__range=[start, finish]
    ).select_related(depth=1).order_by('-id')

    for i, con in enumerate(qs):
        l = [
            con.id,
            con.customer.name,
            con.designer.name,
            con.salesman.name,

            con.date_signed,
            con.date_start,
            con.date_finish,
            con.date_start_actual,
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

        WE, C, B, P = (
            Expenditure.TYPE.WATERELECTRIC,
            Expenditure.TYPE.CARPENTER,
            Expenditure.TYPE.BRICKLAYER,
            Expenditure.TYPE.PAINTER,
        )
        l.extend([
            e[WE].budget, e[C].budget, e[B].budget, e[P].budget,
            e[WE].amount1, e[WE].granttime1, e[WE].amount2, e[WE].granttime2,
            e[C].amount1, e[C].granttime1, e[C].amount2, e[C].granttime2,
            e[B].amount1, e[B].granttime1, e[B].amount2, e[B].granttime2,
            e[P].amount1, e[P].granttime1, e[P].amount2, e[P].granttime2,
            e[WE].materialfee, e[C].materialfee, e[B].materialfee, e[P].materialfee,
        ])
        del WE, C, B, P

        T = Commission.TYPE
        c = {j:dummy for j in xrange(1, 20)}
        for com in con.commissions.all():
            c[com.type] = com

        def mysum(*cats):
            al = [c[i].amount for i in cats]
            if all(i is None for i in al):
                return None
            al = [i for i in al if i is not None]
            return sum(al)

        l.extend([
            c[T.DESIGNFEE].amount,
            mysum(T.DESIGNER1, T.DESIGNER2),
            c[T.DESIGNERPM].amount,
            c[T.SALESMAN].amount,
            mysum(T.PROJADMINSTART, T.PROJADMINFINISH),
            c[T.PROJMGR].amount,
            c[T.MATERIALMGR].amount,
        ])

        for j, v in enumerate(l):
            if v is not None:
                w(i+2, j, v, cell_styles[j])

    f = StringIO()
    wb.save(f)
    rsp = HttpResponse(f.getvalue(), content_type='application/vnd.ms-excel')
    rsp['Content-Disposition'] = 'attachment; filename=contracts.xls'
    return rsp

@report(u'工资表')
def salary(request, start, stop):
    from datetime import date
    if not (start.year == stop.year) and (start.month == stop.month):
        return render_to_response('error.html', RequestContext(request, dict(text=u'工资表只能按月输出报表')))

    start, stop = both_end(start.year, start.month)

    def builditer(seq):
        def _genfunc():
            for i in seq:
                yield i

        _gen = _genfunc()
        def _wrapper():
            return _gen.next()

        return _wrapper

    from itertools import count, cycle

    colortbl = []
    colors = [41, 47, 43, 44]
    xftemplate = u'''
        pattern: pattern solid, fore_color %d;
        align: horizontal center, vertical center;
        font: bold %s, name 微软雅黑, height 180;
        borders: left thin, right thin, top thin, bottom thin;
    '''
    for i in colors:
        norm = easyxf(xftemplate % (i, False))
        bold = easyxf(xftemplate % (i, True))
        colortbl.append((norm, bold))

    wb = Workbook(style_compression=2)

    for staff in Staff.objects.all():
        sheet = wb.add_sheet(staff.name)
        line = builditer(count(0))
        color = builditer(cycle(colortbl))
        w = sheet.write
        wm = sheet.write_merge

        total = Decimal('0')

        # 基本信息
        line()
        ln = line()
        norm, bold = color()

        cols = [u'姓名', u'职位', u'考核月份', u'基本工资']
        for i, colname in enumerate(cols):
            w(ln, i, colname, bold)
        wm(ln-1, ln-1, 0, len(cols)-1, u'基本信息', bold)
        ln = line()
        col = builditer(count(0))
        w(ln, col(), staff.name, norm)
        w(ln, col(), staff.get_position_display(), norm)
        w(ln, col(), u'%s-%s' % (start.year, start.month), norm)
        w(ln, col(), staff.basesalary, norm)
        total += staff.basesalary
        line()

        # 职位相关
        cols = vals= []
        norm, bold = color()
        if staff.position == Staff.POSITION.SALESMAN:
            cols = [u'邀约客户', u'基本工资浮动']
            cnt = staff.contracts_salesman.filter(
                customer__arrive_time__range=(start, stop)
            ).count()
            c = cnt - 8
            adj = c * 40 if c >= 0 else c * 80
            total += adj
            vals = [cnt, adj]
        elif staff.position in (Staff.POSITION.DESIGNER, Staff.POSITION.DZLEADER):
            cols = [u'当月签单额', u'基本工资浮动']
            _sum = staff.contracts_designer.filter(
                date_signed__range=(start, stop)
            ).aggregate(sum=Sum('directfee_discount'))['sum']
            while True:
                if _sum < 30000: adj = 0; break
                elif _sum < 80000: adj = 400; break
                elif _sum < 150000: adj = 700; break
                elif _sum < 200000: adj = 1200; break
                else: adj = 1700; break
            vals = [_sum, adj]
            total += adj

        for i, (head, val) in enumerate(zip(cols, vals)):
            w(1, 4+i, head, bold)
            w(2, 4+i, val, norm)

        if len(cols):
            wm(0, 0, 4, 4+len(cols)-1, u'职位相关', bold)

        #  提点
        norm, bold = color()
        headerln = line()

        cols = [u'合同', u'类型', u'数额', u'说明']
        ln = line()
        for i, colname in enumerate(cols):
            w(ln, i, colname, bold)

        comsum = Decimal('0')
        coms = staff.commissions.filter(
            granttime__range=both_end(start.year, start.month+1)
        ).order_by('contract__id', 'type')

        for com in coms:
            ln = line()
            col = builditer(count(0))
            w(ln, col(), u'%s' % com.contract, norm)
            w(ln, col(), com.get_type_display(), norm)
            w(ln, col(), com.amount, norm)
            w(ln, col(), com.tag, norm)
            comsum += com.amount

        total += comsum

        ln = line()
        w(ln, 0, u'合计', bold)
        wm(ln, ln, 1, len(cols)-1, comsum, norm)

        wm(headerln, headerln, 0, len(cols)-1, u'合同提点', bold)
        line()

        # 其他
        norm, bold = color()
        headerln = line()

        ln = line()
        cols = [u'发放原因', u'数额']
        for i, colname in enumerate(cols):
            w(ln, i, colname, bold)

        oss = staff.othersalaries.filter(
            granttime__range=both_end(start.year, start.month)
        )

        ossum = Decimal('0')
        for os in oss:
            ln = line()
            w(ln, 0, os.reason, norm)
            w(ln, 1, os.amount, norm)
            ossum += os.amount
        ln = line()
        w(ln, 0, u'合计', bold)
        w(ln, 1, ossum, norm)
        wm(headerln, headerln, 0, 1, u'其他工资', bold)
        total += ossum
        line()

        # 工资合计
        norm, bold = color()
        ln = line()
        w(ln, 0, u'本月工资合计', bold)
        w(ln, 1, total, norm)
        ln = line()
        w(ln, 0, u'本月工资实发', bold)
        w(ln, 1, total, norm)

    f = StringIO()
    wb.save(f)
    rsp = HttpResponse(f.getvalue(), content_type='application/vnd.ms-excel')
    rsp['Content-Disposition'] = 'attachment; filename=salaries.xls'
    return rsp

def _last_month(dt):
    from datetime import date, timedelta
    d = date.today()
    y, m = d.year, d.month
    m -= 1
    m -= dt
    while m < 0:
        m += 12
        y -= 1
    m += 1
    d = date(y, m, 1)
    if not dt:
        d = d - timedelta(1)
    return d

def _date_granttime():
    import datetime
    t = datetime.date.today()
    return datetime.date(t.year, t.month, 15).strftime('%Y-%m-%d')

class ReportForm(forms.Form):
    report_type = forms.ChoiceField(
        label=u'报表类型',
        choices=[(type, name) for type, (_, name) in report_types.items()],
    )
    date_start = forms.DateField(label=u'开始日期', initial=partial(_last_month, 1))
    date_finish = forms.DateField(label=u'结束日期', initial=partial(_last_month, 0))

def _month():
    return _last_month(1).strftime('%Y-%m')

def _month_validator(v):
    import re
    if not re.match(r'^\d{4}-\d{1,2}$', v):
        raise ValidationError(u'月份格式错误')

class AutoFillForm(forms.Form):
    month = forms.CharField(label=u'填写月份', initial=_month, validators=[_month_validator])
    date_granttime = forms.DateField(label=u'提点发放日期', initial=_date_granttime)

@need_login
def reports(request):
    form = ReportForm(request.POST)
    if not form.is_valid():
        data = dict(report_form=form, autofill_form=AutoFillForm())
        return render_to_response('index.html', RequestContext(request, data))

    meth = report_types[form.cleaned_data['report_type']][0]
    start = form.cleaned_data['date_start']
    finish = form.cleaned_data['date_finish']
    return meth(request, start, finish)

@need_login
@transaction.commit_on_success
def autofill(request):
    form = AutoFillForm(request.POST)
    if not form.is_valid():
        return render_to_response('error.html', dict(text=u'你的输入有错误，请返回重新来过'))

    import re
    monthstr = form.cleaned_data['month']
    year, month = re.match(r'^(\d{4})-(\d{1,2})$', monthstr).groups()
    year, month = int(year), int(month)

    from datetime import date

    start = date(year, month, 1)

    for day in xrange(31, 27, -1):
        try:
            stop = date(year, month, day)
            break
        except ValueError:
            pass

    granttime = form.cleaned_data['date_granttime']

    log = []

    # 设计师主材返点：所有实际竣工时间在7月内的合同，SUM（所有主材的实际数量*实际单价*提点比例）
    cl = Contract.objects.filter(
        date_finish_actual__range=(start, stop),
        designer__isnull=False
    ).select_related(depth=1)

    for c in cl:
        pms = c.pm_expenditures.filter(type_actual__isnull=False)
        qs = c.commissions.filter(type=Commission.TYPE.DESIGNERPM, staff=c.designer)
        if qs.exists():
            log.append(u'合同 %s 的 设计师主材返点 被自动填写覆盖。' % c)
        qs.delete()

        _sum = sum(pm.unitprice_actual * pm.amount_actual * pm.commission_rate for pm in pms)

        c.commissions.create(
            type = Commission.TYPE.DESIGNERPM,
            amount = _sum,
            granttime = granttime,
            staff = c.designer,
        )
    log.append(u'更新了%d条 设计师主材返点' % len(cl))

    # 设计费：设计费（折） == 已付设计费的，发设计费（折）-面积*3
    cl = Contract.objects.exclude(
        commissions__type=Commission.TYPE.DESIGNFEE
    ).filter(
        designfee_discount__lte=F('designfee_paid')
    )

    for c in cl:
        c.commissions.create(
            type = Commission.TYPE.DESIGNFEE,
            amount = c.designfee_discount - c.area * 3,
            granttime = granttime,
            staff = c.designer,
        )
    log.append(u'更新了%d条 设计费发放' % len(cl))

    # 业务员提点：所有实际开工日期在7月份的，且7月已收首期款不为零，按照业绩分段提点，高折扣另算
    # 设计师、业务员为同一人，不发业务员提点
    # FIXME:7月底，开工，8月15没有付费, 合同就被忽略掉了
    cl = Contract.objects.filter(
        date_start_actual__range=(start, stop),
        generalfee1_paid__gt=0,
        salesman__isnull=False,
    ).exclude(
        salesman=F('designer')
    )

    nc = cl.count()
    nc_actual = 0

    def ratefunc(a):
        if a < 0:
            raise ValueError
        elif a <= 30000:
            return Decimal('0.03')
        elif a <= 80000:
            return Decimal('0.04')
        else:
            return Decimal('0.05')

    def fill(l, rate):
        for c in l:
            qs = c.commissions.filter(type=Commission.TYPE.SALESMAN, staff=c.salesman)
            if qs.exists():
                log.append(u'合同 %s 的 业务员提点 被自动填写覆盖。' % c)
            qs.delete()

            c.commissions.create(
                type = Commission.TYPE.SALESMAN,
                amount = c.directfee_discount * rate,
                granttime = granttime,
                staff = c.salesman,
                tag = u'Rate: %s' % rate
            )

    saleslist = set(c.salesman for c in cl)
    for sales in saleslist:
        mycl = cl.filter(salesman=sales)
        high_discount = []
        normal = []
        for c in mycl:
            if c.directfee_discount / c.directfee >= Decimal('0.9'):
                normal.append(c)
            else:
                high_discount.append(c)
        nc_actual += len(mycl)

        rate = ratefunc(sum(c.directfee_discount for c in normal))

        fill(normal, rate)
        fill(high_discount, Decimal('0.03'))
    del saleslist
    assert nc == nc_actual

    log.append(u'更新了%d条 业务员提点' % nc)
    del ratefunc, fill

    # 工程经理提点：填写直接费（实际结算），并且合同实际竣工日期在7月内的，SUM（直接费实际结算）*0.75%
    cl = Contract.objects.filter(
        date_finish_actual__range=(start, stop),
        directfee_actual__isnull=False,
        projmgr__isnull=False,
    ).select_related(depth=1)

    for c in cl:
        qs = c.commissions.filter(type=Commission.TYPE.PROJMGR, staff=c.projmgr)
        if qs.exists():
            log.append(u'合同 %s 的 工程经理提点 被自动填写覆盖。' % c)
        qs.delete()

        c.commissions.create(
            type = Commission.TYPE.PROJMGR,
            amount = c.directfee_actual * Decimal('0.0075'),
            granttime = granttime,
            staff = c.projmgr,
        )
    log.append(u'更新了%d条 工程经理提点' % len(cl))

    # 工程管理员开工提点：COUNT（填写了实际开工日期，并且实际开工日期在7月以内的）*100
    cl = Contract.objects.filter(
        date_start_actual__range=(start, stop),
        projadmin__isnull=False,
    )

    for c in cl:
        qs = c.commissions.filter(type=Commission.TYPE.PROJADMINSTART, staff=c.projadmin)
        if qs.exists():
            log.append(u'合同 %s 的 工程管理员开工提点 被自动填写覆盖。' % c)
        qs.delete()

        c.commissions.create(
            type = Commission.TYPE.PROJADMINSTART,
            amount = 100,
            granttime = granttime,
            staff = c.projadmin,
        )
    log.append(u'更新了%d条 工程管理员开工提点' % len(cl))

    # 工程管理员结算提点：COUNT（填写了实际竣工日期，并且实际开工日期在7月以内的）*100
    cl = Contract.objects.filter(
        date_finish_actual__range=(start, stop),
        projadmin__isnull=False,
    )

    for c in cl:
        qs = c.commissions.filter(type=Commission.TYPE.PROJADMINFINISH, staff=c.projadmin)
        if qs.exists():
            log.append(u'合同 %s 的 工程管理员结算提点 被自动填写覆盖。' % c)
        qs.delete()

        c.commissions.create(
            type = Commission.TYPE.PROJADMINFINISH,
            amount = 100,
            granttime = granttime,
            staff = c.projadmin,
        )
    log.append(u'更新了%d条 工程管理员结算提点' % len(cl))

    # 材料经理提点：填写了实际开工日期，并且实际开工日期在7月以内的，全包200，非全包100
    cl = Contract.objects.filter(
        date_start_actual__range=(start, stop),
        materialmgr__isnull=False,
    )

    for c in cl:
        qs = c.commissions.filter(type=Commission.TYPE.MATERIALMGR, staff=c.materialmgr)
        if qs.exists():
            log.append(u'合同 %s 的 材料经理提点 被自动填写覆盖。' % c)
        qs.delete()

        c.commissions.create(
            type = Commission.TYPE.MATERIALMGR,
            amount = 200 if c.all_included else 100,
            granttime = granttime,
            staff = c.projmgr,
        )
    log.append(u'更新了%d条 材料经理提点' % len(cl))

    def ratefunc(a):
        if a < 0:
            raise ValueError
        elif a <= 30000:
            return Decimal('0.03')
        elif a <= 80000:
            return Decimal('0.04')
        elif a <= 150000:
            return Decimal('0.05')
        elif a <= 200000:
            return Decimal('0.06')
        else:
            return Decimal('0.07')

    # 设计师提点1： 设计费(折） > 0： 0， 设计费（折） == 0：直接费折*rate/2, 合同开工后发放
    cl = Contract.objects.filter(
        date_start_actual__range=(start, stop),
        designer__isnull=False,
    )

    nc = cl.count()
    nc_actual = 0

    def fill(l, rate):
        for c in l:
            if c.designfee_discount > 0: continue
            qs = c.commissions.filter(type=Commission.TYPE.DESIGNER1, staff=c.designer)
            if qs.exists():
                log.append(u'合同 %s 的 设计师提点1 被自动填写覆盖。' % c)
            qs.delete()

            c.commissions.create(
                type = Commission.TYPE.DESIGNER1,
                amount = c.directfee_discount * rate / 2,
                granttime = granttime,
                staff = c.designer,
                tag = u'Rate: %s' % rate
            )

    dzlist = set(c.designer for c in cl)
    for dz in dzlist:
        mycl = cl.filter(designer=dz)
        high_discount = []
        normal = []
        for c in mycl:
            if c.directfee_discount / c.directfee >= Decimal('0.9'):
                normal.append(c)
            else:
                high_discount.append(c)
        nc_actual += len(mycl)

        _sum = sum(c.directfee_discount for c in normal)
        rate = ratefunc(sum(c.directfee_discount for c in normal))

        fill(normal, rate)
        fill(high_discount, Decimal('0.03'))
    assert nc == nc_actual
    log.append(u'更新了%d条 设计师提点1' % nc)
    del fill

    # 设计师提点2： 设计费 > 0： 直接费（实际）*rate， 设计费 == 0：直接费（实际）*rate - 提点1, 合同竣工后发放
    cl = Contract.objects.filter(
        date_finish_actual__range =(start, stop),
        designer__isnull=False,
    ).select_related(depth=1)

    from datetime import date, timedelta
    d09 = Decimal('0.9')
    for c in cl:
        if c.directfee_discount / c.directfee >= d09:
            d = c.date_start_actual
            y, m = d.year, d.month
            _start = date(y, m, 1)
            m += 1
            if m > 12:
                m = 1
                y += 1
            _stop = date(y, m, 1) - timedelta(1)

            mycl = Contract.objects.filter(
                date_start_actual__range=(_start, _stop),
                designer=c.designer,
            )

            _sum = sum(
                i.directfee_discount for i in mycl
                if i.directfee_discount / i.directfee >= d09
            )
            rate = ratefunc(_sum)
        else:
            rate = Decimal('0.03')

        qs = c.commissions.filter(type=Commission.TYPE.DESIGNER2, staff=c.designer)
        if qs.exists():
            log.append(u'合同 %s 的 设计师提点2 被自动填写覆盖。' % c)
        qs.delete()

        if c.designfee_discount > 0:
            adj = 0
        else:
            com = c.commissions.get(type=Commission.TYPE.DESIGNER1, staff=c.designer)
            adj = com.amount

        c.commissions.create(
            type = Commission.TYPE.DESIGNER2,
            amount = c.directfee_actual * rate - adj,
            granttime = granttime,
            staff = c.designer,
            tag = u'Rate: %s' % rate
        )

    log.append(u'更新了%d条 设计师提点2' % len(cl))

    return render_to_response('message.html', dict(text='\n'.join(log)))

@need_login
def index(request):
    data = dict(report_form=ReportForm(), autofill_form=AutoFillForm())
    return render_to_response('index.html', RequestContext(request, data))
