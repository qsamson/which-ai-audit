import pandas as pd
from sklearn.metrics import cohen_kappa_score as ck
g=pd.read_pickle('reliability/gpt.pkl').set_index('ft_id')
old=pd.read_pickle('coded.pkl').set_index('ft_id'); new=pd.read_pickle('coded_v11.pkl').set_index('ft_id')
ids=[i for i in g.index if i in new.index]
rows=[]
for it in ['B1','E1','G1','X1','X6']:
    for lab,c in (('v1.0',old),('v1.1',new)):
        k=[i for i in ids if c.loc[i,'ft_decision']=='include' and g.loc[i,'ft_decision']=='include' and c.loc[i,it] not in ('NA','') and g.loc[i,it] not in ('NA','',None)]
        a=[str(c.loc[i,it]) for i in k]; b=[str(g.loc[i,it]) for i in k]
        rows.append((it,lab,len(k),round(sum(x==y for x,y in zip(a,b))/len(k),2),round(ck(a,b),2)))
print(pd.DataFrame(rows,columns=['item','version','n','agree','kappa']).to_string(index=False))
