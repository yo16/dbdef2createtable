from openpyxl import load_workbook

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
    table_sep = '.'
    if 'table_connection_str' in in_def['columns'].keys():
        table_sep = in_def['columns']['table_connection_str']
    table_name = get_table_name(sh, cur_line, table_name_columns, table_sep)
    cur_line += 1
    while(table_name is not None):  # テーブル単位のループ
        #print(table_name)
        tab = {}

        # テーブル名
        tab['name'] = table_name
        # コメント
        tab['comment'] = sh[
            def_col['table_comment']+str(cur_line)
        ].value

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
            col['type'] = sh[
                def_col['type']+str(cur_line)
            ].value
            # NotNull
            col['nn'] = sh[
                def_col['not_null']+str(cur_line)
            ].value
            # PK
            col['pk'] = sh[
                def_col['primary_key']+str(cur_line)
            ].value
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
        table_name = get_table_name(sh, cur_line, table_name_columns, table_sep)
        cur_line += 1
    return result


def get_table_name(sh, line_num, table_name_columns, sep_str='.'):
    table_name = ''
    for c in table_name_columns:
        tmp = sh[f'{c}{line_num}'].value
        if tmp is not None:
            table_name += tmp + sep_str
    # 最後のsep_strを削除して返す
    table_name = table_name[:(-1)*len(sep_str)]
    if len(table_name)==0:
        return None
    return table_name
