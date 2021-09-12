import os

companies = ["HAS","ADSK","BWA","CAH","CE","CHTR","FANG","XLNX"]
companies = ['ADSK']
adv_ex_list = ['simple']
seed = [6]
adv_dir = [1,-1]
epsilon = [0.01]
max_iter = [50]
param_param= {'DeepAR':['mu','sigma','nu'],'DeepVAR':['mu','sigma'],'GPVAR':['mu','sigma']}

freq_param = {'Daily':{'tl':[1150],'vl':[1190],'ttl':[1290]},
              'Hourly':{'tl':[2400],'vl':[2550],'ttl':[2750]},}
path_bit = 'vtest_run'
models = ['DeepAR']
frequencies = ['Daily']
#frequencies = ['Hourly']
special_dict = {('ADSK', 'Daily', 'DeepAR'): (300, 300, 150, 0.01, 1, 5), ('ADSK', 'Daily', 'DeepVAR'): (200, 200, 150, 0.01, 1, 5), ('ADSK', 'Hourly', 'DeepAR'): (300, 300, 150, 0.01, 1, 3), ('ADSK', 'Hourly', 'DeepVAR'): (30, 200, 20, 0.01, 1, 5), ('BWA', 'Daily', 'DeepAR'): (400, 300, 150, 0.01, 1, 5), ('BWA', 'Daily', 'DeepVAR'): (200, 100, 150, 0.01, 1, 5), ('BWA', 'Hourly', 'DeepAR'): (200, 300, 150, 0.01, 1, 5), ('BWA', 'Hourly', 'DeepVAR'): (30, 50, 20, 0.01, 1, 5), ('CAH', 'Daily', 'DeepAR'): (100, 100, 30, 0.01, 100, 5), ('CAH', 'Daily', 'DeepVAR'): (30, 200, 20, 0.01, 1, 5), ('CAH', 'Hourly', 'DeepAR'): (30, 50, 100, 0.01, 1, 5), ('CAH', 'Hourly', 'DeepVAR'): (30, 50, 20, 0.01, 1, 5), ('CE', 'Daily', 'DeepAR'): (100, 200, 100, 0.01, 100, 5), ('CE', 'Daily', 'DeepVAR'): (40, 40, 60, 0.03, 50, 5), ('CE', 'Hourly', 'DeepAR'): (30, 50, 20, 0.01, 1, 5), ('CE', 'Hourly', 'DeepVAR'): (200, 100, 200, 0.01, 1, 3), ('CHTR', 'Daily', 'DeepAR'): (400, 300, 150, 0.01, 1, 5), ('CHTR', 'Daily', 'DeepVAR'): (80, 80, 25, 0.01, 150, 5), ('CHTR', 'Hourly', 'DeepAR'): (200, 100, 150, 0.01, 1, 3), ('CHTR', 'Hourly', 'DeepVAR'): (40, 40, 60, 0.03, 50, 5), ('HAS', 'Daily', 'DeepAR'): (300, 200, 150, 0.01, 1, 3), ('HAS', 'Daily', 'DeepVAR'): (30, 50, 20, 0.01, 1, 5), ('HAS', 'Hourly', 'DeepAR'): (30, 200, 20, 0.01, 1, 5), ('HAS', 'Hourly', 'DeepVAR'): (200, 100, 150, 0.01, 1, 3), ('FANG', 'Daily', 'DeepAR'): (75, 200, 100, 0.01, 1, 5), ('FANG', 'Daily', 'DeepVAR'): (80, 80, 25, 0.01, 150, 5), ('FANG', 'Hourly', 'DeepAR'): (400, 300, 150, 0.01, 1, 3), ('FANG', 'Hourly', 'DeepVAR'): (200, 100, 150, 0.01, 1, 3), ('XLNX', 'Daily', 'DeepAR'): (30, 50, 20, 0.01, 1, 5), ('XLNX', 'Daily', 'DeepVAR'): (100, 100, 30, 0.01, 100, 5), ('XLNX', 'Hourly', 'DeepAR'): (30, 50, 20, 0.01, 1, 5), ('XLNX', 'Hourly', 'DeepVAR'): (200, 200, 150, 0.01, 1, 3)}

for dataset in companies:
    for freq_ in frequencies:
        for model_ in models:
            print(f'{dataset} {freq_} {model_}')
            args = special_dict[(dataset,freq_,model_)]
            batch_size = [args[0]]
            nbpe = [args[1]]
            epoch = [args[2]]
            d=[dataset]
            prediction_length =[args[-1]]
            train_length = freq_param[freq_]['tl']
            validation_length = freq_param[freq_]['vl']
            test_length = freq_param[freq_]['ttl']
            parameter = param_param[model_]
            os.system(
                f"python submit_jobs.py --bit {path_bit} --models {model_} --frequencies {freq_} --companies \"{' '.join(d)}\" "
                f"--train_length \"{' '.join([str(c) for c in train_length])}\" --validation_length \"{' '.join([str(c) for c in validation_length])}\" "
                f"--test_length \"{' '.join([str(c) for c in test_length])}\" --prediction_length \"{' '.join([str(c) for c in prediction_length])}\" "
                f"--epochs \"{' '.join([str(c) for c in epoch])}\" --batch_size \"{' '.join([str(c) for c in batch_size])}\" "
                f"--nbpe \"{' '.join([str(c) for c in nbpe])}\" --seed \"{' '.join([str(c) for c in seed])}\" "
                f"--adv_dir \"{' '.join([str(c) for c in adv_dir])}\" --epsilon \"{' '.join([str(c) for c in epsilon])}\" "
                f"--max_iter \"{' '.join([str(c) for c in max_iter])}\" --adv_example_type \"{' '.join(adv_ex_list)}\" --parameter \"{' '.join(parameter)}\"")

