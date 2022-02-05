# dbdef2createtable
- テーブル定義書(Excel)からCreateTable文を作る

## Usage
- read_definition()で読んで、write～()で書く。
- write～の関数は、必要に応じて作っていく。
- 型の書き方も、必要に応じて増やしていく。

## 備忘録
- openpyxlを使ってExcelを読むとき、イテレータを使うともっとスマートに書ける。後から知った。（←言い訳）いつか気が向いたらリファクタリングする。
