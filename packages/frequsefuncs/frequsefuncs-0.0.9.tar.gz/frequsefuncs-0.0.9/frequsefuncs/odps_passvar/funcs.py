


########################### 连接ODPS ###########################

import json
from odps import ODPS
import time


def func_conn_odps(fpath_cfg):
    #连接odps的配置信息
    with open(fpath_cfg, 'r') as c:
        dict_conn_odps = json.load(c)
    v_accessid = dict_conn_odps['access_id']
    v_accesskey = dict_conn_odps['access_key']
    v_project = dict_conn_odps['project']
    v_endpoint = dict_conn_odps['endpoint']
    odps = ODPS(v_accessid, v_accesskey, v_project, endpoint = v_endpoint)
    return odps

########################### ###########################


#设置全局参数
from odps import options
options.sql.settings = {"odps.sql.submit.mode" : "script"}




########################### 构建函数 ###########################

from odps.df import DataFrame
import time


def func_run_sql(fpath_cfg, str_sql, flag_mute = 0, mode = None):
    odps = func_conn_odps(fpath_cfg)
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

def func_get_schema(fpath_cfg, nm_table):
    odps = func_conn_odps(fpath_cfg)
    t = odps.get_table(nm_table)
    print(t.schema, str(round(t.size/1024/1024, 6)) + ' MB')
    return(t.size)


def func_downloaddata(fpath_cfg, nm_table, flag_mute = 0):
    odps = func_conn_odps(fpath_cfg)
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
def func_run_sql_get_result(fpath_cfg, str_sql, nm_table, flag_mute, mode):
    func_run_sql(fpath_cfg, str_sql, flag_mute, mode)
    df_r = func_downloaddata(fpath_cfg, nm_table, flag_mute)
    return df_r


def func_downloaddata_bybatch(fpath_cfg, nm_table, flag_mute = 0, batch_size = 100000, sec_wait_retry = 30):
    odps = func_conn_odps(fpath_cfg)
    t = odps.get_table(nm_table)
    data = []

    with t.open_reader() as reader:
        num_rows = reader.count
        if flag_mute == 0:
            print(t.schema, str(round(t.size/1024/1024, 3)) + ' MB;', ' total row number: {}'.format(num_rows))
        else:
            pass

    for cur_i in range(0, num_rows, batch_size):
        
        str_sql_exe = '''
        select
            *
        from {tbnm_from}
        limit {batch_size}
        offset {i}
        '''.format(tbnm_from = nm_table, batch_size = batch_size, i = cur_i)
        retry_i = 0
        while retry_i <= 5:
            retry_i += 1
            try:
                with odps.execute_sql(str_sql_exe).open_reader() as reader:
                    dft = reader.to_pandas()
                    if flag_mute == 0:
                        rn = dft.shape[0]
                        print('start at {cur_i}, finish number of rows {rn}'.format(cur_i = cur_i, rn = rn))
                break
            except:
                if retry_i <= 4:
                    print('retry {} failed'.format(retry_i))
                    time.sleep(sec_wait_retry)
                else:
                    raise
        data.append(dft)

    import pandas as pd
    df_r = pd.concat(data, ignore_index = True, axis = 0)
    return(df_r)



#输入sql代码 和 临时表名，返回dataframe - 分批下载数据
def func_run_sql_get_result_bybatch(fpath_cfg, str_sql, nm_table, flag_mute, mode, batch_size, sec_wait_retry = 30):
    func_run_sql(fpath_cfg, str_sql, flag_mute, mode)
    df_r = func_downloaddata_bybatch(fpath_cfg, nm_table, flag_mute, batch_size, sec_wait_retry)
    return df_r




########################### ###########################


