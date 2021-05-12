import os
import shutil

test_log = 'test_log.txt'
result_path = 'predict.files/'

if os.path.exists(result_path):
    shutil.rmtree(result_path)
     os.makedirs(result_path)
else:
    os.makedirs(result_path)

with open(test_log, 'r') as f:
    result_list = f.readlines()
for i, result in enumerate(result_list):
    result_infos = result.strip().split()
    result_file = os.path.join(result_path, str(i+1)+'.predict.txt')
    f = open(result_file, 'w')
    for result_info in result_infos:
        f.write(str(result_info)+'\n')
    f.close()
