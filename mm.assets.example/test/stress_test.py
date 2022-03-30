import os, sys
import traceback
import requests
import csv
import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from datetime import  datetime

pool = ThreadPoolExecutor(8)
futures = []



def get_row(row, key):
    if key in row:
        return row[key]
    return None


RETRY_CNT = 3

mm_server_host = "https://mm-stage.lgebigdata.com/mmserver"
# mm_server_host = "http://127.0.0.1:5011"
# mm_server_host = "https://mm-internal.intellytics.biz/mmserver"


def post(**kwargv):
    host = mm_server_host
    url = os.path.join(host, "update/models")

    retry = RETRY_CNT
    while retry >= 0:
        try:
            r = requests.post(url, json=kwargv, timeout=300)
            # print(r)
            if r.status_code >= 500:
                print('r.status_code : %d' % r.status_code)
                raise Exception
        except requests.Timeout:
            retry = retry - 1
            time.sleep(RETRY_CNT - retry)
            print('post - Timeout Exception : %s' % traceback.format_exc())
        except requests.ConnectionError:
            retry = retry - 1
            time.sleep(RETRY_CNT - retry)
            print('post - ConnectionError : %s' % traceback.format_exc())
        except Exception as e:
            retry = retry - 1
            time.sleep(RETRY_CNT - retry)
            print('post - Exception : %s' % traceback.format_exc())
        else:
            break

    return r


home = '/mm/project'
workflow_home = 'workflows/scmdf-ai-stage.thd-ref-selectmodel.87'
step = "scores"
target_path = ''
seq = os.environ.get('seq', '0')
args = '{"order_1":1,"order_2":0,"order_3":0,"lambda":0,"featureset":["MA5W","nor_qty"],"featuresetbase":["MA3W"],' \
       '"Event":["Indy","BF","Labor","Mem"],"Promo_index_name":["Indy","BF"],"rounding":0.5,' \
       '"tscleanMA":0,"fcst_weeks":26}'
model = 'ARIMA_united'
model_plan_def_id = 10000

path = os.path.join(os.path.dirname(__file__), 'score.csv')

for i in range(1, 9):
    model_info = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmp = {}
            target = get_row(row, 'target')
            score = get_row(row, 'score')
            if (not score) or (score.lower() == "nan") or (score.lower() == "na"):
                score = None

            tmp['target'] = target
            tmp['args'] = args
            tmp['path'] = '/mm/project/workflows/scmdf-ai-stage.thd-ref-selectmodel.87/scores/product=REF_store=THD_dc=NL/17/score.csv'
            tmp['score'] = score
            tmp['model'] = model
            tmp['seq'] = i
            model_info.append(tmp)

        print('%s : %s' % (i, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        # post(mm_server_host=mm_server_host, \
        #     project_id=39, workflow_def_id=70, \
        #     workflow_id=52714, step_id=131436, model_plan_def_id=3, model_info=model_info)


        # futures.append(pool.submit(post, mm_server_host=mm_server_host, \
        #     project_id=15, workflow_def_id=19, \
        #     workflow_id=53728, step_id=142816, model_plan_def_id=None, model_info=model_info))

        # mm-stage
        futures.append(pool.submit(post, mm_server_host=mm_server_host, \
            project_id=178, workflow_def_id=144, \
            workflow_id=31490, step_id=33060, model_plan_def_id=100, model_info=model_info))


    # if i%8 == 0:
    #     print('submitted i=%s' % i)
    #     time.sleep(10)

for x in as_completed(futures):
    print('%s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print(x.result())