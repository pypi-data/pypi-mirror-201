import bnlearn


def predict(model, variables, evidence):

    return bnlearn.inference.fit(model, variables=variables, evidence=evidence)