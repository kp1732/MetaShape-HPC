#! /usr/bin/bash

#SBATCH --job-name=metaNet-DMT
#SBATCH --nodes=3
#SBATCH --cpus-per-task=28
#SBATCH --time=48:00:00
#SBATCH --mem=250GB
#SBATCH --gres=gpu:k80:4

#SBATCH --output=/beegfs/kp1732/meta-net/logs/client_logs/%j_metaNet-rest.out

#create node log directory
mkdir /beegfs/kp1732/meta-net/logs/node_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME"

#start metashape server on log-0 node, output to server log
NODE=$(hostname)
ssh -x -f $NODE "metashape.sh --server --control $NODE --dispatch $NODE > /beegfs/kp1732/meta-net/logs/server_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME".log 2>&1"

#loop through allocated nodes and start metashape --node on each
for node in $(scontrol show hostname); do
    ssh -x -f $node "metashape.sh --platform offscreen --node --cpu_enable 1 --dispatch $NODE --root $1 > /beegfs/kp1732/meta-net/logs/node_logs/"$SLURM_JOB_ID"_"$SLURM_JOB_NAME"/$node.log 2>&1"
    sleep 1
done

#process dense cloud and model on project
metashape.sh --platform offscreen -r metaNet-denseModel.py $NODE

#process texture on the project
metashape.sh --platform offscreen -r metaNet-texture.py $NODE

#sleep for a bit then kill the metashape server instance
echo "KILLING META SERVER"
sleep 60
ssh $NODE "killall -9 metashape"
sleep 300



