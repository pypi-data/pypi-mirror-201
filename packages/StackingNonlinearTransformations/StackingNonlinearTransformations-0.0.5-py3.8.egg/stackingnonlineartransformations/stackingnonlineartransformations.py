from sklearn.model_selection import cross_validate
import numpy as np

class StackingNonlinearTransformations():
    def __init__(self, base_models, meta_model, n_folds=10):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds
        
   
    def NonlinearTransformations(self, x, NT, **kwargs):
        if NT == None:
            return x
        elif NT == "relu":
            return x
        elif NT == "sigmoid":
            return 1.0 / (1 + np.exp(-x))
        elif NT == "elu":
            if 'alpha' not in kwargs:
                raise ValueError('alpha is not given')
            alpha = kwargs["alpha"]
            return np.where(x < 0, alpha * (np.exp(x) - 1), x)
        elif NT == "tanh":
            return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
        elif NT == "sin":
            return np.sin(x)
        elif NT == "cos":
            return np.cos(x)
        elif NT == "softmax":
            exps = np.exp(x - np.max(x, axis=-1, keepdims=True))
            return exps/np.sum(exps, axis=-1, keepdims=True)
        elif NT == "softplus":
            return np.log(1 + np.exp(x))


    def base_model_fit(self, train_X, train_y, test_X, test_y,cv=10):
        best_models = dict()
        for name in self.base_models.keys():
            model = self.base_models[name]
            cv_results = cross_validate(model, train_X, train_y.values, cv=cv, return_estimator=True, return_train_score=True)
            test_results = []
            for m in cv_results['estimator']:
                test_results.append(m.score(test_X, test_y.values))

            # 保存在测试集上性能最好的模型
            ind = np.argmax(test_results)
            best_models[name] = cv_results['estimator'][ind]
            



        train_ = np.zeros((train_X.shape[0], len(self.base_models ) + len(train_X.columns)))
        test_ = np.zeros((test_X.shape[0], len(self.base_models) + len(test_X.columns)))
        
        train_[:,0:len(train_X.columns)] = train_X
        test_[:,0:len(test_X.columns)] = test_X

        for i, name in enumerate(best_models):
            model = best_models[name]
            train_pred = model.predict(train_X)
            test_pred = model.predict(test_X)

            train_[:, len(train_X.columns)+i] = self.NonlinearTransformations(train_pred,"sigmoid")
            test_[:,len(test_X.columns)+i] = self.NonlinearTransformations(test_pred,"sigmoid")

            
        return train_, test_

    def fit(self, train_X, train_y, test_X, test_y, cv=10):

        new_train, new_test = self.base_model_fit(train_X, train_y, test_X, test_y,cv)
        model = list(self.meta_model.values())[0]
        cv_results = cross_validate(model, new_train, train_y.values, cv=cv, return_estimator=True, return_train_score=True)
        test_results = []
        for m in cv_results['estimator']:
            test_results.append(m.score(new_test, test_y.values))
        ind = np.argmax(test_results)
        new_best_models = cv_results['estimator'][ind]
        model = new_best_models
        train_pred = model.predict(new_train)
        test_pred = model.predict(new_test)
        train_pred_prob = model.predict_proba(new_train)
        test_pred_prob = model.predict_proba(new_test)
        
        return train_pred, test_pred, train_pred_prob, test_pred_prob