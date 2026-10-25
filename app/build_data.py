import json,re,sys
SP='/tmp/claude-0/-home-user-work/65c52178-c5e0-542f-9dfd-843a2358e00e/scratchpad/'
Q=json.load(open(SP+'Qfinal.json'))['Q']
SUBJ=[("인간행동과 사회환경","hb"),("사회복지 조사론","rs"),("사회복지 실천론","pr"),("사회복지 실천 기술론","sk"),("지역사회 복지론","cm"),("사회복지 정책론","po"),("사회복지 행정론","ad"),("사회복지 법제론","lw")]
key=dict(SUBJ)
mark=re.compile(r'^[①②③④⑤❶❷❸❹❺]\s*')
out={k:[] for _,k in SUBJ}
for q in Q:
    ch=[mark.sub('',c).strip() for c in q['choices']]
    assert len(ch)==5
    i=f"{q['year']%100}-{q['gyo']}-{q['no']}"
    out[key[q['subj']]].append({"id":i,"y":q['year'],"g":q['gyo'],"n":q['no'],"t":q['topic'],"f":q['fmt'],"s":q['stem'],"c":ch,"a":q['ans']})
for k,v in out.items():
    json.dump(v,open(f'data/q_{k}.json','w'),ensure_ascii=False,separators=(',',':'))
    print(k,len(v))
json.dump([{"k":k,"name":n,"g":next(q['gyo'] for q in Q if q['subj']==n)} for n,k in SUBJ],open('data/subjects.json','w'),ensure_ascii=False)
