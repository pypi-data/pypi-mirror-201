import bnlearn
from kolibri.backend.bn.structure import *
def learn_structure_from_data(data, method_type='cs', score_type='k2', threshold=0.1, rank=3):

    columns=list(data.columns.values)
    nt=None
    if method_type=='nt':
        nt=Notears(w_threshold=threshold)
    elif method_type=='lr':
        nt=NotearsLowRank(w_threshold=threshold)
    elif method_type=='nl':
        nt=NotearsNonlinear(w_threshold=threshold)
    elif method_type=='gl':
        nt=GolemModel()

    if method_type=='lr':
        nt.learn(data.values, columns=columns, rank=rank)
    else:
        return bnlearn.structure_learning.fit(data, methodtype=method_type, scoretype=score_type)

    edges=[]
    for s, source  in enumerate(nt.causal_matrix):
        for t, target in enumerate(source):
            if target>0:
                edges.append((columns[s], columns[t]))


    return bnlearn.make_DAG(edges)


