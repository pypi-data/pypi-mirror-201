def minMaxAvg(testlist):
    """
    최소 최댓값을 뺀 평균
    parameter : testlist = 리스트 
    return : 리스트내 값에서 최소 최대값을 뺀 평균을 반환한다
    """
    minValue = min(testlist)
    maxValue = max(testlist)

    print('최소값 : {} ,최대값 :  {}'.format(minValue,maxValue))

    testlist.remove(minValue)
    testlist.remove(maxValue)

    if len(testlist) !=0 :
        average  = sum(testlist) / len(testlist)
    else: 
        pass
    
    return average

def round_desc(in_value,point=2):        
    """
    소수 셋째자리까지 구하는 함수 
    parameter : in_value = float 타입 ,point = int 타입 ->default는 2로 인자를 넣지않으면 2를 사용
    return : 값에 100을 곱하고 int로 캐스팅한뒤 round_point으로 나누어 더블형으로 반환
    """
    round_point = 10 ** point
    change_num = in_value * round_point
    change_num = int(change_num)     
    change_num = change_num / round_point
    return change_num                        #구한 값 return


def WeekPredict(yearMonth,backNum,flag):
    from isoweek import Week
    year = 0
    month = 0
    divdigit = 4
    if type(yearMonth) == str :
        year  = yearMonth[:divdigit]
        month = yearMonth[divdigit:]
        year = int(year)
        month = int(month)
        
    if type(backNum) == str:
        backNum = int(backNum)
    
    if flag == True:
        while backNum >0:
            month = month -1
            backNum = backNum - 1;
            if month == 0:
                year = year - 1
                month = Week.last_week_of_year(year).week  
    else:
        while backNum >0:
            month = month +1
            backNum = backNum - 1;
            if month == 0:
                year = year + 1
                month = Week.last_week_of_year(year).week  
    
    newYearMonth = str(year)+str(month).zfill(2)
    return newYearMonth


import datetime
from dateutil.relativedelta import relativedelta
def monthCal(yearMonthDay, dayCal,flag = True):
    year = 0
    month = 0
    day = 0
    dividyear = 4
    dividmonth = 6

    if type(yearMonthDay) == str :
            year  = yearMonthDay[:dividyear]
            month = yearMonthDay[dividyear:dividmonth]
            day = yearMonthDay[dividmonth:]
            year = int(year)
            month = int(month)
            day = int(day)


    if type(dayCal) == str:
            dayCal = int(dayCal)
    if flag == True:
        checkMonth = datetime.date(year,month,day) + relativedelta(months=dayCal)
        calChekMonth = str(checkMonth.year) + str(checkMonth.month).zfill(2)
    else:
        checkMonth = datetime.date(year,month,day) + relativedelta(months=dayCal)
        calChekMonth = str(checkMonth.year) + str(checkMonth.month).zfill(2)
    
    return calChekMonth