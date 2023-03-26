# 导入sqlite3模块
import sqlite3
import pandas as pd

# 连接数据库
con = sqlite3.connect('db.sqlite3')
# 创建游标对象
cur = con.cursor()

# 查询ESG_esg_reports表中的所有数据，并转换为pandas的DataFrame对象
sql = "select * from ESG_esg_reports"
df = pd.read_sql(sql, con)

# 删除md5字段相同的数据，只保留第一条记录
df.drop_duplicates(subset="md5", keep="first", inplace=True)

# 将清理后的数据重新写入数据库，覆盖原表
df.to_sql("ESG_esg_reports", con, if_exists="replace", index=False)

# ESG_esg_reports表中site字段的值为“cinfo”，将其改为“cninfo”
sql = "update ESG_esg_reports set site='cninfo' where site='cinfo'"
cur.execute(sql)
con.commit()

cur.close()
con.close()