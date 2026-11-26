import re,glob
def T(ft):
    p=[x for x in glob.glob(f'ft_txt/{ft}_*.txt') if not x.endswith('.raw.txt')][0]
    return re.sub(r"\s+"," ",re.sub(r"-\n(?=[a-z])","",open(p).read()))
def q(ft,pat):
    m=re.search(pat,T(ft)); 
    if not m: raise SystemExit(f'NOT FOUND {ft}: {pat}')
    return m.group(0)
