import pandas as pd
import os

home = os.environ['project_home']
workflow_history_path = os.environ['workflow_history_path']
target_path = os.path.join(workflow_history_path, 'parameter', 'parameter.csv')

df = pd.DataFrame([['basic-train', '', '', ''], ['dynamic-train', 'train', 'LOGISTIC', '1']], columns = ['workflow', 'step', 'target', 'args'])
df.to_csv(target_path, index= False)