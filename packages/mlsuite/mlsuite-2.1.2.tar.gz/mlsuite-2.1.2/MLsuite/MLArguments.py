#===================================================
#
# Project      : mlsuite building models or predicting
# Description  : argspase script
# Usage        : 
# Author       : Suxing Li
# Email        : li.suxing@genecast.com.cn
# Created at   : 2022-06-21
#
#====================================================

import argparse
import os

def Args():
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                prefix_chars='-+',
                conflict_handler='resolve',
                description="\nThe traditional machine learning analysis based on sklearn package:\n",
                epilog='''\
Example:
1. python mlsuite.py Auto    -i data.traintest.txt -g group.new.txt -p data.predict.txt -o testdt/ -m DT
2. python mlsuite.py Auto    -i data.traintest.txt -g group.new.txt -o testdt/ -m DT
3. python mlsuite.py Fitting -i data.traintest.txt -g group.new.txt -o testdt/ -m DT
4. python mlsuite.py Predict -p data.predict.txt   -g group.new.txt -x modelpath/ -y predictdt/ -m DT.''')

    parser.add_argument('-V','--version',action ='version',
                version='mlsuite version 2.1.2')
    subparsers = parser.add_subparsers(dest="commands",
                    help='machine learning models help.')
    ### Fitting module
    P_fitting  = subparsers.add_parser('Fitting',conflict_handler='resolve', add_help=False)
    P_fitting.add_argument("-i", "--input",type=str,
                    help='''the input train and test data file with dataframe format  by row(samples) x columns (features and Y). the sample column name must be Sample.
''')
    P_fitting.add_argument("-g", "--group",type=str,required=True,
                    help='''the group file tell the featues, groups and variable type, which has Variables, Group, Type columns. Only continuous and discrete variables are supported in variable type. Onehot variables is coming.''')
    P_fitting.add_argument("-o", "--outdir",type=str,default=os.getcwd(),
                    help="output file dir, default=current dir.")
    P_fitting.add_argument("-m", "--model",type=str, default='LinearSVM',
                    help='''the model you can used for ML.
You can choose the models as follows:
classification:......++++++++++++++++++++++
**RF.................RandomForestClassifier
**GBDT...............GradientBoostingClassifier
**XGB................XGBClassifier(+LR/LRCV)
**MLP................MLPClassifier
**DT.................DecisionTreeClassifier
**AdaB_DT............AdaBoostClassifier(DT)
**LinearSVM..........LinearSVC(penalty='l1')
**LinearSVMil2.......LinearSVC(penalty='l2')
**SVMlinear..........SVC(kernel="linear")
**SVM................SVC(no linear)
**nuSVMrbf...........NuSVC(kernel='rbf')
**SGD................SGDClassifier
**KNN................KNeighborsClassifier
**RNN................RadiusNeighborsClassifier
**MNB................MultinomialNB
**CNB................ComplementNB
**BNB................BernoulliNB
**GNB................GaussianNB
**LR.................LogisticRegression
**LRCV...............LogisticRegressionCV
''')
    P_fitting.add_argument("-am", "--Addmode", type=str, default='LinearSVM',
                    help='''use additional model to adjust modeling in RF, GBDT and XGB estimators. N means no addition.''')
    P_fitting.add_argument("-nt", "--n_iter", type=int, default= 2500,
                    help="Number of parameter settings that are sampled in RSCV. n_iter trades off runtime vs quality of the solution.")
    P_fitting.add_argument("-nj", "--n_job", type=int, default=-1,
                    help="Number of cores to run in parallel while fitting across folds.")
    P_fitting.add_argument("-cm", "--CVfit", type=str, default='SSA',
                    help='''the cross validation model:
**SSA..................StratifiedShuffleSplit() + StratifiedKFold()
**SSS..................StratifiedShuffleSplit()
**SKF..................StratifiedKFold()
**RSKF.................RepeatedStratifiedKFold()
**RKF..................RepeatedKFold()
**LPO..................LeavePOut()
**LOU..................LeaveOneOut()
''')
    P_fitting.add_argument("-rd", "--random",type=int, default=123456,
                    help="the random seeds for cross validation when using StratifiedShuffleSplit.")
    P_fitting.add_argument("-tz", "--testS",type=float, default=0.3,
                    help="the test size for cross validation when using StratifiedShuffleSplit.")
    P_fitting.add_argument("-sc", "--SearchCV",type=str, nargs='?', default='GSCV', choices=['GSCV','RSCV',],
                    help="the hyperparameters optimization method. You also can set it none to discard the method.")
    P_fitting.add_argument("-rt", "--Repeatime", type=int, default=1,
                    help='''the repeat time of modeling. Suggest change to a lagger value with a none value of SearchCV.''')
    P_fitting.add_argument("-cz", "--GStestS",type=float, default=0.3,
                    help="the test size for cross validation when using StratifiedShuffleSplit in gridsearchCV.")
    P_fitting.add_argument("-cv", "--crossV",type=int, default=10,
                    help="the cross validation times when using StratifiedShuffleSplit.")
    P_fitting.add_argument("-lp", "--leavP",type=int, default=1,
                    help="the size of the test sets in Leave-P-Out cross-validator.")
    P_fitting.add_argument("-cc", "--calib", action='store_true', default=True,
                    help='''whether use CalibratedClassifierCV to calibrate probability with isotonic regression or sigmoid.''')
    P_fitting.add_argument("-si", "--calibme", type=str, default='sigmoid', choices=['isotonic','sigmoid'],
                    help="the CalibratedClassifierCV method, you can choose isotonic and sigmoid.")
    P_Fitting  = subparsers.add_parser('Fitting',conflict_handler='resolve',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                    parents=[P_fitting],
                    help='Fitting and predicting the training and testing set from estimators.')
    ### Predict module
    P_predict  = subparsers.add_parser('Predict', conflict_handler='resolve',add_help=False,)
    P_predict.add_argument("-p", "--predict",type=str,
                    help="the predict matrix file.")
    P_predict.add_argument("-x", "--modelpath",type=str,
                    help="the model path used for prediction.")
    P_predict.add_argument("-y", "--out_predict",type=str,
                    help="the predict result file path.")
    P_predict.add_argument("-z", "--out_header",type=str, default='Predict',
                    help="the predict result file header.")
    P_predict.add_argument("-ef", "--refit" , default='fixed',
                    help='''the model used for prediction.
raw: the train set of cross validation in modeling data.
fixed: the train and test set of cross validation in modeling data.
latest: the latest data of modeling data and prediction data.
int number: specified number model used for prediction ''')
    P_Predict  = subparsers.add_parser('Predict',conflict_handler='resolve',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                    parents=[P_fitting, P_predict],
                    help='predict new data from fittting process model.')
    ### Auto module
    P_Autopipe = subparsers.add_parser('Auto', conflict_handler='resolve', prefix_chars='-+',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                    parents=[P_fitting, P_predict],
                    help='the auto-processing for all: Fitting and/or Prediction.')

    args  = parser.parse_args()
    return args
