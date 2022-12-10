


def DateToStd(date):
    [y,m,d] = str(date).split('/')
    if len(m)==1: m = '0' + m 
    if len(d)==1: d = '0' + d 
    return y+'/'+m+'/'+d

def DateToInt(date):
    [y,m,d] = str(date).split('/')
    return int(y+m+d)
    
def IntToDate(date):
    dateStr = str(date)
    y = dateStr[0:4]
    m = dateStr[4:6]
    d = dateStr[6:8]
    return y+'/'+m+'/'+d