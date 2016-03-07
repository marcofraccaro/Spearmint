import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
from spearmint.utils.database.mongodb import MongoDB
from spearmint.main import load_jobs


# Loads database into a (sorted) pandas dataframe
def db_to_df(db_address = 'localhost', db_name= "spearmintDB_marfra", experiment_name = 'rnn_3'):

    db = MongoDB(database_address=db_address,database_name=db_name)

    # Load jobs
    jobs = load_jobs(db, experiment_name)

    # Remove unfinished jobs
    jobs_fin = []
    for job in jobs:
        if job['status'] == 'complete':
            jobs_fin.append(job)


    df=pd.DataFrame()

    for job in jobs_fin:

        # Data from DB to a OrderedDict
        tmp=(("job_id",[job["id"]]),)
        tmp=tmp + (("exp_values",[np.exp(job["values"]['nlp'])]),)
        tmp=tmp + (("values",[job["values"]['nlp']]),)
        for par in job["params"]:
            tmp= tmp + ((par,[job["params"][par]["values"][0]]),)
        tmp=tmp + (("duration_h",[(job["end time"]-job["start time"])/3600.0]),)
        try: # for backward compatibility
            tmp=tmp + (("manual",[job["manual"]]),)
        except:
            pass
        tmp=tmp + (("start_time",[job["start time"]]),)
        tmp=tmp + (("end_time",[job["end time"]]),)

        dict_tmp = OrderedDict(tmp)

        # From OrderedDict to a pandas dataframe
        df_tmp=pd.DataFrame.from_dict(dict_tmp)

        # Append dataframe
        df=df.append(df_tmp, ignore_index=True)

    return df


# Print the head of the (sorted) database
def print_df(df, sorted=""):

    if sorted:
        df=df.sort_values(by=sorted, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')

    cols=range(len(df.columns))
    print df.to_string(columns=cols[:-2],float_format=lambda x: '%.3f' % x)
