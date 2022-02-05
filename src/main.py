
from table_def import read_definition, write_for_mysql

def main():
    """Excelファイルからテーブル定義書を読んで、CreateTable文を作る
    """
    # 読み込み方の定義
    excel_read_def = {
        'file': './input/テーブル定義.xlsx',
        'sheet': 'DB項目定義',
        'start_line': 3,        # Excelの1行目=1, 2行目=2, ...
        'columns': {    # Excelの列名A,B,...で指定する
            'table_name': ['B','C'],    # 複数、単数も可
            'table_comment': 'D',
            'column_name': 'E',
            'column_comment': 'F',
            'type': 'G',
            'not_null': 'H',
            'primary_key': 'I',
            'default_value': 'J',
        }
    }
    # 出力の定義
    mysql_dir = './output/myql'

    # ----------------------------

    # 定義書を読む
    table_def_info = read_definition(excel_read_def)
    #print(table_def_info)
    
    # SQLファイルを生成
    write_for_mysql(table_def_info, mysql_dir)

    return None



if __name__=='__main__':
    main()