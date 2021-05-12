import os
import math
import shutil

baseline = 'predict.files_bl'
baseline_self = 'predict.files_bl_self'
baseline_swish = 'predict.files_bl_swish'
baseline_dev = 'predict.files_add_dev'
result_path = 'predict.files'
if os.path.exists(result_path):
    shutil.rmtree(result_path)
    os.makedirs(result_path)
else:
    os.makedirs(result_path)
num = 0
total_num = 0
baseline_files = os.listdir(baseline)
for baseline_file in baseline_files:
    baseline_list = open(os.path.join(baseline, baseline_file)).readlines()
    baseline_self_list = open(os.path.join(baseline_self, baseline_file)).readlines()
    baseline_swish_list = open(os.path.join(baseline_swish, baseline_file)).readlines()
    baseline_dev_list = open(os.path.join(baseline_dev, baseline_file)).readlines()
    for i, bl_prob in enumerate(baseline_list):
        bl_self_prob = float(baseline_self_list[i])
        bl_swish_prob = float(baseline_swish_list[i])
        bl_dev_prob = float(baseline_dev_list[i])
        err1 = abs(float(bl_prob) - bl_swish_prob) + 0.0001
        err2 = abs(bl_self_prob - bl_swish_prob)
        if err2 / err1 > 10:
            num += 1
        total_num += 1
        merge_prob = 0.3 * float(bl_prob) + 0.2 * bl_self_prob  + 0.05 * bl_swish_prob  + 0.45 * bl_dev_prob
        baseline_list[i] = merge_prob
    result_file = open(os.path.join(result_path, baseline_file), 'w')
    for prob in baseline_list:
        result_file.write(str(prob) + '\n')
    result_file.close()
print(num) 
print(total_num) 
