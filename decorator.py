def log(func):
    
    def wrapper(*args, **kw):
        #print 'begin call %s()============='%func.__name__
        flag = func(*args, **kw)
        #print 'flag: ' + str(flag)
        #print 'end   call %s()============='%func.__name__
        return flag
    return wrapper

@log
def check_entrance(check, log_a, log_b, log_diff_x, log_diff_t, flag):
    '''
       check_entrance
    '''
    if 'entrance' in log_a['request_info'] and 'entrance' in log_b['request_info']:
        if log_a['request_info']['entrance'] != log_b['request_info']['entrance']:
            flag                   = 1
            log_diff_x['entrance'] = log_a['request_info']['entrance']
            log_diff_t['entrance'] = log_b['request_info']['entrance']
    
    return flag
