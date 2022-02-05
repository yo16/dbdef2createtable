from openpyxl import load_workbook
import re

from . import ColumnType

def read_definition(in_def):
    """ 指示されたExcelの読み方を元に読んで、
    あとで使いやすい形にして返す

    (イテレーターを使って書き直したい.後から知った.)
    """

    wb = load_workbook(in_def['file'], read_only=True)
    sh = wb[in_def['sheet']]

    def_col = in_def['columns']

    # テーブル名
    table_name_columns = None
    if isinstance(def_col['table_name'], list) or \
        isinstance(def_col['table_name'], tuple):
        table_name_columns = [v for v in def_col['table_name']]
    else:
        table_name_columns = [def_col['table_name']]

    # テーブル情報を得る
    result = []
    cur_line = in_def['start_line']
    table_name = get_table_name(sh, cur_line, table_name_columns)
    table_cmnt = sh[def_col['table_comment']+str(cur_line)].value
    cur_line += 1
    while(table_name is not None):  # テーブル単位のループ
        #print(table_name)
        tab = {}

        # テーブル名
        tab['name'] = table_name
        # コメント
        tab['comment'] = table_cmnt

        # 列名
        tab['columns'] = []
        column_name = sh[
            def_col['column_name']+str(cur_line)
        ].value
        while(column_name is not None):
            #print(column_name)
            col = {}

            # 列名
            col['name'] = column_name
            # 列コメント
            col['comment'] = sh[
                def_col['column_comment']+str(cur_line)
            ].value
            # 型
            typ = sh[
                def_col['type']+str(cur_line)
            ].value
            col['type'], col['type_size'] = \
                get_type_info(typ)
            # NotNull
            col['nn'] = True if sh[
                def_col['not_null']+str(cur_line)
            ].value == 'Y' else False
            # PK
            col['pk'] = True if sh[
                def_col['primary_key']+str(cur_line)
            ].value == 'Y' else False
            # 初期値
            col['default'] = sh[
                def_col['default_value']+str(cur_line)
            ].value

            tab['columns'].append(col)

            # 次の行
            cur_line += 1
            column_name = sh[
                def_col['column_name']+str(cur_line)
            ].value


        result.append(tab)

        # 次のテーブル
        table_name = get_table_name(sh, cur_line, table_name_columns)
        table_cmnt = sh[def_col['table_comment']+str(cur_line)].value
        cur_line += 1
    return result


def get_table_name(sh, line_num, table_name_columns):
    """テーブル指定の列から抜き出して、1個でも配列にして返す
    """
    table_name = []
    for c in table_name_columns:
        tmp = sh[f'{c}{line_num}'].value
        if tmp is not None:
            table_name.append(tmp)
    if len(table_name)==0:
        return None
    return table_name


def get_type_info(_s):
    """型の文字列から、当モジュール内で使用する型(ColumnType)へ変換しつつ
    サイズも分ける。
    新しいものが増えたら、ここと__init__.pyへ追加する。
    """
    s = _s.lower()

    ret_type = None
    ret_type_len = None

    if s.startswith('string') or \
        s.startswith('varchar') or \
        s.startswith('char'):
        ret_type = ColumnType.STRING
    elif s.startswith('int'):
        ret_type = ColumnType.INT
    elif s.startswith('double') or \
        s.startswith('float') or \
        s.startswith('number'):
        ret_type = ColumnType.DOUBLE
    elif s=='date':
        ret_type = ColumnType.DATE
    elif s=='datetime':
        ret_type = ColumnType.DATETIME
    elif s.startswith('bool'):
        ret_type = ColumnType.BOOL
    else:
        assert False, f'Unknown type!!: {s}'

    # 丸カッコでサイズが指定されてたら取得
    m = re.match(r'^.*\(([^\)]+)\)', s)
    if m:
        ret_type_len = int(m.groups()[0])
    
    return (ret_type, ret_type_len)
