'''
指代衔接：
1. pronouns/nouns
2. pronouns/sqrt(tokens)
3. personal pronouns/nouns
4.
prp_li=['我', '我们', '本人', '鄙人', '敝人', '私', '老子', '老娘', '本姑娘', '本小姐', '本少爷', '人家', '本席', '咱', '咱们', '俺', '俺们', '恁爸', '恁祖妈', '人哋', '我哋', '阿拉', '偶', '禾', '小弟', '小妹', '姊', '哥', '洒家', '某家', '予一人', '本王', '寡小君', '小童', '梓童', '本座', '本单位', '本官', '本将', '末将', '下官', '卑职', '在下', '仆', '区区', '某', '某人', '某某', '某甲', '小弟', '愚兄', '小妹', '愚姊', '愚姐','小生', '晚生', '后学', '末学', '不才', '老夫', '老朽', '老叟', '老身', '免贵', '老奴', '老仆', '小女子', '奴家', '奴', '儿', '卬', '姎', '贫道', '小道', '草民', '小人', '小可', '小的', '哀家', '本宫', '你', '你们', '妳', '妳们', '祢', '子', '乃', '他', '他们', '她', '她们', '它', '它们', '祂', '伊', '渠', '佢', '怹', '贵公司', '贵社', '贵府', '贵院', '贵局', '贵处', '贵校', '贵会']
'''

# import pickle
# with open('/home/pyp/D/mywork/组会/1_LTP_cohesion_07/2_file2pickle/res/essay_clean_ltp.pickle','rb') as f:
#     id2ltp=pickle.load(f)

# for v in id2ltp.values():
#     print(v)
#     break
# exit()
prp_li=['我', '我们', '本人', '鄙人', '敝人', '私', '老子', '老娘', '本姑娘', '本小姐', '本少爷', '人家', '本席', '咱', '咱们', '俺', '俺们', '恁爸', '恁祖妈', '人哋', '我哋', '阿拉', '偶', '禾', '小弟', '小妹', '姊', '哥', '洒家', '某家', '予一人', '本王', '寡小君', '小童', '梓童', '本座', '本单位', '本官', '本将', '末将', '下官', '卑职', '在下', '仆', '区区', '某', '某人', '某某', '某甲', '小弟', '愚兄', '小妹', '愚姊', '愚姐','小生', '晚生', '后学', '末学', '不才', '老夫', '老朽', '老叟', '老身', '免贵', '老奴', '老仆', '小女子', '奴家', '奴', '儿', '卬', '姎', '贫道', '小道', '草民', '小人', '小可', '小的', '哀家', '本宫', '你', '你们', '妳', '妳们', '祢', '子', '乃', '他', '他们', '她', '她们', '它', '它们', '祂', '伊', '渠', '佢', '怹', '贵公司', '贵社', '贵府', '贵院', '贵局', '贵处', '贵校', '贵会']
dsp_li=[]
irp_li=[]
def get_grammatical_cohesion_index(words,pos):
    words_cnt,nouns_cnt,pronouns_count,prp_count,dsp_cnt,cnj_cnt=0,0,0,0,0,0
    prp_word, pronoun_word, cnj_word = [], [], []
    for i in range(len(words)):
        for j in range(len(words[i])):
            # 排除标点符号
            if pos[i][j]!='wp':
                words_cnt+=1
                if pos[i][j]=='n': nouns_cnt+=1
                if pos[i][j]=='r':
                    pronouns_count+=1
                    pronoun_word.append(words[i][j])
                    if words[i][j] in prp_li:
                        prp_count+=1
                        prp_word.append(words[i][j])
                if pos[i][j]=='c':
                    cnj_cnt+=1
                    cnj_word.append(words[i][j])


    PN_RATIO = pronouns_count / (nouns_cnt + 1)    
    PT_RATIO = pronouns_count / (pow(words_cnt,0.5) + 1)  
    PPN_RATIO = prp_count / (nouns_cnt + 1)   
    PPP_RATIO = prp_count / (pronouns_count + 1)

    PP_TTR = len(list(set(prp_word))) / (len(prp_word) + 1)
    P_TTR = len(list(set(pronoun_word))) / (len(pronoun_word) + 1)

    PSent_RATIO = pronouns_count / (len(words)+1)
    PPSent_RATIO = prp_count / (len(words)+1)

    CSent_RATIO = cnj_cnt / (len(words)+1)
    CN_RATIO = cnj_cnt / (nouns_cnt+1)
    CT_RATIO = cnj_cnt/(pow(words_cnt,0.5)+1)

    C_TTR = len(list(set(cnj_word))) / (len(cnj_word) + 1)

    return PN_RATIO, PT_RATIO, PPN_RATIO, PPP_RATIO, PP_TTR, P_TTR, PSent_RATIO, PPSent_RATIO, CSent_RATIO, CN_RATIO,CT_RATIO,C_TTR


def grammar_cohesion(id2ltp):
    id2grammarCohesion={}
    for id,ltpRes in id2ltp.items():
        curRes={}
        r2n, r2tokens, prp2n, dsp2sent, cnj2sent, cnj2n, cnj2tokens=coreference_conjunctions_index(ltpRes['words'],ltpRes['pos'])

        # print(id,r2n, r2tokens, prp2n, dsp2sent, cnj2sent, cnj2n, cnj2tokens)

        curRes['r2n']=r2n
        curRes['r2tokens']=r2tokens
        curRes['prp2n']=prp2n
        curRes['dsp2sent']=dsp2sent
        curRes['cnj2sent']=cnj2sent
        curRes['cnj2n']=cnj2n
        curRes['cnj2tokens']=cnj2tokens

        id2grammarCohesion[id]=curRes
    return id2grammarCohesion

# id2grammarCohesion=grammar_cohesion(id2ltp)
