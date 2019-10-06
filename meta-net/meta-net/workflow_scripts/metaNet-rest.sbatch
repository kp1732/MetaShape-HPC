#! /usr/bin/bash

#SBATCH --job-name=metaNet-rest
#SBATCH --nodes=9
#SBATCH --cpus-per-task=28
#SBATCH --time=48:00:00
#SBATCH --mem=250GB
#SBATCH --gres=gpu:k80:4

#SBATCH --output=/beegfs/kp1732/meta-net/logs/client_logs/%j_metaNet-rest.out

#create node log directory
mkdir /beegfs/kp1732/meta-net/logs/node_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME"

#start metashape server on log-0 node, output to server log
ssh -x -f log-0 "metashape.sh --server --control log-0 --dispatch log-0 > /beegfs/kp1732/meta-net/logs/server_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME".log 2>&1"

#loop through allocated nodes and start metashape --node on each
for node in $(scontrol show hostname); do
    ssh -x -f $node "metashape.sh --platform offscreen --node --cpu_enable 1 --dispatch log-0 --root $1 > /beegfs/kp1732/meta-net/logs/node_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME"/$node.log 2>&1"
    sleep 1
done

#run match photos on project
metashape.sh --platform offscreen -r metaNet-rest.py log-0

#sleep for a bit then kill the metashape server instance
sleep 60
ssh log-0 "killall -9 metashape"
sleep 300



