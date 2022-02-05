from enum import Enum
# 型の定義
class ColumnType(Enum):
    INT = 1
    DOUBLE = 2
    STRING = 3
    DATE = 4
    DATETIME = 5

from .read_definition import read_definition
from .write_for_mysql import write_for_mysql
