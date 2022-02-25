import sys,pickle
import pandas as pd
from ltp import LTP
ltp=LTP('base2')

# inputfile=sys.argv[1]
# outputfile=sys.argv[2]

def xlsx2ltp(inputfile,outputfile):
    with open(outputfile,'wb') as f:
        id2ltp={}
        seq=0
        df = pd.read_excel(inputfile)
        dc = df.to_dict('list')
        ids = dc['id']
        texts = dc['text']
        for i in range(len(ids)):
            ltp_res={}

            id=ids[i]
            essay=texts[i]

            print(f'{seq}\t{id}')

            text = list()
            text.append(essay)
            text_list = ltp.sent_split(text)
            seg, hidden = ltp.seg(text_list)

            words=seg
            pos=ltp.pos(hidden)
            ner=ltp.ner(hidden)
            srl = ltp.srl(hidden, keep_empty=False)
            dep = ltp.dep(hidden)
            sdp_tree = ltp.sdp(hidden,mode='tree')
            sdp_graph=ltp.sdp(hidden,mode='graph')

            ltp_res['words']=words
            ltp_res['pos']=pos
            ltp_res['ner']=ner
            ltp_res['srl']=srl
            ltp_res['dep']=dep
            ltp_res['sdp_tree']=sdp_tree
            ltp_res['sdp_graph']=sdp_graph

            id2ltp[id]=ltp_res

            seq+=1
        pickle.dump(id2ltp,f)

# file2ltp(inputfile,outputfile)

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

def ltp2svo(inputfile, outputfile):
    f1 = open(inputfile, 'rb')
    id2ltp = pickle.load(f1)
    id2svo = getSVO(id2ltp)
    with open(outputfile, 'wb') as f:
        pickle.dump(id2svo, f)