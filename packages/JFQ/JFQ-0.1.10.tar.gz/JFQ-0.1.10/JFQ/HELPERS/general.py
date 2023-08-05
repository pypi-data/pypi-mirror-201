import _datetime
strptime = _datetime.datetime.strptime

def list_results(result,tab="___"):
    if not (isinstance(result,list) or isinstance(result,dict) or isinstance(result,tuple)):
        print(tab,result)
        return
    if isinstance(result,list) or isinstance(result,tuple):
        for listElement in result:
            list_results(listElement)
        return
    for key in result:
        value = result[key]
        if isinstance(value,dict):
            print(tab, key)
            newtab=tab+"___"
            list_results(value,newtab)
        elif isinstance(value,list):
            print(tab, key)
            newtab = tab + "___"
            for listElement in value:
                list_results(listElement,newtab)
        else:
            print(tab,key,":",result[key])

def date_interval_iso(num_days=0,startDateYYYYMMDD="",endDateYYYYMMDD=""):
    '''
    :param num_days:
    :param startDateYYYYMMDD:
    :param endDateYYYYMMDD:
    :return: if either start or end dates are specified, it will return start, end adjusted by num_days. If neither start or end are specified, then it will be number of days from today, backwards
    '''

    def isoformat(date):
        return date.isoformat().replace("-", "")

    delta = _datetime.timedelta(days=num_days)
    if (startDateYYYYMMDD=="" and endDateYYYYMMDD==""):
        today = _datetime.date.today()
        end = isoformat(today)
        start = isoformat(today-delta)
    elif startDateYYYYMMDD!="":
        end = isoformat(strptime(startDateYYYYMMDD,"%Y%m%d")+delta)[0:8]
        start = startDateYYYYMMDD
    elif (startDateYYYYMMDD!="" and endDateYYYYMMDD!=""):
        start = startDateYYYYMMDD
        end = endDateYYYYMMDD
    else:
        start = isoformat(strptime(endDateYYYYMMDD,"%Y%m%d") - delta)[0:8]
        end = endDateYYYYMMDD

    return [start,end]
