import sys,pickle
import pandas as pd
from collections import Counter

from lexical_overlap import *
from grammatical_cohesion import *

def add_parameters(params, **kwargs):
    params.update(kwargs)

def get_index(essay,essay_pos,essay_svo):
	essay_index = {}

	t = get_SO_TTR_RATIO_index(essay_svo)
	essay_index.update(argument_TTR = t[0], subject_TTR = t[1], object_TTR = t[2], subject_p_RATIO = t[3], subject_n_RATIO = t[4])

	essay_only_noun = get_essay_only_noun(essay, essay_pos)

	t = get_synonymy_overlap_index(essay, essay_only_noun)
	essay_index.update(sent_local_synonymy_overlap = t[0], sent_global_synonymy_overlap = t[1], sent_local_noun_synonymy_overlap = t[2],sent_global_noun_synonymy_overlap = t[3])

	t = get_SO_overlap_index(essay_svo)
	essay_index.update(sent_local_subject_overlap = t[0], sent_global_subject_overlap = t[1], sent_local_object_overlap = t[2], sent_global_object_overlap = t[3])

	t = get_noun_overlap_index(essay_only_noun)
	essay_index.update(sent_local_noun_overlap = t[0],sent_global_noun_overlap = t[1])

	# essay_index.update(theme_synonymy_overlap = get_theme_synonymy_overlap_index(theme, essay))

	t = get_central_sent_index(essay)
	essay_index.update(central_sent_count = t[0], central_sent_RATIO = t[1])

	# 语法衔接
	t = get_grammatical_cohesion_index(essay, essay_pos)
	essay_index.update(PN_RATIO = t[0], PT_RATIO = t[1], PPN_RATIO = t[2], PPP_RATIO = t[3], PP_TTR = t[4], P_TTR = t[5], PSent_RATIO = t[6], PPSent_RATIO = t[7], CSent_RATIO = t[8], CN_RATIO = t[9],CT_RATIO = t[10],C_TTR = t[11])
	
	return essay_index


def ltp2index(ltp_file, svo_file, index_file):
	with open(ltp_file,'rb') as f:
		id2ltp=pickle.load(f)
	with open(svo_file,'rb') as f:
		id2ltpsvo = pickle.load(f)

	id2index = {}
	i = 1
	for e_id in id2ltp.keys():
		# print(i,'\t',e_id)
		essay, essay_pos, essay_svo = id2ltp[e_id]['words'], id2ltp[e_id]['pos'], id2ltpsvo[e_id]
		id2index[e_id] = get_index(essay, essay_pos, essay_svo)	
		i += 1

	df_li = list()
	for e_id,e_index in id2index.items():
		cur_li = [e_id] + list(e_index.values())
		df_li.append(cur_li)
	random_id = list(id2ltp.keys())[0]
	head = ['id'] + list(id2index[random_id].keys())
	df = pd.DataFrame(df_li, columns=head)
	df.to_excel(index_file, index=False)


if __name__ == '__main__':
	need_pickle_index = False
	if need_pickle_index:
		with open('/home/pyp/D/mywork/group/LTP_cohesion/b_file2pickle/res/essay_clean_ltp.pickle','rb') as f:
			id2ltp=pickle.load(f)
		with open('/home/pyp/D/mywork/group/LTP_cohesion/c_lexical_cohesion/essay_clean_ltp_svo.pickle','rb') as f:
			id2ltpsvo = pickle.load(f)
		
		id2index = {}
		i = 1
		for e_id in id2ltp.keys():
			print(i,'\t',e_id)
			essay, essay_pos, essay_svo = id2ltp[e_id]['words'], id2ltp[e_id]['pos'], id2ltpsvo[e_id]
			id2index[e_id] = get_index(essay, essay_pos, essay_svo)
			i += 1

		with open('./essay_clean_cohesion_index.pickle','wb') as f:
			pickle.dump(id2index, f)

	# 得到id和标题、文体之间的映射
	need_id2title_style = True
	if need_id2title_style:
		df = pd.read_excel('/home/pyp/D/mywork/group/corpus/HSK动态作文语料库（汉语二语）/essay_info.xlsx', usecols=[0,1,2,9])
		df_li = df.values.tolist()
		m_id = [str(t[0]) for t in df_li]
		title = [t[1] for t in df_li]
		style = [t[2] for t in df_li]
		score = [t[3] for t in df_li]
		id2title = dict(zip(m_id, title))
		id2style = dict(zip(m_id, style))
		id2score = dict(zip(m_id, score))

		# print(*df_li[0:10],sep='\n')
		# print(id2title['200405610610150012'],id2style['200405610610150012'])

		# print(*dict(Counter(title)).items(),sep='\n')

	# 得到绿色食品与饥饿的衔接特征的xlsx
	need_cohindex_xlsx = True
	if need_id2title_style and need_cohindex_xlsx:
		with open('./essay_clean_cohesion_index.pickle','rb') as f:
			id2index = pickle.load(f)

		index_li = []
		for e_id,e_index in id2index.items():
			if id2title[e_id] == '一封写给父母的信':
				cur_row = [e_id,id2score[e_id]] + list(e_index.values())
				index_li.append(cur_row)
		head = ['id','socre'] + list(id2index['199312104523100003'].keys())

		df = pd.DataFrame(index_li,columns=head)

		df.to_excel("一封写给父母的信-衔接特征.xlsx",index=False)


	