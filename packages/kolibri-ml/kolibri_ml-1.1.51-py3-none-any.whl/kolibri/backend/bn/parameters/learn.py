import bnlearn


def learn_parameters(model_structure, data, methodtype='maximumlikelihood'):
     model_mle=  bnlearn.parameter_learning.fit(model_structure, data, methodtype=methodtype)
     bnlearn.print_CPD(model_mle)
     return model_mle