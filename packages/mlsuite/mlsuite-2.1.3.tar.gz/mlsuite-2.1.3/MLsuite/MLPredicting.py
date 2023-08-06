#===================================================
#
# Project      : mlsuite model prediction
# Description  : predict testing dataset by 13 models
# Usage        : 
# Author       : Suxing Li
# Email        : li.suxing@genecast.com.cn
# Created at   : 2022-06-14
#
#====================================================


import joblib
import os
import re
import glob
import time
from .MLOpenWrite import OpenM, Openf
from .MLSupervising import HyperparamOptimal, MergeAllResult

class Supervised():
    def __init__(self, arg, log, Type='C', MClass=2):
        self.arg = arg
        self.log = log
        self.Type=Type
        self.MClass= MClass

    def GetLatest(self, _Y_name):
        comples = '%s%s_Class_best_estimator_' % (self.arg.MODELF, _Y_name) 
        modelfs = glob.glob(comples + '*.pkl')
        modelnu = sorted([ int(re.search('_best_estimator_(?P<id>\d+).pkl', i ).group('id')) for i in modelfs ])
        if self.arg.refit == 'raw':
            assign = 0
        elif self.arg.refit == 'fixed':
            assign = 1
        elif self.arg.refit == 'latest':
            assign = max(modelnu)
        else:
            assign = int(self.arg.refit)
        return '%s%s.pkl' % (comples, assign)

    def Predict_X(self, DFall, _Y_name):
        Best_Model = joblib.load(self.GetLatest(_Y_name))
        CVRlt = HyperparamOptimal(arg=self.arg, log=self.log, model=self.arg.model, y_variable_type=self.Type, y_variable_class=self.MClass)
        Y_PRED, Y_Eval = CVRlt.Predicting_C(Best_Model, DFall, _Y_name)
        ### All_Pred_predict
        merge_opt = MergeAllResult(log=self.log)
        merge_opt.CVMerge(Y_PRED, label='Predict')
        Openf('%s%s_Class_%s_detials.xls'%(self.arg.output, _Y_name, 'Predict'), (merge_opt.allTest), index=True, index_label='sample').openv()
        Openf('%s%s_Class_%s_summary.xls'%(self.arg.output, _Y_name, 'Predict'), (merge_opt.ALL_Result), index=True, index_label='sample').openv()
        Openf('%s%s_Class_%s_summary_statistics.xls'%(self.arg.output, _Y_name, 'Predict'), (merge_opt.EvalueA), index=True, index_label='Score').openv()
        ### All_evaluate_score_
        merge_opt.ModelScore(Y_Eval)
        Openf('%s%s_Class_%s_metrics_pvalues.xls'%(self.arg.output, _Y_name, 'Predict'), (merge_opt.All_pvalues), index=True, index_label='Score').openv()



def run_predict(args, Log):
    ### set predict output directory
    if not ( bool(args.out_predict) | bool(args.modelpath) ):
        args.output = '%s/02Prediction/%s' % (args.outdir, args.header)
        Log.NIF('')
        Log.NIF('')
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    ### load data
    (group, RYa, CYa, Xa, Xg) = OpenM(args, Log).openg()
    YType = group[(group.Variables.isin(RYa + CYa))][['Variables', 'Type']]
    Predt_set = OpenM(args, Log).openp()
    for Yi,Typi in YType.values:
        Log.CIF(('%s: Supervised Predicting' % Yi).center(45, '*'))
        Supervised(args, Log, Type=Typi, MClass=2).Predict_X(Predt_set, Yi)
        Log.CIF(('%s: Supervised Predicting Finish' % Yi).center(45, '*'))
    Log.CIF('Supervisor Predicting Finish'.center(45, '*'))


if __name__ == "__main__":
    from MLLogging import Logger
    from MLArguments import Args
    args = Args()
    args.commands = "Predict"
    args.group = "../Data/fragment.stat_Methy.Ratio.PCA_0.95.group.Info.PCA.txt"
    args.predict = "../Data/fragment.stat_Methy.Ratio.PCA_0.95.validation.PCA.txt"
    args.modelpath = "../Test"
    args.model = "LinearSVM"
    args.out_predict = "../Test"
    args.out_header = "Predict"
    args.refit = "fixed"
    args.n_job = 5

    # print output message and create new folder for modeling results
    args.header = '/%s_' % (args.model)
    args.outdir = '%s/%s/' % (args.out_predict, args.model)
    args.MODELF = '%s/00MODEL/%s' % (args.outdir, args.header)
    Theader = time.strftime("%Y%m%d%H%M", time.localtime())
    args.output = '%s/%s_Prediction_%s/%s' % (args.outdir, args.out_header, Theader, args.header)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    Log = Logger('%s%s_log.log' % (args.output, args.commands))
    Log.NIF("The argument you have set as follows:".center(59, '*'))
    for i, k in enumerate(vars(args), start=1):
        Log.NIF('**%s|%-13s: %s' % (str(i).zfill(2), k, str(getattr(args, k))))
    Log.NIF(59 * '*')
    Log.CIF( 'Supervisor Predicting'.center(45, '*') )

    run_predict(args, Log)
