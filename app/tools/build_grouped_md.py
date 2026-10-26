import json,sys,glob,collections
sys.path.insert(0,'/tmp')
from cluster import load
C='①②③④⑤'
NAMES={'hb':'인간행동과 사회환경','rs':'사회복지조사론','pr':'사회복지실천론','sk':'사회복지실천기술론','cm':'지역사회복지론','po':'사회복지정책론','ad':'사회복지행정론','lw':'사회복지법제론'}
Q=load();BY={q['id']:q for q in Q}
E={}
for f in glob.glob('data/e_*.json'): E.update(json.load(open(f,encoding='utf-8')))
subs=json.load(open('data/subjects.json',encoding='utf-8'))
types=collections.defaultdict(list)
for q in Q: types[(q['k'],q['t'])].append(q)
out=['# 사회복지사업 1급 기출 유형별·유사문항별 정리 (2017~2026)'.replace('사회복지사업','사회복지사'),'',
'- 같은 유형 안에서 질문이 비슷한 문항끼리 묶었습니다. 묶음 안은 최신 연도순입니다.',
'- 정답은 CBT 공식 정답표 기준이며, 법령 개정으로 달라진 문항은 현행법 기준을 따로 표시했습니다.',
'- 해석은 AI가 작성했으며 틀릴 수 있습니다. 문항번호는 연도-교시-번호입니다.','']
ng=0;ot=0
for s in subs:
    k=s['k'];ns={};exec(open(f'/tmp/claude-0/grp/{k}.py',encoding='utf-8').read(),ns);G=ns['G']
    tot=sum(len(l) for (kk,t),l in types.items() if kk==k)
    out+=[f"## {s['g']}교시 · {NAMES[k]} ({tot}문항)",'']
    for t,l in sorted([(t,l) for (kk,t),l in types.items() if kk==k],key=lambda x:(-len(x[1]),x[0])):
        groups=[(n,[i for i in ids if i in BY and BY[i]['k']==k and BY[i]['t']==t]) for n,ids in G[t]]
        groups=[(n,ids) for n,ids in groups if ids]
        used={i for _,ids in groups for i in ids}
        rest=[q['id'] for q in l if q['id'] not in used]
        if rest: groups.append(('그 밖의 문항',rest))
        out+=[f"### {t} ({len(l)}문항 · {len(groups)}개 묶음)",'']
        for n,ids in groups:
            ng+=1
            out+=[f"#### {n} ({len(ids)}문항)",'']
            for i,id_ in enumerate(sorted(ids,key=lambda x:(-BY[x]['y'],BY[x]['g'],BY[x]['n'])),1):
                x=BY[id_];ex=E.get(id_,{})
                a=ex['cur'] if isinstance(ex.get('cur'),int) else x['a']
                st=x['s']
                out.append(f"문제{i}. [{id_}] {st[0]}");out+=st[1:]
                ch=[f"{C[j]} {c.strip()}" for j,c in enumerate(x['c'])]
                if sum(len(c) for c in ch)+len(ch)<=48: out.append('  '.join(ch))
                else: out+=ch
                out.append('정답: '+((C[a-1]+(' '+x['c'][a-1].strip() if max(len(c) for c in x['c'])>12 else '')) if a else '없음 (현행법 기준 정답 없음)'))
                out.append('해석: '+ex.get('x','해설 준비 중').replace('\n\n',' ').replace('\n',' '))
                if isinstance(ex.get('cur'),int) and ex['cur']!=x['a']:
                    out.append(f"※ 개정 반영: 시험 당시 정답 {C[x['a']-1]}, 현행 기준 "+(C[ex['cur']-1] if ex['cur'] else '정답 없음'))
                if ex.get('note'): out.append('※ '+ex['note'])
                out.append('');ot+=1
open('gichul-note-grouped.md','w',encoding='utf-8').write('\n'.join(out))
print('questions',ot,'groups',ng)
