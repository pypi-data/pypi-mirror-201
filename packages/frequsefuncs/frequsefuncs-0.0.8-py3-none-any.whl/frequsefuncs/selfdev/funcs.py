






#输入df和希望呈现的数字格式（'{:,}'、'{:.2%}'、'{:,.0f}'），呈现带格式的表格
def func_format_display(df, num_fmt):
    all_props = [
        ('border','2px solid black'),
    ]
    th_props = [
        ('font-size', '11px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', 'black'),               ## #6d6d6d
        ('background-color', 'white'),    ## #f7f7f9
        ('border','1px dashed black')
    ]
    td_props = [
        ('font-size', '9px'),
        ('text-align', 'right'),
        ('color', 'black'),
        ('background-color', 'white'),    ## #f7f7f9
        ('border','1px dashed black')
    ]

    config_fmt = [{'selector':'','props':all_props}, 
                  {'selector':'th','props':th_props},
                  {'selector':'td','props':td_props}
                 ]
    dict_fmt = {}
    lst_barfmt = []
    for k in df.columns:
        dict_fmt[k] = num_fmt   #'{:,}' #'{:.2%}' #'{:,.0f}'
        lst_barfmt.append(k)
    display(df.style.set_table_styles(config_fmt).format(dict_fmt).bar(subset = lst_barfmt, width = 80, align = 'mid'))




#输入df和希望呈现的数字格式（'{:,}'、'{:.2%}'、'{:,.0f}'），呈现带格式的表格
def func_format_display_bycol(df, dict_fmt, lst_barfmt):
    all_props = [
        ('border','2px solid black'),
    ]
    th_props = [
        ('font-size', '11px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', 'black'),               ## #6d6d6d
        ('background-color', 'white'),    ## #f7f7f9
        ('border','1px dashed black')
    ]
    td_props = [
        ('font-size', '9px'),
        ('text-align', 'right'),
        ('color', 'black'),
        ('background-color', 'white'),    ## #f7f7f9
        ('border','1px dashed black')
    ]

    config_fmt = [{'selector':'','props':all_props}, 
                  {'selector':'th','props':th_props},
                  {'selector':'td','props':td_props}
                 ]
    display(df.style.set_table_styles(config_fmt).format(dict_fmt).bar(subset = lst_barfmt, width = 80, align = 'mid'))






