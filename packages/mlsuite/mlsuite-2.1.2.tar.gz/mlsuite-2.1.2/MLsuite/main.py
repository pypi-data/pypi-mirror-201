#===================================================
#
# Project      :mlsuite building models or predicting
# Description  : main script
# Usage        : 
# Author       : Suxing Li
# Email        : li.suxing@genecast.com.cn
# Created at   : 2022-06-21
#
#====================================================


import traceback
import os,sys
import time
from .MLPipeline import Pipeline
from .MLLogging import Logger
from .MLArguments import Args


def Commands():
    info = '''
    #===================================================
    #
    # Project      : mlsuite building models or predicting
    # Description  : main script
    # Usage        : 
    # Author       : Suxing Li
    # Email        : li.suxing@genecast.com.cn
    # Created at   : 2022-06-21
    #
    #====================================================
    '''
    
    args = Args()
    args.header = '/%s_' % (args.model)
    args.outdir = '%s/%s/' % (args.outdir, args.model)
    args.output = '%s%s' % (args.outdir, args.header)
    args.MODELF = '%s/00MODEL/%s' % (args.outdir, args.header)
    Theader = time.strftime("%Y%m%d%H%M", time.localtime())
    if args.commands=='Predict' :
        if ( bool(args.out_predict) | bool(args.modelpath) ):
            args.outdir = '%s/%s/' % (args.modelpath, args.model)
            args.output = '%s/%s_Prediction_%s/%s' % (args.out_predict, args.out_header, Theader, args.header)
            args.MODELF = '%s/00MODEL/%s' % (args.outdir, args.header)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    Log = Logger( '%s%s_log.log'%(args.output, args.commands) )
    Log.NIF(info.strip())
    Log.NIF("The argument you have set as follows:".center(59, '*'))
    for i,k in enumerate(vars(args),start=1):
        Log.NIF('**%s|%-13s: %s'%(str(i).zfill(2), k, str(getattr(args, k))) )
    Log.NIF(59 * '*')

    return_code = 0
    try:
        Pipeline(args, Log).Pipe()
        Log.CIF('Success!!!')
    except Exception:
        traceback.print_exc()
        return_code = 1
    finally:
        Log.CIF('You can check your progress in log file.')
        exit(return_code)

