# jsonm
python object to or from json

python2, python3 supported.

注意:

    python2:
        json_loads 支持解析str/unicode
        json_dumps 结果为str

    python3:
        json_loads 支持解析bytes/str
        json_dumps 结果为str


对于python3，标准库json.dumps的结果始终为str类型。

另外注意python2和python3的str意义是不一样的。
