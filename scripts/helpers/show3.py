import json,sys
E=json.load(open('ev3.json')); ks=sorted(E)[int(sys.argv[1]):int(sys.argv[2])]
for k in ks:
    e=E[k]; print(f"## {k} {e['type']} cur={e['x6']} lim={'Y' if e['haslim'] else 'N'}")
    if e['x6q']: print('   Q:',e['x6q'][:200])
    for x in e['gc'][:2]: print('   G:',x[:200])
    for x in e['mv'][:2]: print('   M:',x[:260])
    for x in e['st'][:2]: print('   S:',x[:220])
