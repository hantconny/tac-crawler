# -*- coding:utf-8 -*-
list=[]
with open(r'C:\Users\Administrator\Desktop\tac_20231208.text', encoding='utf-8') as f:
    for line in f.readlines():
        tac, v = line.split('|', 1)
        if len(tac) < 8:
            list.append('|'.join([tac.rjust(8, '0'), v]))
        else:
            list.append(line)


with open('new.text', encoding='utf-8', mode='w') as n:
    n.writelines(list)