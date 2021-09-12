import os

companies = ["HAS","ADSK","BWA","CAH","CE","CHTR","FANG","XLNX"]
companies = ['ADSK','CHTR']
param_param= {'DeepAR':['mu','sigma','nu'],'DeepVAR':['mu','sigma'],'GPVAR':['mu','sigma']}

freq_param = {'Daily':{'tl':[1150],'vl':[1190],'ttl':[1290]},
              'Hourly':{'tl':[2400],'vl':[2550],'ttl':[2750]},}
path_bit = '_FC22_WHILE_test_correct_num'
frequencies = ['Daily']
model_ = 'DeepAR'
freq_ = 'Daily'
train_length = freq_param[freq_]['tl']
validation_length = freq_param[freq_]['vl']
test_length = freq_param[freq_]['ttl']
prediction_length  = [5]
epoch = [30,70]
d= companies
batch_size = [50,100]
nbpe = [300,100]
seed = [6]
adv_dir = [1,-1]
epsilon  =[0.05]
frac_amount= [0.3,0.7]
adv_ex_list= ['simple','complex']
parameter = param_param[model_]

os.system(f"python WHILE_submit_jobs.py --bit {path_bit} --models {model_} --frequencies {freq_} --companies \"{' '.join(d)}\" "
                f"--train_length \"{' '.join([str(c) for c in train_length])}\" --validation_length \"{' '.join([str(c) for c in validation_length])}\" "
                f"--test_length \"{' '.join([str(c) for c in test_length])}\" --prediction_length \"{' '.join([str(c) for c in prediction_length])}\" "
                f"--epochs \"{' '.join([str(c) for c in epoch])}\" --batch_size \"{' '.join([str(c) for c in batch_size])}\" "
                f"--nbpe \"{' '.join([str(c) for c in nbpe])}\" --seed \"{' '.join([str(c) for c in seed])}\" "
                f"--adv_dir \"{' '.join([str(c) for c in adv_dir])}\" --epsilon \"{' '.join([str(c) for c in epsilon])}\" "
                f"--frac_amount \"{' '.join([str(c) for c in frac_amount])}\" --adv_example_type \"{' '.join(adv_ex_list)}\" --parameter \"{' '.join(parameter)}\"")

