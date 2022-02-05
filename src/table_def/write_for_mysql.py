import os
from . import ColumnType

def write_for_mysql(tab_info, to_dir):
    """MySQL向けのCreateTable文を生成
    """
    os.makedirs(to_dir, exist_ok=True)

    for t in tab_info:
        write_for_mysql_tab(t, to_dir)

    return None


def write_for_mysql_tab(tab_info, to_dir, table_sep='_'):
    """MySQL向けのCreateTable文を生成(テーブル単位)
    """
    pk_column_names = []
    table_name = table_sep.join(tab_info['name'])
    file_path = f'{to_dir}/{table_name}.sql'
    with open(file_path, mode='w', encoding='utf-8') as f:
        # CREATE TABLE
        f.write(f'CREATE TABLE IF NOT EXISTS {table_name}\n')
        f.write('(\n')
        
        for i,c in enumerate(tab_info['columns']):
            sep = '' if i==0 else ','
            nm = c['name']
            typ = c['type']
            typ_sz = c['type_size']
            type_str = get_type_str(typ, typ_sz)
            nn = 'NOT NULL' if c['nn'] else ''
            cmnt = 'COMMENT \'' + c['comment'] + '\'' if c['comment'] else ''
            dflt = get_default_value(c['default'], typ)
            # 列
            f.write(f'\t{sep}{nm} {type_str} {nn} {dflt} {cmnt}\n')

            if c['pk']:
                pk_column_names.append(nm)
        
        # PK
        if len(pk_column_names):
            pkcolumns = ','.join(pk_column_names)
            f.write(f'\t,PRIMARY KEY({pkcolumns})\n')

        f.write(')\n')

        # テーブルコメント
        if tab_info['comment']:
            cmnt = tab_info['comment']
            f.write(f'COMMENT=\'{cmnt}\'\n')
        
        f.write(';\n');


def get_type_str(typ, typ_sz):
    """ MySQLの型の書き方に書き直す

    とりあえず今必要なものだけ定義する。
    他のは必要になったら追加する。
    """
    ret = ''
    if typ==ColumnType.INT:
        ret = 'INT'
    elif typ==ColumnType.DOUBLE:
        ret = 'DOUBLE'
    elif typ==ColumnType.STRING:
        ret = 'VARCHAR'
    elif typ==ColumnType.DATE:
        ret = 'DATE'
    elif typ==ColumnType.DATETIME:
        ret = 'DATETIME'
    elif typ==ColumnType.BOOL:
        ret = 'BOOLEAN'     # tinyint(1)として作られるけど、True, Falseが使える
    
    if typ_sz:
        ret += f'({typ_sz})'
    
    return ret

def get_default_value(val, typ):
    if val is None:
        return ''
    
    ret = 'DEFAULT '
    if typ==ColumnType.STRING:
        ret += '\'' + val + '\''
    else:
        ret += val
    
    return ret
