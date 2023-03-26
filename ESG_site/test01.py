import tabula

tabula.environment_info()

dfs = tabula.read_pdf('test.pdf', pages='all', encoding='GBK')

for item in dfs:
    print(item, type(item))