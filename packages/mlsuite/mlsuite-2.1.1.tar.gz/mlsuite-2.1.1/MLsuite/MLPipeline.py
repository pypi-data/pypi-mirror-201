#===================================================
#
# Project      : mlsuite building models or predicting
# Description  : pipeline script
# Usage        : 
# Author       : Suxing Li
# Email        : li.suxing@genecast.com.cn
# Created at   : 2022-06-14
#
#====================================================


from .MLSupervising import run_fitting
from .MLPredicting import run_predict

class Pipeline():
    'The pipeline used for machine learning models'
    def __init__(self, arg, log,  *array, **dicts):
        self.arg = arg
        self.log = log
        self.array  = array
        self.dicts  = dicts

    def Pipe(self):

        if self.arg.commands in ['Fitting', 'Auto']:
            run_fitting(self.arg, self.log)

        if self.arg.commands in ['Predict', 'Auto']:
            run_predict(self.arg, self.log)
