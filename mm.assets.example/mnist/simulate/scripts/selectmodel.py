import os
import pandas as pd

home = os.environ['project_home']
workflow_home = os.environ['workflow_history_path']
step = "selectmodel"
target_path = os.environ['target_path']
seq = os.environ.get('seq', '0')

MODELS_FILE_PATH = os.path.join(workflow_home, step, 'models.csv')
SELECTMODEL_FILE_PATH = os.path.join(workflow_home, step, 'selectmodel.csv')

df = pd.read_csv(MODELS_FILE_PATH)
df['score'] = df['score']*2
# df = df[0:0]

df.to_csv(SELECTMODEL_FILE_PATH, index=False)
