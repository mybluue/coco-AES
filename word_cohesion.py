import pickle

with open('/home/pyp/D/mywork/group/LTP_cohesion/b_file2pickle/res/essay_clean_ltp.pickle','rb') as f:
    id2ltp=pickle.load(f)
with open('./essay_clean_ltp_svo.pickle','rb') as f:
    id2ltpsvo = pickle.load(f)
test={}
test['199312104523100003']=id2ltp['199312104523100003']
# print(test['199312104523100003'])
print(*list(id2ltpsvo.values())[0:10],sep='\n')
exit()
def getSVO(id2ltp,singleSent=False):
    allSVO={}
    ct=0
    for k,v in id2ltp.items():
        ct+=1
        print(ct,k)

        seg=v['words']
        pos=v['pos']
        dep=v['dep']
        # print(seg)
        # print(pos)
        # print(dep)
        words = [list(zip([i for i in range(1, len(seg[i]) + 1)], seg[i])) for i in range(len(seg))]
        essaySVO=[]
        for i in range(len(words)):
            id2word = {x[0]: x[1] for x in words[i]}
            id2word[0] = '0'
            id2pos={j+1:pos[i][j] for j in range(len(pos[i]))}
            id2head = {x[0]: x[1] for x in dep[i]}
            id2rel = {x[0]: x[2] for x in dep[i]}
            curSVO=[]
            curPOS=[]
            sentSVO=[]
            for index in id2rel.keys():
                if id2rel[index]=='SBV':
                    if curSVO and not singleSent:
                        sentSVO.append(curSVO+curPOS)
                    curSVO=[]
                    curPOS=[]
                    curSVO.append(id2word[index])
                    curPOS.append(id2pos[index])
                    curSVO.append(id2word[id2head[index]])
                    curPOS.append(id2pos[id2head[index]])

                    hasObject=False
                    for id in id2rel.keys():
                        if id!=index and id2head[id]==id2head[index] and id2rel[id]=='VOB':
                            hasObject=True
                            curSVO.append(id2word[id])
                            curPOS.append(id2pos[id])
                    if not hasObject:
                        curSVO.append('--object')
                        curPOS.append('--pos')
                    if(singleSent):
                        sentSVO=curSVO+curPOS
                        break
            if not singleSent:
                sentSVO.append(curSVO+curPOS)
            if sentSVO:
                essaySVO.append(sentSVO)

        allSVO[k]=essaySVO
    return allSVO

# allSVO=getSVO(id2ltp)
# with open('./essay_clean_ltp_svo.pickle','wb') as f:
#     pickle.dump(allSVO,f)
# # testSVO=getSVO(test)
# for v in testSVO.values():
#     print(v)


