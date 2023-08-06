from sklearn.linear_model import Lasso, LassoCV, ElasticNetCV, LassoLarsIC, SGDClassifier, LogisticRegressionCV,LogisticRegression
from sklearn.neighbors import KNeighborsClassifier,RadiusNeighborsClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC,SVR,LinearSVC,NuSVC,NuSVR
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, RandomForestRegressor,GradientBoostingClassifier,GradientBoostingRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB, ComplementNB
from scipy.stats import randint,uniform
from xgboost import XGBClassifier, XGBRegressor
#from catboost import CatBoostClassifier, CatBoostRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from skrvm import RVR, RVC
import numpy as np
#from bartpy.sklearnmodel import SklearnModel
#from bartpy.extensions.baseestimator import ResidualBART

class ML():
    def __init__(self, modle, Type='C', SearchCV='GSCV', *array, **dicto):
        self.modle = modle
        self.Type  = Type
        self.SearchCV = SearchCV
        self.array = array
        self.dicto = dicto

    def GetPara(self):
        if self.Type == 'C' :
            Parameters = self.Classification()
        elif self.Type == 'R' :
            Parameters = self.Regression()

        self.estimator  =  Parameters[self.modle]['estimator']
        self.parameters =  Parameters[self.modle]['parameters'][self.SearchCV]
        return self

    def Classification(self):
        return {
        'RF'   : {
            'estimator' : RandomForestClassifier(oob_score=True, n_estimators=100, n_jobs=10, random_state=123456),
            'parameters': {
                'GSCV'  : { 'max_features'     : [0.6, 0.7, 0.8, 0.9, 'sqrt','log2', None],
                            'max_depth'        : [3, 4, None],
                            'class_weight'     : ['balanced', 'balanced_subsample', None], 
                            'min_samples_split': [2, 4, 6 ],
                            'min_samples_leaf' : [1, 2, 3 ],
                            'criterion'        : ['gini', 'entropy'] },
                'RSCV'  : { 'max_features': [ 0.6, 0.7, 0.8, 0.9, 'sqrt','log2', None ],
                            'max_depth'   : [ 3, 4, None ],
                            'criterion'   : ['gini', 'entropy'],
                            'class_weight': ['balanced', 'balanced_subsample', None], 
                            'min_samples_split' : [ 2, 4, 6, 8, 11, 15],
                            'min_samples_leaf'  : [ 1, 2, 3, 7, 11, 15],
                            }
                }},

        'GBDT'          : {
            'estimator' : GradientBoostingClassifier(n_estimators=100, random_state=123456),
            'parameters': {
                'GSCV'  : { 'max_features': (0.5, 0.75, 0.8, 0.9, 'auto'),
                            'loss' : ['deviance', 'exponential'],
                            'max_depth': [ 3, 4, 5 ],
                            'learning_rate': [0.005, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9],
                            'min_samples_split':[2, 3, 4, 5],
                            'subsample': [0.75, 0.85, 0.95 ]},
                'RSCV'  : { 'max_features': (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 'auto', 'log2', None),
                            'loss' : ['deviance', 'exponential'],
                            'max_depth': [ 3, 4, 5, 6, 7, 8, 9, 11, 15],
                            'learning_rate': [0.005, 0.01, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9],
                            'min_samples_split':[2, 3, 4, 5, 6, 8],
                            'subsample': [0.7, 0.8, 0.9, 1]},
                }},

        'XGB'           : {
            'estimator' : XGBClassifier(
                            objective    ='binary:logistic', # multi:softprob
                            booster      ='gbtree',
                            silent       =True,
                            missing      =None,
                            n_jobs       =8,
                            random_state =123456),
            'parameters': {
                'GSCV'  : { 'colsample_bytree' : [0.75, 0.85, 0.95 ],
                            'subsample'        : [0.75, 0.85, 0.95 ],
                            'reg_alpha'        : [0, 0.1, 0.5, 1, 2  ],
                            'reg_lambda'       : [0.1, 0.5, 1, 2, 2.5 ],
                            'max_depth'        : [3, 4, 5, 6],
                            'learning_rate'    : [0.01, 0.05, 0.1, 0.2],
                            #'min_child_weight' : [1, 2],
                          },

                'RSCV'  : { 'subsample'        : [0.7, 0.8, 0.85],
                            'colsample_bytree' : [0.7, 0.8, 0.9],
                            'colsample_bylevel': [0.7, 0.8, 0.9],
                            'max_delta_step'   : [0, 1],
                            'colsample_bynode' : [1],
                            'scale_pos_weight' : [0.8, 1, 1.2],
                            'base_score'       : [0.5],
                            'gamma'            : [0, 0.005, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9],
                            'min_child_weight' : [1, 2, 3, 4, 5],
                            'min_samples_split': [2, 3, 4, 5, 6, 7],
                            'max_depth'        : [3, 4, 5, 6, 7, 8],
                            'reg_lambda'       : [0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.96, 1],
                            'reg_alpha'        : [0, 0.001, 0.01, 0.1, 0.2, 0.3, 0.5, 0.7],
                            'learning_rate'    : [0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5],
                           },
                }},

        'LGBM'          : {
            'estimator' : LGBMClassifier(
                            boosting_type='gbdt',
                            n_estimators=100,
                            min_split_gain=0.0,
                            min_child_weight=1e-3,
                            min_child_samples=10,
                            subsample_freq=0,
                            random_state=123456,
                            n_jobs=-1,
                            silent=False,
                            importance_type='split',
                            verbose = -1,
                            ),
            'parameters': {
                'GSCV'  : { 'num_leaves'       : [9, 17, 33, 65],
                            'max_depth'        : [-1, 3, 4, 5, 6],
                            'learning_rate'    : [0.01, 0.05, 0.1, 0.2],
                            'reg_alpha'        : [0.01, 0.1, 0.5, 1, 1.5, 2],
                            'reg_lambda'       : [0.01, 0.1, 0.5, 1, 1.5, 2],
                            'class_weight'     : ['balanced', None, ],
                            'subsample'        : [0.7, 0.78, 0.85],
                            'colsample_bytree' : [0.7, 0.78, 0.85],
                          },
                'RSCV'  : { 'num_leaves'       : [9, 17, 33, 65, 129],
                            'max_depth'        : [-1, 3, 4, 5, 6, 7],
                            'learning_rate'    : [0.01, 0.05, 0.1, 0.2],
                            'reg_alpha'        : [0, 0.01, 0.1, 0.5, 0.75, 1, 1.5, 2, 2.5, 3],
                            'reg_lambda'       : [0, 0.01, 0.1, 0.5, 0.75, 1, 1.5, 2, 2.5, 3],
                            'class_weight'     : ['balanced', None, ],
                            'subsample'        : [0.7, 0.78, 0.85],
                            'colsample_bytree' : [0.7, 0.78, 0.85],
                          }
                }},

        'AdaB_DT'   : {
            'estimator' : AdaBoostClassifier(DecisionTreeClassifier(criterion='gini', splitter='best',
                            class_weight='balanced', min_samples_leaf =1, max_features=None), random_state=123456),
            'parameters': {
                'GSCV'  : { 'n_estimators': range(400, 800, 1000),
                            'algorithm': ['SAMME', 'SAMME.R'],
                            "learning_rate": [0.3, 0.5, 0.7, 0.9, 0.95, 1, 2]},
                'RSCV'  : {}
                }},

        'MLP'           : {
            'estimator' : MLPClassifier(max_iter=15000,
                                        tol =1e-4,
                                        random_state=123456),
            'parameters': {
                'GSCV'  : { 'alpha': [10**i for i in [-6, -5, -4, -3, -1, 1]],
                            'solver':['adam', 'lbfgs', 'sgd'],
                            'activation': ["logistic", 'identity', "relu", "tanh"],
                            'hidden_layer_sizes': [ (50, 30, 20, 10, 10,  ), (15, 25, 15, 10, ), (8, 15, 10, 10, ), (30, 10, 40, 10, ), (10, 20, 10, 10, )],
                            'learning_rate': ["constant", "invscaling", "adaptive"]},
                'RSCV'  : {'hidden_layer_sizes': [ (randint.rvs(8,30,1), randint.rvs(5,20,1), randint.rvs(5,30,1),) ,
                                                   (randint.rvs(8,40,1), randint.rvs(5,40,1), )],
                            'activation': ["logistic", 'identity', "relu", "tanh"],
                            'solver':['adam', 'lbfgs', 'sgd'],
                            'alpha': [10**i for i in [-6, -5, -4, -3, -1, 1]], #uniform(1e-06, 0.9),
                            'learning_rate': ["constant", "invscaling", "adaptive"]}
                }},

        'LinearSVM'  : {
            'estimator' : LinearSVC(penalty='l2', dual=True, random_state=123456),
            'parameters': {
                'GSCV'  : { 'loss': ['hinge', 'squared_hinge'],
                            'tol': [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2 ],
                            'C': np.power(10, np.linspace(-1.7, 1.7, 20)),
                            'max_iter':[int(8e6), int(1.5e7)]},
                'RSCV'  : {}
                }},
        'LinearSVMl1'   : {
            'estimator' : LinearSVC(penalty='l1', max_iter=int(1e6), random_state=123456),
            'parameters': {
                'GSCV'  : { 'dual' : [False, True],
                            'loss': ['squared_hinge'],
                            'tol': [ 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2 ],
                            'C': np.power(10, np.linspace(-2, 2, 10))},

                'RSCV'  : {}
                }},
        'SVMlinear'     : {
            'estimator' : SVC(kernel="linear", probability=True, decision_function_shape='ovr', random_state=123456),
            'parameters': {
                'GSCV'  : [{'tol': [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'C': np.power(10, np.linspace(-2, 2, 10)),
                           }],
                'RSCV'  : {}
                }},
        'SVMrbf'        : {
            'estimator' : SVC(kernel='rbf',  probability=True, decision_function_shape='ovr', random_state=123456),
            'parameters': {
                'GSCV'  : { 'gamma': [1e1, 1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 'scale'],
                            'tol': [ 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'C': np.power(10, np.linspace(-2, 2, 10)),
                          },
                'RSCV'  : {}
                }},
        'SVMpoly'        : {
            'estimator' : SVC(kernel='poly',  probability=True, decision_function_shape='ovr', random_state=123456),
            'parameters': {
                'GSCV'  : { 'gamma': [1e1, 1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 'scale'],
                            'tol': [ 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'C': np.power(10, np.linspace(-2, 2, 10)),
                          },
                'RSCV'  : {}
                }},
        'RVMrbf'        : {
            'estimator' : RVC(kernel='rbf', n_iter=1000, threshold_alpha=1e9),
            'parameters': {
                'GSCV'  : { 'tol': [ 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'alpha': [ 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
                            'beta': [ 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
                            'beta_fixed': [False],
                            'bias_used': [True],
                          },
                'RSCV'  : {}
                }},
        'RVMpoly'        : {
            'estimator' : RVC(kernel='poly', n_iter=1000, threshold_alpha=1e9),
            'parameters': {
                'GSCV'  : { 'tol': [ 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'alpha': [ 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
                            'beta': [ 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
                            'beta_fixed': [False],
                            'bias_used': [True]
                          },
                'RSCV'  : {}
                }},
        'SVM'           : {
            'estimator' : SVC(probability=True, decision_function_shape='ovr', random_state=123456),
            'parameters': {
                'GSCV'  : [{'kernel': ['rbf', 'sigmoid'],
                            'gamma': [1e1, 1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 'scale'],
                            'tol': [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'C': np.power(10, np.linspace(-2, 2, 10)),
                           },
                           {'kernel': ['poly'],
                            'degree' : [2, 3, 4, 5],
                            'gamma': [1e1, 1e0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 'auto'],
                            'tol': [1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1 ],
                            'C': np.power(10, np.linspace(-2, 2, 10)),
                           },
                          ],
                'RSCV'  : {}
                }},
        'nuSVMrbf'      : {
            'estimator' : NuSVC(probability=True, decision_function_shape='ovr', random_state=123456),
            'parameters': {
                'GSCV'  : { 'kernel': ['rbf'],
                            'nu': [0.8, 0.9, 1],
                            'gamma': [1e-2,1e-3,1e-4,1e-5,5e-2,5e-3,5e-4,'auto'],
                            'tol': [1e-6, 1e-5, 5e-5, 1e-4, 5e-3, 3e-3, 1e-3, 1e-2, 5e-2]},
                'RSCV'  : {}
                }},

        'SGD'           : {
            'estimator' : SGDClassifier(max_iter = int(1e5), learning_rate='optimal', n_jobs=2, random_state=123456),
            'parameters': {
                'GSCV'  : [{ 'penalty' : ['l2','elasticnet'],
                             'loss': ['hinge','log','modified_huber','squared_hinge','perceptron' ],
                             'alpha': [5e-5, 1e-4, 5e-4, 1e-3, 1e-2, 1e-1, 1e0, 1e1 ],
                             'l1_ratio': [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9 ],
                             #'eta0' : [0, 0.0001, 0.001, 0.01, 0.1],
                             'tol': [1e-3, 5e-3, 1e-4, 1e-5, 1e-2]},
                          ],
                'RSCV'  : {}
                }},

        'KNN'           : {
            'estimator' : KNeighborsClassifier(n_jobs=2),
            'parameters': {
                'GSCV'  : { 'n_neighbors':[3, 4, 5, 6, 7, 8, 10, 12, 15],
                            'weights': ['uniform', 'distance'],
                            'algorithm': ['auto','ball_tree','kd_tree','brute'],
                            'leaf_size': [10,20,30,40, 50, 60, 70, 100],
                            'p': [1,2]},
                'RSCV'  : {}
                }},

        'RNN'           : {
            'estimator' : RadiusNeighborsClassifier(metric='minkowski', outlier_label=None, n_jobs=2),
            'parameters': {
                'GSCV'  : { 'radius': [1,2,3,4,5,10,15,20,23,26,30,35,40],
                            'weights': ['uniform', 'distance'],
                            'algorithm':['auto','ball_tree','kd_tree','brute'],
                            'leaf_size': [10,20,30,50,70,100,200],
                            'p': [1,2]},
                'RSCV'  : {}
                }},

        'GNB'           : {
            'estimator' : GaussianNB(priors=None, var_smoothing=1e-09),
            'parameters': {
                'GSCV'  : {'var_smoothing' : np.dot( np.array([[1e-11, 1e-10,1e-09,1e-08,1e-07]]).T, np.array([[1,3,5,7]]) ).flatten() },
                'RSCV'  : {}
                }},

        'BNB'           : {
            'estimator' : BernoulliNB(fit_prior=True, class_prior=None),
            'parameters': {
                'GSCV'  : {'alpha':[i/10 for i in range(1,21,1)], 'binarize' : [i/10 for i in range(1,10,1)] },
                'RSCV'  : {}
                }},

        'MNB'           : {
            'estimator' : MultinomialNB(fit_prior=True, class_prior=None),
            'parameters': {
                'GSCV'  : {'alpha':[i/10 for i in range(1,21,1)]},
                'RSCV'  : {}
                }},

        'CNB'           : {
            'estimator' : ComplementNB(fit_prior=True, class_prior=None, norm=False),
            'parameters': {
                'GSCV'  : {'alpha':[i/10 for i in range(1,21,1)]},
                'RSCV'  : {}
                }},

        'DT'    : {
            'estimator' : DecisionTreeClassifier(splitter='best', class_weight='balanced', random_state=123456),
            'parameters': {
                'GSCV'  : { 'max_features': (0.4, 0.5, 0.6, 0.7, 0.8, 'sqrt','log2','None'),
                            'min_samples_leaf' : (1,2,3) ,
                            'max_depth': (5, 8, 10, 15, 25, 30, None),
                            'criterion' : ['gini', 'entropy']},
                'RSCV'  : {}
                }},

        'LR'            : {
            'estimator' : LogisticRegression(random_state=123456,
                                             fit_intercept=True,
                                             max_iter=10000,
                                             multi_class='auto'),
            'parameters': {
                'GSCV'  : [ { 'penalty'  : ['l1'],
                              'tol'      : [ 1e-3, 1e-4,  1e-5, ],
                              'l1_ratio' : [None],
                              'solver'   : ['liblinear', 'saga']},
                            { 'penalty'  : ['l2'],
                              'tol'      : [1e-3, 1e-4,  1e-5, ],
                              'l1_ratio' : [None],
                              'solver'   : ['lbfgs', 'sag']},
                            { 'penalty'  : ['elasticnet'],
                              'tol'      : [ 1e-3, 1e-4, 1e-5, ],
                              'l1_ratio' : [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95],
                              'solver'   : ['saga']},
                          ],
                'RSCV'  : {}
                }},

        'LRCV'          : {
            'estimator' : LogisticRegressionCV(random_state=123456,
                                             fit_intercept=True,
                                             n_jobs = 30,
                                             multi_class='auto'),
            'parameters': {
                'GSCV'  : [ { 'penalty'  : [ 'elasticnet'],
                              'Cs'       : [ 10,
                                             np.power(10, np.arange(-4,4,0.4)),
                                             np.power(10, np.arange(-3,3,0.3))
                                           ],
                              'l1_ratios': [ [0.005, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9], ],
                              'max_iter' : [ int(4e4) ],
                              'cv'       : [ 10  ],
                              'solver'   : [ 'saga']},
                          ],
                'RSCV'  : [ { 'penalty'  : [ 'l1'],
                              'Cs'       : [ np.power(10, np.arange(-2,4,0.3)) ],
                              'l1_ratios': [ None ],
                              'max_iter' : [ int(6e4) ],
                              'cv'       : [ 10 ],
                              'solver'   : [ 'liblinear', 'saga']},
                            { 'penalty'  : [ 'l2'],
                              'l1_ratios': [ None ],
                              'max_iter' : [ int(6e4) ],
                              'cv'       : [ 10   ],
                              'Cs'       : [ np.power(10, np.arange(-2,4,0.3)) ],
                              'solver'   : [ 'lbfgs', 'sag']},
                            { 'penalty'  : [ 'elasticnet'],
                              'Cs'       : [ np.power(10, np.arange(-2,4,0.3)) ],
                              'max_iter' : [ int(6e4) ],
                              'cv'       : [ 10 ],
                              'solver'   : ['saga']},
                          ],
                }},

        'LassoCV'       : {
            'estimator' : LassoCV(cv=10,
                                  alphas=[0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1, 10],
                                  max_iter=20000,
                                  n_jobs=-1),
            'parameters': {
                'GSCV'  : { 'n_alphas': [200, 500],
                            'normalize':[False, True]},
                'RSCV'  : {}
                }},

        'Lasso'         : {
            'estimator' : Lasso(random_state=123456),
            'parameters': {
                'GSCV'  : { 'alpha': [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1, 10],
                            'max_iter': [15000],
                            'normalize':[False, True],
                            'precompute':[False, True]},
                'RSCV'  : {}
                }},

        'LLIC'          : {
            'estimator' : LassoLarsIC(fit_intercept=True,
                                      verbose=False,
                                      normalize=True,
                                      precompute='auto',
                                      max_iter=10000,
                                      eps=2.220446049250313e-16,
                                      copy_X=True,
                                      positive=False),
            'parameters': {
                'GSCV'  : { 'criterion' : ['aic','bic'],
                            },
                'RSCV'  : {}
                }},

        'ENet'          : {
            'estimator' : ElasticNetCV( cv=10,
                                        alphas=[0.001, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 1, 10],
                                        random_state=123456,
                                        n_jobs= 20,
                                        l1_ratio=[.01,.05, .1, .3, .5, .7, .9, .98]),
            'parameters': {
                'GSCV'  : { 'n_alphas' : [200, 500],
                            'max_iter' : [20000, 50000],
                            'tol'      : [1e-3, 1e-4, 1e-5, ],
                            'normalize': [False, True]},
                'RSCV'  : {}
                }},
        }

    def Regression(self):
        return {
        'RF'   : {
            'estimator' : RandomForestRegressor(n_jobs=-1, oob_score=True, n_estimators=200),
            'parameters': {
                'GSCV'  : { 'max_features': (0.4, 0.6, 0.8, 'auto'),
                            'max_depth': (5, 8, 12, 15, 25, None),
                            'n_estimators': [100, 200, 400, 600],
                            'min_samples_split':[2,5,10] },
                'RSCV'  : {}
                }},

        'Decis_Tree'    : {
            'estimator' : DecisionTreeRegressor(),
            'parameters': {
                'GSCV'  : { 'max_features': (0.4, 0.6, 0.8, 'auto'),
                            'max_depth': (5, 8, 12, 15, 25, None)},
                'RSCV'  : {}
                }},

        'SVM'           : {
            'estimator' : SVR(gamma='scale', kernel="linear"),
            'parameters': {
                'GSCV'  : {'C': [0.1, 0.5, 1, 5, 10, 100, 1000]},
                'RSCV'  : {}
                }},


        'MLP'           : {
            'estimator' : MLPRegressor(max_iter=3000, solver='lbfgs'),
            'parameters': {
                'GSCV'  : { 'alpha': [10**i for i in [-5, -3, -1, 1, 3]],
                            'max_iter':[10000, 15000],
                            'solver':['adam', 'lbfgs'],
                            'hidden_layer_sizes': [(50, 40, 20), (100, 30, 20), (200, 20), (10, 10, 10), (100, 20, 10)],
                            'learning_rate': ["constant", "invscaling", "adaptive"],
                            'activation': ["logistic", "relu", "tanh"]},
                'RSCV'  : {}
                }},

        'LassoCV'       : {
            'estimator' : LassoCV(cv=10, alphas=[0.0005, 0.001, 0.01,0.1, 0.5, 0.9, 1, 10], max_iter=5000),
            'parameters': {
                'GSCV'  : { 'n_alphas': [200, 500],
                            'max_iter':[5000, 10000, 15000],
                            'normalize':[False, True]},
                'RSCV'  : {}
                }},

        'Lasso'         : {
            'estimator' : Lasso(alpha=1, max_iter=5000),
            'parameters': {
                'GSCV'  : { 'alpha': [0.1, 0.5, 0.9, 1, 5, 10],
                            'max_iter': [5000, 10000, 15000],
                            'normalize':[False, True],
                            'precompute':[False, True]},
                'RSCV'  : {}
                }},

        'ENet'          : {
            'estimator' : ElasticNetCV( cv=10,
                                        alphas=[0.0001, 0.0005, 0.001, 0.01, 0.5, 0.1,1, 10],
                                        max_iter=5000,
                                        l1_ratio=[.01, .1, .5, .7, .9, .95, .99]),
            'parameters': {
                'GSCV'  : { 'n_alphas': [200, 500],
                            'max_iter':[5000, 10000, 15000],
                            'normalize':[False, True]},
                'RSCV'  : {}
                }},

        'BayesianRidge' : {
            'estimator' : '',
            'parameters': {
                'GSCV'  : {},
                'RSCV'  : {}
                }},

        'LogistR'       : {
            'estimator' : LogisticRegression(random_state=None,
                                              solver='lbfgs',
                                              fit_intercept=True,
                                              max_iter=500,
                                              multi_class='auto'),
            'parameters': {
                'GSCV'  : {},
                'RSCV'  : {}
                }},
        }

