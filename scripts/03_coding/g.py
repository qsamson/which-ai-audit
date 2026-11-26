import re,sys,glob
ft,pat=sys.argv[1],sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 160
p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
t=re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
for m in list(re.finditer(pat,t,re.I))[:6]: print(f"[{m.start()*100//len(t)}%] …{t[max(0,m.start()-w):m.end()+w]}…")
