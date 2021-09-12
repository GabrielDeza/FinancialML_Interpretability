#!/usr/bin/env python
import time
import os
import itertools
import argparse
parser = argparse.ArgumentParser(description='Main Script to Run one of the jobs')

parser.add_argument('--models', default='DeepAR', type=str, help='List of What Setting (DeepAR, DeepVAR, GPVAR)')
parser.add_argument('--frequencies', default='Daily', type=str, help='List of What Frequency (Daily, Hourly)')
parser.add_argument('--companies', default='CHTR', type=str, help='List of Company')

parser.add_argument('--train_length', default=60, type=str, help='Length of training set')
parser.add_argument('--validation_length', default=70, type=str, help='Length of validation set')
parser.add_argument('--test_length', default=120, type=str, help='Length of testing set')

parser.add_argument('--prediction_length', default=5, type=str, help='Prediction Length')
parser.add_argument('--epochs', default=1, type=str, help='number of epochs')
parser.add_argument('--batch_size', default=32, type=str, help='Batch size')
parser.add_argument('--nbpe', default=30, type=str, help='Number of batches per epoch')

parser.add_argument('--seed', default=6, type=str, help='seed')

parser.add_argument('--adv_dir', default = 1, type= str, help ="Direction of parameter to modify (-1 or +1)")
parser.add_argument('--epsilon', default=0.5, type=str, help='Percent change in dataset at each iteration')
parser.add_argument('--frac_amount', default=0.3, type=str, help='number of iterations on the adv dataset algorithm')
parser.add_argument('--parameter', default='mu', type=str, help='parameter we want to change. its mu sigma nu for student-t',)
parser.add_argument('--adv_example_type', default='mu', type=str, help='parameter we want to change. its mu sigma nu for student-t',)
parser.add_argument('--bit', default='', type=str, help='p',)
args = parser.parse_args()
model = args.models
freq = args.frequencies
my_list = [str(item) for item in args.companies.split(',')]
companies = my_list[0].split()

my_list = [str(item) for item in args.adv_example_type.split(',')]
aet = my_list[0].split()

my_list = [str(item) for item in args.train_length.split(',')]
train_length = my_list[0].split()
train_length = [int(i) for i in train_length]

my_list = [str(item) for item in args.validation_length.split(',')]
validation_length = my_list[0].split()
validation_length = [int(i) for i in validation_length]

my_list = [str(item) for item in args.test_length.split(',')]
test_length= my_list[0].split()
test_length = [int(i) for i in test_length]

my_list = [str(item) for item in args.prediction_length.split(',')]
prediction_length = my_list[0].split()
prediction_length = [int(i) for i in prediction_length]

my_list = [str(item) for item in args.epochs.split(',')]
epochs = my_list[0].split()
epochs_length = [int(i) for i in epochs]

my_list = [str(item) for item in args.batch_size.split(',')]
batch_size = my_list[0].split()
batch_size = [int(i) for i in batch_size]

my_list = [str(item) for item in args.nbpe.split(',')]
nbpe = my_list[0].split()
nbpe = [int(i) for i in nbpe]

my_list = [str(item) for item in args.seed.split(',')]
seed = my_list[0].split()
seed = [int(i) for i in seed]

my_list = [str(item) for item in args.adv_dir.split(',')]
adv_dir = my_list[0].split()
adv_dir = [int(i) for i in adv_dir]

my_list = [str(item) for item in args.epsilon.split(',')]
epsilon = my_list[0].split()
epsilon = [float(i) for i in epsilon]

my_list = [str(item) for item in args.frac_amount.split(',')]
frac_amount = my_list[0].split()
frac_amount = [float(i) for i in frac_amount]

my_list = [str(item) for item in args.parameter.split(',')]
parameter = my_list[0].split()

big_list = [companies, aet,train_length,validation_length, test_length, prediction_length, epochs, batch_size, nbpe, seed, adv_dir, epsilon, frac_amount, parameter]

combinations = list(itertools.product(*big_list))

print(f'number of jobs for {model} {freq} ={len(combinations)}')

for instance in combinations:
    c,aaa,tl,vl,test_l,pl,e,b,num_b_p_e,s,d,eps,max_iter_single,param= tuple(instance)
    job_file = f"./job_files/{model}{freq}{c}.slrm"
    with open(job_file, 'w+') as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH --time=12:00:00\n")
        fh.writelines("#SBATCH --mem=5g\n")
        fh.writelines("#SBATCH --cpus-per-task=1\n")
        fh.writelines("#SBATCH --gres=gpu:0\n")
        fh.writelines("#SBATCH --partition=cpu\n")
        fh.writelines("#SBATCH --qos=nopreemption\n")
        fh.writelines("#SBATCH --open-mode=append\n")
        fh.writelines("echo `date`: Job $SLURM_JOB_ID is allocated resource\n")
        fh.writelines("ln -sfn /checkpoint/${USER}/${SLURM_JOB_ID} $PWD/models\n")
        fh.writelines("touch /checkpoint/${USER}/${SLURM_JOB_ID}/DELAYPURGE\n")
        fh.writelines("export LD_LIBRARY_PATH=/pkgs/cuda-10.1/lib64:/pkgs/cudnn-10.1-v7.6.3.30/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}\n")
        fh.writelines("export PATH=/pkgs/anaconda3/bin:$PATH\n")
        fh.writelines("source activate /scratch/ssd001/home/$USER/finance_env/\n")

        fh.writelines(f"python -u WHILE_{model}-Log_diff-{freq}_Attacked.py --company {c} --bit {args.bit} --adv_example_type {aaa} --train_length {tl} --validation_length {vl} --test_length {test_l} --prediction_length {pl} --epochs {e} --batch_size {b} --nbpe {num_b_p_e} --seed {s} --adv_dir {d} --epsilon {eps} --frac_amount {max_iter_single} --parameter {param}\n")
        fh.writelines(f"conda deactivate\n")
    os.system("sbatch %s" %job_file)
    time.sleep(0.3)
