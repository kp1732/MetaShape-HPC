#! /usr/bin/bash

#SBATCH --job-name=metaNode
#SBATCH --nodes=1
#SBATCH --cpus-per-task=60
#SBATCH --time=48:00:00
#SBATCH --mem=150GB
#SBATCH --partition=knl
##SBATCH --gres=gpu:v100:4

#SBATCH --output=/beegfs/kp1732/meta-net/logs/client_logs/%j_metaNode-gpu.out

#PRINCE PRINCE_GPU_COMPUTE_MODE=default
#PRINCE PRINCE_GPU_DCGM_STATS=NO

#create node log directory
mkdir /beegfs/kp1732/meta-net/logs/node_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME"

#loop through allocated nodes and start metashape --node on each
for node in $(scontrol show hostname); do
    ssh -x -f $node "metashape.sh --platform offscreen --node --cpu_enable 1 --gpu_mask 255 --dispatch gpu-05 --root $1 > /beegfs/kp1732/meta-net/logs/node_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME"/$node.log 2>&1"
    sleep 1
done

#sleep forever so we don't loose the nodes
sleep 10000000000000



