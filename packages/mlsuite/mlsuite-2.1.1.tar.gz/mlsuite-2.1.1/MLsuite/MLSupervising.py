#===================================================
#
# Project      : mlsuite build model
# Description  : build 13 models by StratifiedShuffleSplit
# Usage        : ./MLSupervising.py 
# Author       : Suxing Li
# Email        : li.suxing@genecast.com.cn
# Created at   : 2022-05-12
#
#====================================================


from .MLUtilities import MyThread, _predict_proba_lr, CrossvalidationSplit, Check_Label, Check_Binar
from .MLEstimators import ML
from .MLOpenWrite import OpenM, Openf
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import (accuracy_score, f1_score, recall_score, precision_score,
                             balanced_accuracy_score, roc_auc_score, average_precision_score)
from sklearn.preprocessing import OneHotEncoder
from sklearn.calibration import CalibratedClassifierCV
from scipy.sparse import vstack
import os
import numpy as np
import pandas as pd
import re
import time
import joblib
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100000)
pd.set_option('display.width', 100000)


# obj: data grouping (default is 13 sets of data)
class sampleSplit:
    def __init__(self, arg):
        self.arg = arg
    def CVSplit(self, Xdf, Ydf):
        all_test = []
        all_split = []
        if self.arg.crossV == 1:
            all_split = [[range(Xdf.shape[0]), range(Xdf.shape[0])]]
        else:
            CVS = CrossvalidationSplit(
                n_splits=self.arg.crossV, test_size=self.arg.testS, CVt=self.arg.CVfit, n_repeats=2, leavP=self.arg.leavP, random_state=self.arg.random)
            SFA = CrossvalidationSplit(
                n_splits=self.arg.crossV, test_size=self.arg.testS, CVt='SFA', n_repeats=2, leavP=self.arg.leavP, random_state=self.arg.random)
            for train_index, test_index in CVS.split(Xdf, Ydf):
                all_test.extend(test_index)
                all_split.append([train_index.tolist(), test_index.tolist()])
            # if the unique of all test sample is not equal to input sample, add other 3 sets data by SFA method spliting
            if self.arg.CVfit == 'SSA':
                if len(set(all_test)) < len(Ydf):
                    all_add = [[tr.tolist(), te.tolist()]
                               for tr, te in SFA.split(Xdf, Ydf)]
                    all_split += all_add
        return(all_split)


class HyperparamOptimal():
    def __init__(self, arg, log, model, y_variable_type="C",  y_variable_class=2, score= None):
        self.arg = arg
        self.log = log
        self.model = model
        self.Type = y_variable_type
        self.MClass = y_variable_class
        self.score = score
    
    def Pdecorator(self):
        # sample split
        if self.Type == 'C':
            self.SSS = CrossvalidationSplit(n_splits=9, test_size=self.arg.GStestS, CVt='SSS', random_state=self.arg.random)
        elif self.Type == 'R':
            self.SSS = CrossvalidationSplit(n_splits=3, n_repeats=3, CVt='RSKF', random_state=self.arg.random)
        else:
            self.SSS = ''
        # get estimator and parameters
        self.estimator = ML(self.model, Type=self.Type).GetPara().estimator
        if self.arg.SearchCV:
            self.parameters = ML(self.model, Type=self.Type, SearchCV=self.arg.SearchCV).GetPara().parameters
        else:
            self.parameters = {}
        
    def Hyperparemet(self, x_train, x_test, y_train, y_test):
        HyperparamOptimal.Pdecorator(self)
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.log += HyperparamOptimal.logRecord('info', 'hyperparameter optimization in the %s model......\n', self.model)
        if (self.MClass > 2) & (self.model in ['XGB']):
            self.estimator = self.estimator.set_params(objective='multi:softprob')
        if self.model in ['XGB']:
            _n_jobs = 20
            if 'scale_pos_weight' in self.parameters.keys():
                pos_weight = y_train.value_counts(normalize=True)
                self.parameters['scale_pos_weight'] += ((1-pos_weight)/pos_weight).to_list()
                self.parameters['scale_pos_weight'] = list(set(self.parameters['scale_pos_weight']))
        else:
            _n_jobs = self.arg.n_job
        # add hyperopt Spearmint hyperparameter
        if not self.arg.SearchCV:
            clf = self.estimator
            self.log += HyperparamOptimal.logRecord('info','decrepate hyperparameter optimization......\n')
        elif self.arg.SearchCV == 'GSCV':
            clf = GridSearchCV(
                estimator=self.estimator,
                param_grid=self.parameters,
                n_jobs=_n_jobs,
                cv=self.SSS,
                scoring=self.score,
                error_score=np.nan,
                return_train_score=True,
                refit=True
            )
            self.log += HyperparamOptimal.logRecord('info','GSCV hyperparameter optimization......\n')
        elif self.arg.SearchCV == 'RSCV':
            clf = RandomizedSearchCV(
                estimator=self.estimator,
                param_grid=self.parameters,
                n_jobs=_n_jobs,
                cv=self.SSS,
                n_iter=self.arg.n_iter,
                scoring=self.score,
                return_train_score=True,
                refit=True,
                error_score='raise'
            )
            self.log += HyperparamOptimal.logRecord('info','RSCV hyperparameter optimization......\n')
        # fit
        if self.model in ['XGB_']:
            clf.fit(x_train, y_train,
                    #eval_metric=["error", "logloss"],
                    #eval_set=[(X_train, y_train), (X_test, y_test)],
                    eval_set=[(x_test, y_test)],
                    eval_metric='auc',
                    early_stopping_rounds=15,
                    verbose=False)
        else:
            clf.fit(x_train, y_train)
        # print best parameters
        if hasattr(clf, 'best_estimator_'):
            self.log += HyperparamOptimal.logRecord('info','%s best parameters in %s: \n%s\n', self.model, self.arg.SearchCV, clf.best_estimator_.get_params())
            self.clf = clf.best_estimator_
        else:
            self.log += HyperparamOptimal.logRecord('info','%s best parameters: \n%s\n', self.model, clf.get_params())
            self.clf = clf
    
    # obj: refitting the models by the entire train data
    @staticmethod
    def re_fit(clf, x_matrix, y_matrix, model, log):
        new_clf = clf.fit(x_matrix, y_matrix)
        log += HyperparamOptimal.logRecord('info', '%s model has been refitted by input train data.\n', model)
        return new_clf
    
    @staticmethod
    def logRecord(*args):
        if args[0] == 'info':
            return '[%s] [INFO]: ' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + args[1] % args[2:]
        elif args[0] == 'warning':
            return '[%s] [WARNING]: ' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + args[1] % args[2:]

    @staticmethod
    def CalibratedClassifierCV(clf, CV, method, x_matrix, y_matrix):
        clf_C = CalibratedClassifierCV(clf, cv=CV, method=method)
        clf_C.fit(x_matrix, y_matrix)
        return clf_C

    @staticmethod
    def MergeTrainTest(train, test):
        try:
            allData = pd.concat((train, test), axis=0)
        except TypeError:
            allData = vstack((train, test))
        return allData

    @staticmethod
    def GetPredict(clf, x_matrix, mclass, log):
        predict = clf.predict(x_matrix)
        try:
            proba = clf.predict_proba(x_matrix)
        except AttributeError:
            proba = clf._predict_proba_lr(x_matrix)
            log += HyperparamOptimal.logRecord('warning','Note: LinearSVC, SGB use _predict_proba_lr based on decision_function as predict_proba in GridsearchCV.\n')
        except:
            proba = _predict_proba_lr(clf.decision_function(x_matrix))
            log += HyperparamOptimal.logRecord('warning','Note: predict_proba use sigmoid transversion based on decision_function!\n')

        if (mclass & mclass != proba.shape[1]):
            raise Exception('The columns length of predict probability is wrong!') 
        return np.c_[predict, proba], log

    @staticmethod
    def GetCoef(model, clf, mclass, log, index=None):
        if model in ['MNB','BNB'] :
            importances= np.exp(clf.coef_)
            log += HyperparamOptimal.logRecord('warning','Note: Use coef_ exp values as the feature importance of the estimator %s.\n', model)
        elif model in ['CNB'] :
            if mclass ==2:
                importances= np.exp(-clf.feature_log_prob_)[1]
            else:
                importances= np.exp(-clf.feature_log_prob_)
            log += HyperparamOptimal.logRecord('warning','Note: Use feature_log_prob_ negative exp values as the feature importance of the estimator %s.\n', model)
        elif model in ['GNB'] :
            if mclass ==2:
                importances= clf.theta_[1]
            else:
                importances= clf.theta_
            log += HyperparamOptimal.logRecord('warning','Note: Use theta_ values as the feature importance of the estimator %s.\n', model)
        elif model in ['MLP'] :
            def collapse(coefs):
                Coefs = coefs[0]
                for b in coefs[1:]:
                    Coefs = Coefs.dot(b)
                return(Coefs/Coefs.sum(0))
            importances = collapse(clf.coefs_).T
            log += HyperparamOptimal.logRecord('warning','Note: Use coefs_ weighted average as the feature importance of the estimator %s.\n', model)
        elif model in ['SVM', 'SVMrbf', 'nuSVMrbf']:
            dot_coef_ = clf.dual_coef_.dot( clf.support_vectors_ )
            importances = (1-np.exp(-dot_coef_)) / (1+np.exp(-dot_coef_))
            log += HyperparamOptimal.logRecord('warning','Note: Use exp dot of support_vectors_ and dual_coef_ values as the feature importance of the estimator %s.\n', model)
        else:
            for i in ['feature_importances_', 'coef_']:
                try:
                    importances= eval('clf.%s'%i)
                    log += HyperparamOptimal.logRecord('warning','Note: Use %s as the feature importance of the estimator %s.\n', i, model)
                    break
                except AttributeError:
                    importances = []
                    log += HyperparamOptimal.logRecord('warning','Note: Cannot find the feature importance attributes of estimator %s.\n', i)
        df_import = pd.DataFrame(np.array(importances).T)
        if not df_import.empty :
            df_import.index= index
            df_import = df_import[(df_import != 0).any(1)]
        log += HyperparamOptimal.logRecord('info', '%s Feature coefficiency: \n%s\n', model, df_import)
        return df_import, log

    @staticmethod
    def OneHot(model, clf, x_matrix, OHE='N'):
        if model in ['GBDT']:
            x_trans = clf.apply(x_matrix)[:,:,0]
        elif model in ['XGB', 'RF']:
            x_trans = clf.apply(x_matrix)
        if OHE == 'N':
            OHE = OneHotEncoder(categories='auto')
            OHE.fit(x_trans)
        x_trans = OHE.transform(x_trans.astype(np.int32))
        return [x_trans, OHE]

    @staticmethod            
    def GetEvalu_C(y_true, y_predict, y_score, name=None):
        y_trueb = Check_Binar(y_true)

        Model_ = pd.Series({  
                    'Accuracy'  : accuracy_score(y_true, y_predict),
                    'Accuracy_B': balanced_accuracy_score(y_true, y_predict),
                    'F1_score'  : f1_score(y_true, y_predict),
                    'Precision' : precision_score(y_true, y_predict),
                    'Recall'    : recall_score(y_true, y_predict),
        })

        Model_['Roc_auc'] = round(roc_auc_score(y_trueb, y_score), 6)
        Model_['Precision_A'] = round(average_precision_score( y_trueb, y_score), 6)
        if y_score.shape[1] > 2:
            for i in range(y_score.shape[1]):
                Model_['Roc_auc_' + str(i)] = round(roc_auc_score(y_trueb[:,i], y_score[:, i]), 6)
                Model_['Precision_A_' + str(i)] = round(average_precision_score( y_trueb[:, i], y_score[:, i]), 6)

        Model_.name = name
        return Model_.sort_index()
    
    @staticmethod
    def GetScore(df, label=None):
        _m = [re.sub('^Pred','', _i) for _i in df.columns if re.match('Pred', _i)]
        return pd.concat([HyperparamOptimal.GetEvalu_C(df['TRUE'],
                                                       df['Pred'+_j],
                                                       df[sorted([_n for _n in df.columns if re.search('Prob'+_j, _n)])],
                                                       name= label + _j) for _j in _m], axis=1)
                                                 
    def getModelResult(self, x_matrix='N'):
        if x_matrix=='N':
            self.x = HyperparamOptimal.MergeTrainTest(train=self.x_train, test=self.x_test)
        else:
            self.x = x_matrix
        self.y = HyperparamOptimal.MergeTrainTest(train=self.y_train, test=self.y_test)
        self.new_clf = HyperparamOptimal.re_fit(clf=self.clf, x_matrix=self.x, y_matrix=self.y, model=self.model, log=self.log)
        self.clf_C = HyperparamOptimal.CalibratedClassifierCV(clf=self.new_clf, CV=self.SSS, method=self.arg.calibme, x_matrix=self.x, y_matrix=self.y)
        predict_G, self.log = HyperparamOptimal.GetPredict(clf=self.new_clf, x_matrix=self.x, mclass=self.MClass, log=self.log)
        predict_C, self.log = HyperparamOptimal.GetPredict(clf=self.clf_C, x_matrix=self.x, mclass=self.MClass, log=self.log)
        predict = pd.DataFrame(np.c_[self.y, predict_G, predict_C], index=self.y.index)
        predict.columns = ['TRUE', 'Pred_%s'%self.model] + ['%s_Prob_%s'%(x, self.model) for x in range(self.MClass)] + \
                            ['Pred_C_%s'%self.model] + ['%s_Prob_C_%s'%(x, self.model) for x in range(self.MClass)]
        coef, self.log = HyperparamOptimal.GetCoef(model=self.model, clf=self.new_clf, mclass=self.MClass, log=self.log, index=self.x.columns)
        Best_MD = [{'model':self.model, 'clf':self.new_clf, 'features':self.x.columns.tolist()},
                   {'model':'C_'+self.model, 'clf':self.clf_C, 'features':self.x.columns.tolist()}]
        return(predict, coef, Best_MD)

    # obj: predict the testing dataset by 13 models
    def Predicting_C(self, best_model, pDFall, y_name):
        Y_TRUE  = pDFall[y_name].to_frame(name='TRUE')
        Y_PRED , Y_Eval = [], []
        for _k, _cv in enumerate(best_model):
            y_pred = [Y_TRUE]
            for _i, _m in enumerate(_cv):
                model = _m['model']
                clf = _m['clf']
                model_x_names = _m['features']
                x_pred = pDFall[model_x_names]
                if 'leaf' in _m.keys():
                    leaf = _m['leaf']
                    x_pred, OHE = HyperparamOptimal.OneHot(self.model, _cv[0]['clf'], x_pred, leaf)
                log = ''
                _prepro, log = HyperparamOptimal.GetPredict(clf, x_pred, self.MClass, log)
                self.log.NIF(log)
                _prepro = pd.DataFrame(_prepro,
                                       index=pDFall.index,
                                       columns = ['Pred_%s' % model] + ['%s_Prob_%s'%(x, model) for x in range(self.MClass)]
                                       )
                y_pred.append(_prepro)
            y_pred  = pd.concat(y_pred, axis=1)
            y_predv = y_pred[~y_pred['TRUE'].isna()]
            self.log.CIF(('%s %s Model Predicting Parameters'% (y_name, self.model)).center(45, '-'))
            if y_predv.shape[0] > 2:
                Pred_Mel = HyperparamOptimal.GetScore(df=y_predv, label='Predict')
                self.log.CIF("%s Modeling evaluation: \n%s" % (self.model, Pred_Mel))
            else:
                Pred_Mel = pd.DataFrame()
            self.log.CIF(('Completed %2d%%'% ((_k+1)*100/len(best_model))).center(45, '-'))
            Y_PRED.append(y_pred)
            Y_Eval.append(Pred_Mel)
        return(Y_PRED, Y_Eval)


class MergeAllResult():
    '''
    combined and integrated predicted values of 13 models.
    '''
    def __init__(self, log):
        self.log = log
        
    @staticmethod
    def revisedPred(All_Pb, All_Pred):
        _m = All_Pb.columns.str.replace('.*_Prob','Prob',regex=True).drop_duplicates(keep='first')
        for _x in _m:
            All_Pred[_x.replace('Prob','Pred')] = All_Pb.filter(regex=_x, axis=1).values.argmax(1)
        return All_Pred
    
    @staticmethod
    def calculate_MAD(predict):
        '''
        calculate MAD for each sample 13 models' predict value, the central point is median of 13 predict values.
        '''
        predict =list(predict)
        predict.sort()
        half_len = len(predict) // 2
        predict_median = (predict[half_len] + predict[~half_len])/2
        num = 0
        for i in predict:
            num += abs(i - predict_median)
        return num / len(predict)
    
    @staticmethod
    def mad_df(df):
        '''
        calculate MAD for dataframe by self-defining function calculate_MAD
        '''
        return df.apply(MergeAllResult.calculate_MAD)

    def CVMerge(self, predict, label='Test'):
        allTest = pd.concat(predict, axis=0)
        _model = [re.sub('^Pred_','', i) for i in allTest.columns if re.match('Pred_.*', i)]
        All_Prob_mean = allTest.filter(regex=("_Prob_")).groupby([allTest.index]).mean()
        All_Prob_mean.columns +=  '_mean'
        All_Prob_median = allTest.filter(regex=("_Prob_")).groupby([allTest.index]).median()
        All_Prob_median.columns += '_median'
        All_Prob_mad = allTest.filter(regex=("_Prob_")).groupby([allTest.index]).apply(MergeAllResult.mad_df)
        All_Prob_mad.columns += '_mad'
        All_Pred =  allTest.filter(regex=("^TRUE|^Pred_")).groupby([allTest.index]).apply(lambda x : x.mode(0).loc[0,:])
        All_Pred.columns = [ i + '_mode' if i !='TRUE' else i for i in All_Pred.columns ]
        All_Pred = MergeAllResult.revisedPred(All_Prob_mean, All_Pred)
        All_Pred = MergeAllResult.revisedPred(All_Prob_median, All_Pred)
        ALL_Result  = pd.concat([All_Pred, All_Prob_mean, All_Prob_median, All_Prob_mad], axis=1)
        ALL_Resultv = ALL_Result[~ ALL_Result['TRUE'].isna()]
        if ALL_Resultv.shape[0] > 2:
            EvalueA = HyperparamOptimal.GetScore(ALL_Resultv.filter(regex='^TRUE|_mean$', axis=1), label=label)
            self.log.CIF("The final mean evaluation: \n%s" % EvalueA)
        else:
            EvalueA = pd.DataFrame([])
        self.log.CIF(('Finish %s'% label).center(45, '-'))
        self.allTest = allTest
        self.ALL_Result = ALL_Result
        self.EvalueA = EvalueA
    
    def FeatCoeffs(self, All_import):
        if All_import:
            All_import = pd.concat(All_import, axis=1, sort=False).fillna(0)
            column = sorted(set(All_import.columns))
            All_import = All_import[column]
            for i in column:
                All_import['%s_mean'%i]  = All_import[i].mean(axis=1)
                All_import['%s_std'%i]   = All_import[i].std(axis=1)
                All_import['%s_median'%i]= All_import[i].median(axis=1)
            All_import.sort_values(by=['%s_mean'%i for i in column], ascending=[False]*len(column), inplace=True, axis=0)
            self.All_import = All_import
        else:
            self.All_import = pd.DataFrame([])
    
    def ModelScore(self, All_evluat):
        if All_evluat:
            All_pvalues = pd.concat(All_evluat,  axis=0)
            self.All_pvalues = All_pvalues
    
 
### define some functions
def modeling(arg, x_train, x_test, y_train, y_test, Typi, mclass, _k, _n, allGroup):
    log = ''
    hyper = HyperparamOptimal(arg, log, model=arg.model, y_variable_type=Typi, y_variable_class=mclass)
    hyper.Hyperparemet(x_train, x_test, y_train, y_test)
    predict, coef, Best_MD = hyper.getModelResult()
    Openf('%s%s_Class_%s_predict.xls'%(arg.output, 'Group', str(_n)), (predict), index=True, index_label='sample').openv()
    logText = hyper.log
    # addmodel
    if (arg.model in ['GBDT', 'XGB', 'RF']) and (arg.Addmode !='N'):
        log_add = ''
        x_train_add, OHE = HyperparamOptimal.OneHot(model=arg.model, clf=hyper.clf, x_matrix=x_train)
        x_test_add,  OHE = HyperparamOptimal.OneHot(model=arg.model, clf=hyper.clf, x_matrix=x_test, OHE=OHE)
        x_matrix_add, OHE_merge = HyperparamOptimal.OneHot(model=arg.model, clf=hyper.new_clf, x_matrix=hyper.x)
        hyper_add = HyperparamOptimal(arg, log_add, model=arg.Addmode, y_variable_type=Typi, y_variable_class=mclass)
        hyper_add.Hyperparemet(x_train_add, x_test_add, y_train, y_test)
        predict_add, coef_add, Best_MD_add = hyper_add.getModelResult(x_matrix=x_matrix_add)
        predict = pd.concat([predict, predict_add], axis=1)
        Best_MD_add[0].update({'leaf':OHE_merge})
        Best_MD_add[1].update({'leaf':OHE_merge})
        Best_MD += Best_MD_add
    # statistic    
    if len(y_test)>2 and mclass<=2:
        score = HyperparamOptimal.GetScore(predict.loc[y_train.index], label='Train')
    else:
        score = pd.DataFrame()
    logText += HyperparamOptimal.logRecord('info', '%s Modeling evaluation: \n%s\n', arg.model, score)
    logText += HyperparamOptimal.logRecord('info', ('Modeling has been Completed %2d%%%%' % ((_k+1)*(_n+1)*100/(arg.Repeatime*allGroup))).center(45, '-'))
    logText += "\n"
    return(predict, coef, score, Best_MD, logText)

def run_fitting(args, Log):
    ### set fitting output directory
    args.output = '%s/01ModelFit/%s' % (args.outdir, args.header)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.MODELF), exist_ok=True)

    ### load data
    (group, RYa, CYa, Xa, Xg) = OpenM(args, Log).openg()
    YType = group[(group.Variables.isin(RYa + CYa))][['Variables', 'Type']]
    for Yi, Typi in YType.values:
        DFall = Openf(args.input, index_col=0).openb()
        Xi    = list(set(DFall.columns) - set([Yi]))
        Xi.sort(key=DFall.columns.to_list().index)
        Log.CIF(('%s: Supervised MODELing' % Yi).center(45, '*') )
        Log.NIF('%s Value Counts:\n%s' % (Yi, DFall[Yi].value_counts().to_string())) 
        DFall[Yi] = Check_Label(DFall[Yi])
        # sample was splited into 13 groups
        sample_split = sampleSplit(args)
        sample_group_index = sample_split.CVSplit(Xdf=DFall[Xi], Ydf=DFall[Yi])
        # hyperparameter optimization (use the first set of data)
        allPredict, allCoef, allScore, allMD = [], [], [], []
        threads = []
        for repeat in range(args.Repeatime):
            for i in range(len(sample_group_index)):
                train_index, test_index = sample_group_index[i]
                train , test = DFall.iloc[train_index, :], DFall.iloc[test_index, :]
                x_train, y_train = train[Xi], train[Yi]
                x_test , y_test  = test[Xi], test[Yi]
            #    t = MyThread(modeling, (args, x_train, x_test, y_train, y_test, Typi, DFall[Yi].nunique(), repeat, i, len(sample_group_index)))
            #    threads.append(t)
            #for i in range(len(sample_group_index)):
            #    threads[i].setDaemon(True)
            #    threads[i].start()
            #for i in range(len(sample_group_index)):
            #    threads[i].join()
            #for i in range(len(sample_group_index)):
            #    full_predict, coef, score, MD, logText = threads[i].get_result()
                full_predict, coef, score, MD, logText = modeling(args, x_train, x_test, y_train, y_test, Typi, DFall[Yi].nunique(), repeat, i, len(sample_group_index))
                allPredict.append(full_predict)
                allMD.append(MD)
                if not coef.empty:
                    allCoef.append(coef)
                if not score.empty:
                    allScore.append(score)
                Log.NIF(logText)
            Log.CIF('Modeling has been Completed'.center(45, '-'))
        Log.CIF(('%s: Supervised MODELing Finish'%Yi).center(45, '*'))
        # merge all test predict
        matp = MergeAllResult(Log)
        matp.CVMerge(allPredict, label='Train')
        matp.FeatCoeffs(allCoef)
        matp.ModelScore(allScore)
        Openf('%s%s_Class_%s_detials.xls'%(args.output, Yi, 'Train'), (matp.allTest), index=True, index_label='sample').openv()
        Openf('%s%s_Class_%s_summary.xls'%(args.output, Yi, 'Train'), (matp.ALL_Result), index=True, index_label='sample').openv()
        Openf('%s%s_Class_%s_summary_statistics.xls'%(args.output, Yi, 'Train'), (matp.EvalueA), index=True, index_label='Score').openv()
        Openf('%s%s_Class_features_importance.xls' %(args.output, Yi), (matp.All_import)).openv()
        Openf('%s%s_Class_%s_metrics_pvalues.xls'%(args.output, Yi, 'Train'), (matp.All_pvalues), index=True, index_label='Score').openv()
        joblib.dump(DFall[Xi+[Yi]], '%s%s_Class_traintest_set.pkl' %(args.MODELF, Yi), compress=1)
        joblib.dump(allMD , '%s%s_Class_best_estimator_1.pkl' %(args.MODELF, Yi), compress=1)
    Log.CIF(('%s: Supervised MODELing Finish' % Yi).center(45, '*'))
   
if __name__ == "__main__":
    from MLLogging import Logger
    from MLArguments import Args
    args = Args()
    args.commands = "Fitting"
    args.input = "../Data/fragment.stat_Methy.Ratio.PCA_0.95.discovery.PCA.txt"
    args.group = "../Data/fragment.stat_Methy.Ratio.PCA_0.95.group.Info.PCA.txt"
    args.outdir = "../Test"
    args.model = "LinearSVM"
    args.Addmode = "N"
    args.Repeatime = 1
    args.CVfit = 'SSA'
    args.crossV = 10
    args.testS = 0.3
    args.GStestS = 0.3
    args.random = 123456
    args.leavP = 1
    args.calibme = 'sigmoid'
    args.n_job = 5
    args.SearchCV = 'GSCV'
    args.header = '/%s_' % (args.model)
    args.outdir = '%s/%s/' % (args.outdir, args.model)
    args.output = '%s%s'%(args.outdir, args.header)
    args.MODELF = '%s/00MODEL/%s' % (args.outdir, args.header)
    os.makedirs(os.path.dirname(args.outdir), exist_ok=True)
    os.makedirs(os.path.dirname(args.MODELF), exist_ok=True)
    # print output message and create new folder for modeling results
    Log = Logger( '%s%s_log.log'%(args.output, args.commands) )
    Log.NIF("The argument you have set as follows:".center(59, '*'))
    for i,k in enumerate(vars(args),start=1):
        Log.NIF('**%s|%-13s: %s'%(str(i).zfill(2), k, str(getattr(args, k))) )
    Log.NIF(59 * '*')

    run_fitting(args, Log)