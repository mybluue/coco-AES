# 20211004
import pickle
from collections import Counter

with open('/home/pyp/D/mywork/group/LTP_cohesion/d_coh_index/word2tag.pickle','rb') as f:
    word2tag=pickle.load(f)

def getWordRel(w1,w2):
    res=6
    if w1 in word2tag and w2 in word2tag:
        tag1,tag2=word2tag[w1],word2tag[w2]
        # print(tag1+','+tag2)
        if tag1==tag2:
            pass
        elif tag1[0:7]==tag2[0:7]:
            res-=1
        elif tag1[0:5]==tag2[0:5]:
            res-=2
        elif tag1[0:4]==tag2[0:4]:
            res-=3
        elif tag1[0:2]==tag2[0:2]:
            res-=4
        elif tag1[0:1]==tag2[0:1]:
            res-=5
        else:
            res-=6
        return res
    else:
        return 0

# with open('/home/pyp/D/mywork/group/LTP_cohesion/b_file2pickle/res/essay_clean_ltp.pickle','rb') as f:
#     id2ltp=pickle.load(f)
# test={}
# test['199312104523100003']=id2ltp['199312104523100003']
# essay = test['199312104523100003']['words']

essay = [['快乐', '家庭', '旅游', '公司', '：', '\\n', '我', '在', '光明', '日报', '看到', '了', '贵', '公司', '的', '招聘', '启事', '。'], ['我', '对', '贵', '公司', '特别', '感', '兴趣', '。'], ['\\n', '我', '是', '×××', '，', '今年', '28', '岁', '了', '，', '今年', '在', '韩国', '的', '仁荷', '大学', '中文系', '毕业', '的', '。'], ['我', '是', '相貌', '端正', '、', '身体', '健康', '的', '人', '，', '大学', '四', '年级', '时', '，', '我', '打', '过', '工', '，', '就是', '导游', '。'], ['当时', '我', '陪', '从', '中国', '来', '的', '旅游团', '去', '釜山', '，', '我', '给', '他们', '介绍', '釜山', '的', '名胜古迹', '。'], ['我', '在', '导游', '方面', '有', '经验', '。'], ['我', '希望', '在', '贵', '公司', '工作', '，', '如果', '贵公司', '招聘', '我', '，', '我', '永远', '忘不', '了', '贵', '公司', '。'], ['\\n', '我', '等', '着', '你们', '的', '好', '消息', '。']]
essay_pos = [['a', 'n', 'v', 'n', 'wp', 'wp', 'r', 'p', 'n', 'n', 'v', 'u', 'r', 'n', 'u', 'v', 'n', 'wp'], ['r', 'p', 'r', 'n', 'd', 'v', 'n', 'wp'], ['wp', 'r', 'v', 'ws', 'wp', 'nt', 'm', 'q', 'u', 'wp', 'nt', 'p', 'ns', 'u', 'nz', 'n', 'n', 'v', 'u', 'wp'], ['r', 'v', 'n', 'a', 'wp', 'n', 'a', 'u', 'n', 'wp', 'n', 'm', 'n', 'n', 'wp', 'r', 'v', 'u', 'n', 'wp', 'v', 'n', 'wp'], ['nt', 'r', 'v', 'p', 'ns', 'v', 'u', 'n', 'v', 'ns', 'wp', 'r', 'p', 'r', 'v', 'ns', 'u', 'n', 'wp'], ['r', 'p', 'n', 'n', 'v', 'n', 'wp'], ['r', 'v', 'p', 'r', 'n', 'v', 'wp', 'c', 'r', 'v', 'r', 'wp', 'r', 'd', 'v', 'v', 'r', 'n', 'wp'], ['wp', 'r', 'v', 'u', 'r', 'u', 'a', 'n', 'wp'], ['wp']]

def get_essay_only_noun(essay,essay_pos):
	return [[essay[i][j] for j in range(len(essay[i])) if essay_pos[i][j] == 'n'] for i in range(len(essay))]


"""
计算两个句子之间的同义关系累加
"""
def get_synonymy_sum(sent1,sent2):
	synonymy_sum = 0
	for w1 in sent1:
		for w2 in sent2:
			synonymy_sum += getWordRel(w1, w2)
	return synonymy_sum

def get_synonymy_overlap_index(essay,essay_only_noun):
	sent_local_synonymy_overlap = 0
	sent_global_synonymy_overlap = 0
	sent_local_noun_synonymy_overlap = 0
	sent_global_noun_synonymy_overlap = 0
	sent_count = len(essay)
	for i in range(0,sent_count-1):
		for j in range(i+1,sent_count):
			if j == i+1:
				sent_local_synonymy_overlap += get_synonymy_sum(essay[i], essay[j])
				sent_local_noun_synonymy_overlap += get_synonymy_sum(essay_only_noun[i], essay_only_noun[j])
			sent_global_synonymy_overlap += get_synonymy_sum(essay[i], essay[j])
			sent_global_noun_synonymy_overlap += get_synonymy_sum(essay_only_noun[i], essay_only_noun[j])

	sent_local_synonymy_overlap /= (sent_count + 1)
	sent_global_synonymy_overlap /= ((sent_count - 1) * sent_count / 2 + 1)
	sent_local_noun_synonymy_overlap /= (sent_count + 1)
	sent_global_noun_synonymy_overlap /= ((sent_count - 1) * sent_count / 2 + 1)

	return sent_local_synonymy_overlap, sent_global_synonymy_overlap, sent_local_noun_synonymy_overlap,sent_global_noun_synonymy_overlap

essay_SVO = [[['我', '赞同', '观点', 'r', 'v', 'n'], ['父母', '是', '老师', 'n', 'v', 'n']], [['我们', '出生', '--object', 'r', 'v', '--pos']], [['我们', '增加', '财富', 'r', 'v', 'n']], [['父母', '是', '人', 'n', 'v', 'n'], ['我们', '接触', '--object', 'r', 'v', '--pos'], ['习惯', '是', '学', 'n', 'v', 'v']], [['我们', '学习', '--object', 'r', 'v', '--pos'], ['我们', '认为', '是', 'r', 'v', 'v']], [['习惯', '是', '养成', 'n', 'v', 'v'], ['习惯', '是', '发生', 'n', 'v', 'v']], [['孩子', '长大', '--object', 'n', 'v', '--pos'], ['父母', '见面', '--object', 'n', 'v', '--pos']], [['她', '认为', '是', 'r', 'v', 'v'], ['家庭', '是', '幸福', 'n', 'v', 'a'], ['她', '体验', '--object', 'r', 'v', '--pos']], [['她', '接触', '快乐', 'r', 'v', 'a'], ['她', '提出', '疑问', 'r', 'v', 'n']], [['家庭', '是', '吵架', 'n', 'v', 'v'], ['这', '是', '习惯', 'r', 'v', 'n']], [['影响', '重要', '--object', 'v', 'a', '--pos']], [['父亲', '打骂', '母亲', 'n', 'v', 'n'], ['孩了', '认为', '--object', 'n', 'v', '--pos'], ['这', '没有', '错', 'r', 'd', 'v']], [['他', '做', '事情', 'r', 'v', 'n']], [['父母', '习惯', '读书', 'n', 'v', 'v'], ['孩子', '学', '做', 'n', 'v', 'v']], [['孩子', '学会', '习惯', 'n', 'v', 'n']], [['我', '认为', '是', 'r', 'v', 'v'], ['父母', '是', '老师', 'n', 'v', 'n']], [['父母', '做好', '榜样', 'n', 'v', 'n']], [['孩子', '坏', '--object', 'n', 'a', '--pos']], [[]]]

def get_SO_TTR_RATIO_index(essay_SVO):
	essay_subject = []
	essay_object = []
	essay_noun_subject = []
	essay_pronoun_subject = []

	for sent_SVO in essay_SVO:
		for subsent_SVO in sent_SVO:
			if len(subsent_SVO) == 6:
				essay_subject.append(subsent_SVO[0])
				essay_object.append(subsent_SVO[2])
				if subsent_SVO[3] == 'n':
					essay_noun_subject.append(subsent_SVO[0])
				elif subsent_SVO[3] == 'r':
					essay_pronoun_subject.append(subsent_SVO[0])

	argument_TTR = len(list(set(essay_noun_subject))) / (len(essay_noun_subject) + 1)
	subject_TTR = len(list(set(essay_subject))) / (len(essay_subject) + 1)
	object_TTR = len(list(set(essay_object))) / (len(essay_object) + 1)

	subject_p_RATIO = len(essay_pronoun_subject) / (len(essay_subject) + 1)
	subject_n_RATIO = len(essay_noun_subject) / (len(essay_subject) + 1)

	return argument_TTR, subject_TTR, object_TTR, subject_p_RATIO, subject_n_RATIO


def get_SO_overlap_index(essay_SVO):
	sent_local_subject_overlap = 0
	sent_global_subject_overlap = 0
	sent_local_object_overlap = 0
	sent_global_object_overlap = 0
	sent_count = len(essay_SVO)

	for i in range(0,sent_count-1):
		for j in range(i+1,sent_count):
			sent1_subject = [t[0] for t in essay_SVO[i] if t]
			sent2_subject = [t[0] for t in essay_SVO[j] if t]
			sent1_object = [t[2] for t in essay_SVO[i] if t and t[2] != '--object']
			sent2_object = [t[2] for t in essay_SVO[j] if t and t[2] != '--object']

			subject_overlap = len(list(set(sent1_subject).intersection(set(sent2_subject))))
			object_overlap = len(list(set(sent1_object).intersection(set(sent2_object))))

			if j == i+1:
				sent_local_subject_overlap += subject_overlap
				sent_local_object_overlap += object_overlap

			sent_global_subject_overlap += subject_overlap
			sent_global_object_overlap += object_overlap

	sent_local_subject_overlap /= (sent_count + 1)
	sent_global_subject_overlap /= ((sent_count - 1) * sent_count / 2 + 1)
	sent_local_object_overlap /= (sent_count + 1)
	sent_global_object_overlap /= ((sent_count - 1) * sent_count / 2 + 1)

	return sent_local_subject_overlap, sent_global_subject_overlap, sent_local_object_overlap, sent_global_object_overlap

def get_noun_overlap_index(essay_only_noun):
	sent_local_noun_overlap = 0
	sent_global_noun_overlap = 0
	sent_count = len(essay_only_noun)

	for i in range(0,sent_count-1):
		for j in range(i+1,sent_count):
			sent_noun_overlap_cnt = len(list((Counter(essay_only_noun[i])&Counter(essay_only_noun[j])).elements()))
			if j == i+1:
				sent_local_noun_overlap += sent_noun_overlap_cnt
			sent_global_noun_overlap += sent_noun_overlap_cnt

	sent_local_noun_overlap /= (sent_count + 1)
	sent_global_noun_overlap /= ((sent_count - 1) * sent_count / 2 + 1)

	return sent_local_noun_overlap,sent_global_noun_overlap

def get_theme_synonymy_overlap_index(theme,essay):
	theme_synonymy_overlap = 0
	for sent in essay:
		theme_synonymy_overlap += get_synonymy_sum(theme, sent)
	return theme_synonymy_overlap

def get_central_sent_index(essay):
	sent_count = len(essay)
	# 记录一个句子与所有其它句子的重叠系数之和
	sent_overlap_sum = 0
	# 和当前句子重叠系数不为0的句子数
	none_zero_sent_cnt = 0
	# 中心句子数
	central_sent_count = 0
	for i in range(sent_count):
		sent_overlap_sum = 0
		none_zero_sent_cnt = 0
		for j in range(sent_count):
			if j != i and get_synonymy_sum(essay[i], essay[j]) > 0:
				sent_overlap_sum += get_synonymy_sum(essay[i], essay[j])
				none_zero_sent_cnt += 1
		if none_zero_sent_cnt and sent_overlap_sum // none_zero_sent_cnt > 40:
			central_sent_count += 1
	central_sent_RATIO = central_sent_count / (sent_count + 1)
	return central_sent_count, central_sent_RATIO


def add_parameters(params, **kwargs):
    params.update(kwargs)

if __name__ == '__main__':
	with open('/home/pyp/D/mywork/group/LTP_cohesion/c_lexical_cohesion/essay_clean_ltp_svo.pickle','rb') as f:
		id2ltpsvo = pickle.load(f)
	# print(getWordRel('能力', '技能'))
	# print(get_synonymy_sum(essay[0], essay[1]))

	sent_count = len(essay)
	# for i in range(0,sent_count):
	# 	print(i,end=':\t')
	# 	for j in range(0,sent_count):
	# 		if j != i:
	# 			print(get_synonymy_sum(essay[i], essay[j]),end=',\t')
	# 	print('\n')
	# print(get_central_sent_index(essay))
	for essay_SVO in list(id2ltpsvo.values())[0:10]:
		print(get_SO_TTR_RATIO_index(essay_SVO))

	# print(get_synonymy_overlap_index(essay,essay_only_noun))
	# print(get_SO_overlap_index(essay_SVO))

	# print(essay_only_noun)
	# print(get_noun_overlap_index(essay_only_noun))

	essay_only_noun = get_essay_only_noun(essay, essay_pos)

	index = {}
	t = get_SO_TTR_RATIO_index(essay_SVO)
	print(type(t))
	index.update(argument_TTR = t[0], subject_TTR = t[1], object_TTR = t[2], subject_p_RATIO = t[3], subject_n_RATIO = t[4])
	print(index)

	
