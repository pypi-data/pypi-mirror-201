# MLkit

## Install

```
pip install mlsuite==2.1.1
pip install https://github.com/JamesRitchie/scikit-rvm/archive/master.zip
```

## Usage

Notice: used pyhton3, not python2

usage: mlsuite.py [-h] [-V] {Fitting,Predict,Auto} ...

The traditional machine learning analysis based on sklearn package:

positional arguments:
  {Fitting,Predict,Auto}
                        machine learning models help.
    Fitting             Fitting and predicting the training and testing set from estimators.
    Predict             predict new data from fittting process model.
    Auto                the auto-processing for all: Fitting and/or Prediction.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit

Example:

1. python mlsuite.py Auto    -i data.traintest.txt -g group.new.txt -p data.predict.txt -o testdt/ -m DT
2. python mlsuite.py Auto    -i data.traintest.txt -g group.new.txt -o testdt/ -m DT
3. python mlsuite.py Fitting -i data.traintest.txt -g group.new.txt -o testdt/ -m DT
4. python mlsuite.py Predict -p data.predict.txt   -g group.new.txt -x modelpath/ -y predictdt/ -m DT.

## Update log
### v2.1.1
    1. fixed same packages' version:
    ```
    lightgbm == 3.3.3,
    joblib == 1.2.0,
    numpy == 1.23.5,
    pandas == 1.5.2,
    scikit-learn == 1.2.0,
    sklearn_pandas == 2.2.0,
    xgboost == 1.7.2
    ```


### v2.1.0
    1. LinearSVM parameter: LinearSVC(dual=False) report error: "unsupported set of arguments:  The combination of penalty='l2' and loss='hinge' are not supported when dual=False, Parameters: penalty='l2', loss='hinge', dual=False". So go back LinearSVC(dual=True).
    2. modified version information in MLArguments.py.

### v2.0.9

    1. refixed return value of program.

    2. change float data type into integer type.  max_iter parameter in LinearSVM model.

### v2.0.8

    1. modified LinearSVM parameter: LinearSVC(dual=False)

### v2.0.7

    1. repaired same bugs of predict module

### v2.0.6

    1. add RVMrbf and RVMpoly module in MLEstimators.py

### v2.0.2

    1. add SVMpoly module in MLEstimators.py
    2. add calculate MAD function in MLSupervising.py

### v2.0.0

    1. 删除数据预处理、特征筛选、画图等步骤，保留模型构建和模型预测两个步骤。
    2. 13个模型构建，改为并行，缩短分析时间。

### v1.0.0
