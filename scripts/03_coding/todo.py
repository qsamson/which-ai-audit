import json,importlib,sys,glob
sys.path.insert(0,'scripts/03_coding')
done=set()
for m in sorted(glob.glob('code_b*.py')): done|=set(importlib.import_module(m.split('/')[-1][:-3]).D)
R=json.load(open('autocode.json')); t=[f for f in sorted(R) if f not in done]
print(len(done),'done',len(t),'todo'); print(' '.join(t[:int(sys.argv[1]) if len(sys.argv)>1 else 10]))
