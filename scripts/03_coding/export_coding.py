import pandas as pd
from openpyxl.styles import Font,PatternFill,Alignment
d=pd.read_pickle('coded_v12.pkl'); LOG=pd.read_csv('recheck_log_v11.csv')
F=pd.read_excel('which_ai_master_screening.xlsx',sheet_name='Full-text list').set_index('ft_id')
d.insert(1,'journal',d.ft_id.map(F.journal)); d.insert(2,'title',d.ft_id.map(F.title))
inc=d[d.ft_decision=='include']; t12=inc[inc.study_type!='T3']
J=pd.read_excel('which_ai_master_screening.xlsx',sheet_name='By journal').set_index('Journal').Field; inc=inc.assign(field=inc.journal.map(J)); t12=inc[inc.study_type!='T3']
items=['A1','A2','B1','B2','B3','B4','B5','C1','C2','D1','E1','E2','F1','G1']
S=pd.DataFrame({it:inc[it].value_counts().reindex(['R','P','N','NA']).fillna(0).astype(int) for it in items}).T
S['R % of applicable']=(100*S.R/(S.R+S.P+S.N)).round(0)
X=pd.DataFrame({'regime (X1), T1+T2':t12.X1.value_counts()})
FLD=inc.groupby('field').apply(lambda x: pd.Series({'included':len(x),'B1 = R':(x.B1=='R').sum(),'B1 = R %':round(100*(x.B1=='R').mean()),'T1+T2':(x.study_type!='T3').sum(),'X6 yes':(x.X6=='yes').sum(),'X6 yes % of T1+T2':round(100*(x.X6=='yes').sum()/max(1,(x.study_type!='T3').sum()))})); X6=inc.X6.value_counts()
summ=[['Papers coded',len(d)],['Included at full text',len(inc)],['Excluded at full text',len(d)-len(inc)],
      ['Report model version AND date (H1)',f"{(inc.B1=='R').sum()} of {len(inc)} ({100*(inc.B1=='R').mean():.0f}%)"],
      ['Over-generalize (X6 yes, H4)',f"{(t12.X6=='yes').sum()} of {len(t12)} T1+T2 ({100*(t12.X6=='yes').mean():.0f}%)"],
      ['Tool-using or autonomous regime (H3)',f"{t12.X1.isin(['Tool-using agent','Autonomous/multi-agent']).sum()} of {len(t12)} T1+T2 ({100*t12.X1.isin(['Tool-using agent','Autonomous/multi-agent']).mean():.1f}%)"],
      ['Authors disclosed own LLM use (R)',f"{(inc.R!='none').sum()} of {len(inc)}"]]
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE as ILL
clean=lambda df: df.apply(lambda c: c.map(lambda v: ILL.sub('',v) if isinstance(v,str) else v))
d=clean(d); LOG=clean(LOG)
with pd.ExcelWriter('which_ai_coding_v1.2.xlsx',engine='openpyxl') as w:
    pd.DataFrame(summ,columns=['Measure','Value']).to_excel(w,sheet_name='Summary',index=False)
    S.to_excel(w,sheet_name='Items (R-P-N-NA)')
    X.to_excel(w,sheet_name='Regimes')
    FLD.to_excel(w,sheet_name='By field')
    clean(pd.read_csv('x6_v12_three_judgments.csv')).to_excel(w,sheet_name='X6 three judgments',index=False)
    LOG[LOG.old!=LOG.new].to_excel(w,sheet_name='Final-pass changes',index=False)
    d.to_excel(w,sheet_name='Coding',index=False)
    for ws in w.book.worksheets:
        for c in ws[1]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='1F4E79')
        ws.column_dimensions['A'].width=40; ws.column_dimensions['B'].width=22; ws.freeze_panes='B2'
print(pd.DataFrame(summ).to_string(index=False,header=False)); print(S.to_string())
