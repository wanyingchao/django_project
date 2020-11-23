# 调用自己写的文件,不能直接写device_sql,报错没有device_sql这个model
from all_app.device_sql import *
import xlrd
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from all_app.models import *
# Create your views here.


def hello_word(request):
    return HttpResponse('hello word')


def get_index_page(request):
    return render(request, 'index.html')


def get_device_index_page(request):
    return render(request, 'device_index.html')


def get_pop_index_page(request):
    return render(request, 'pop_index.html')


def get_signal_index_page(request):
    return render(request, 'signal_index.html')


def get_statics_results_page(request):
    return render(request, 'statics_results.html')


def select(request):
    sql = "select * from name where id in (5, 4, 3) order by id asc;"
    results = MySql().select(sql)
    # 使用JsonResponse解决输出多个中文乱码的问题
    return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})


def insert(request):
    sql = "insert into name (id,xm,pwd,xb,csny) values (%s, %s, %s, %s, %s);"
    data = ('5', '溜溜', '123456', '男', '1998-06-05')
    MySql().insert(sql, data)
    return HttpResponse(200)


def pop_all(request):
    try:
        files = request.FILES['excel']  # 获取上传的文件
        file = files.read()  # 读取文件
        text = []
        wb = xlrd.open_workbook(filename=None, file_contents=file)
        sheet = wb.sheet_by_index(0)
        cols = sheet.col_values(0)
        for deviceid in cols:
            PopDjango().pop_loop(deviceid, text)
        return render(request, 'pop_results.html', {
            'text': text
        })
    except:
        text = []
        slots_list = request.POST.get('slot')
        deviceid = request.POST.get('data')
        if len(slots_list) == 0:
            PopDjango().pop_loop(deviceid, text)
        else:
            slots = slots_list.split(',')
            for slot in slots:
                PopDjango().pop_interface(deviceid, slot, text)
        # 需要在同级目录创建templates文件存放index.html
        return render(request, 'pop_results.html', {
                'text': text
            })


def device_detail(request):
    try:
        files = request.FILES['device_id']  # 获取上传的文件
        file = files.read()  # 读取文件
        wb = xlrd.open_workbook(filename=None, file_contents=file)
        sheet = wb.sheet_by_index(0)
        device_id_list = sheet.col_values(0)
        device_id_str = "','".join(device_id_list)
        device_id = "'" + device_id_str + "'"
    except:
        device_id = "''"
    try:
        agent_phone = request.POST.get('agent_phone')
    except:
        agent_phone = ''
    try:
        business_phone = request.POST.get('business_phone')
    except:
        business_phone = ''
    try:
        device_one = request.POST.get('device_one')
    except:
        device_one = ''
    try:
        staff_name = request.POST.get('staff_name')
    except:
        staff_name = ''
    sql = device_sql(agent_phone, business_phone, device_id, device_one, staff_name)
    results_list = MySql().select(sql)
    # 判断，如果没有查询到值，抛异常
    if results_list:
        results_keys = results_list[0].keys()
        return render(request, 'device_results.html', {
            'results_list': results_list,
            'results_keys': results_keys
        })
    else:
        return render(request, 'error.html', {
            'text': '没有查到任何信息!'
        })


def device_statics(request):
    result_bd_6_sum = MySql().select(device_bd_6_sum())
    result_agent_6_sum = MySql().select(device_agent_6_sum())
    result_storage_6_sum = MySql().select(device_storage_6_sum())
    result_bd_12_sum = MySql().select(device_bd_12_sum())
    result_agent_12_sum = MySql().select(device_agent_12_sum())
    result_storage_12_sum = MySql().select(device_storage_12_sum())
    results = [result_bd_6_sum, result_bd_12_sum, result_agent_6_sum, result_agent_12_sum, result_storage_6_sum, result_storage_12_sum]

    return render(request, 'statics_results.html', {
        'results': results,
    })


def select_signal(request):
    deviceid = request.POST.get('deviceid')
    results = SelectSignal().select_signal(deviceid)
    signal = results.get('data')
    message = results.get('message')
    return render(request, 'signal_results.html', {
        'signal': signal,
        'message': message,
        'deviceid': deviceid
    })
