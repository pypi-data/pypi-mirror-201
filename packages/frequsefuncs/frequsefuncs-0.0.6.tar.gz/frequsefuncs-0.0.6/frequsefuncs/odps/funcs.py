


########################### 连接ODPS ###########################

import json
from odps import ODPS

fpath_cfg = input('input odps config file path: ')

#连接odps的配置信息
with open(fpath_cfg, 'r') as c:
    dict_conn_odps = json.load(c)

v_accessid = dict_conn_odps['access_id']
v_accesskey = dict_conn_odps['access_key']
v_project = dict_conn_odps['project']
v_endpoint = dict_conn_odps['endpoint']

odps = ODPS(v_accessid, v_accesskey, v_project, endpoint = v_endpoint)

########################### ###########################


#设置全局参数
from odps import options
options.sql.settings = {"odps.sql.submit.mode" : "script"}




########################### 构建函数 ###########################

from odps.df import DataFrame
import time


def func_run_sql(str_sql, flag_mute = 0, mode = None):
    #异步的方式执行
    instance = odps.run_sql(str_sql)
    if flag_mute == 0:
        print(instance.get_logview_address())
    else:
        pass
    if mode == 'parallel':
        pass
    else:
        t1 = time.time()
        instance.wait_for_success()  #调用 wait_for_completion 方法会阻塞直到instance执行完成，wait_for_success 方法同样会阻塞，不同的是， 如果最终任务执行失败，则会抛出相关异常。
        t2 = time.time()
        if flag_mute == 0:
            print('cost {} seconds'.format(str(round(t2 - t1))))
        else:
            pass

def func_get_schema(nm_table):
    t = odps.get_table(nm_table)
    print(t.schema, str(round(t.size/1024/1024, 6)) + ' MB')
    return(t.size)


def func_downloaddata(nm_table, flag_mute = 0):
    t = odps.get_table(nm_table)
    if flag_mute == 0:
        print(t.schema, str(round(t.size/1024/1024, 3)) + ' MB')
    else:
        pass
    #convert data to df
    df_odps = DataFrame(t)
    df = df_odps.to_pandas()
    return(df)


#输入sql代码 和 临时表名，返回dataframe
def func_run_sql_get_result(str_sql, nm_table, flag_mute, mode):
    func_run_sql(str_sql, flag_mute, mode)
    df_r = func_downloaddata(nm_table, flag_mute)
    return df_r

########################### ###########################


