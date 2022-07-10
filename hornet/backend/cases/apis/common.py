import re
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
db_sqlit3 = os.path.join(BASE_DIR, "", "db.sqlite3")


def get_replace_string(s):
    """
    替换字符串中变量
    """
    if "${" in s and "}" in s:
        # s_left = s.split("^{")[0]
        # s_right = s.split("^{")[1]
        # s2_left = s_right.split("}$")[0]
        # s2_right = s_right.split("}$")[1]
        # s_string = f"{s_left}{ss}{s2_right}"

        # 正则表达式
        result = re.search('(?<=\${).+(?=})', s)

        if result is not None:
            name = result.group()
            # 查询数据库
            conn = sqlite3.connect(db_sqlit3)
            cursor = conn.cursor()
            sql = f"""SELECT * FROM cases_testextract WHERE name="{name}";"""
            extract = cursor.execute(sql).fetchone()
            conn.commit()

            s_list = s.split("${" + name + "}")
            s_string = s_list[0] + extract[3] + s_list[1]

            return s_string
        else:
            return s
    else:
        return s


def query_extract_vlue(case_id):
    """
    查询提取器变量
    """
    conn = sqlite3.connect(db_sqlit3)
    cursor = conn.cursor()
    sql = f"""SELECT * FROM cases_testextract WHERE case_id="{case_id}";"""
    extracts = cursor.execute(sql).fetchall()
    conn.commit()
    return extracts


def update_extract_vlue(case_id, name, value):
    """
    更新提取器变量
    """
    conn = sqlite3.connect(db_sqlit3)
    cursor = conn.cursor()
    sql = f"""UPDATE cases_testextract SET vlue='{value}' WHERE case_id={case_id} AND name="{name}";"""
    cursor.execute(sql)
    conn.commit()
