#! /usr/bin/bash

#function grabs job number from sbatch output
grab_job_num () {
	
	for str in $1;
	do

        	if [[ $str =~ ^-?[0-9]+$ ]];
        	then
                	echo $str;
        	fi

	done 

}

cd /beegfs/kp1732/meta-net/workflow_scripts/

#run match photos job
MATCH_JOB="$(sbatch /beegfs/kp1732/meta-net/workflow_scripts/metaNet-match.sbatch /beegfs/kp1732/meta-net/output/main/)"
MATCH_JOB_NUM="$(grab_job_num "$MATCH_JOB")"

#run align camera job with dependancy on match photos
ALIGN_JOB="$(sbatch --dependency=afterok:$MATCH_JOB_NUM /beegfs/kp1732/meta-net/workflow_scripts/metaNet-align.sbatch /beegfs/kp1732/meta-net/output/intermediate/align_step/)"
ALIGN_JOB_NUM="$(grab_job_num "$ALIGN_JOB")"

#run depth maps job with dependance on align
DEPTH_JOB="$(sbatch --dependency=afterok:$ALIGN_JOB_NUM /beegfs/kp1732/meta-net/workflow_scripts/metaNet-depth.sbatch /beegfs/kp1732/meta-net/output/intermediate/align_step/)"
DEPTH_JOB_NUM="$(grab_job_num "$DEPTH_JOB")"

#run rest of job with dependancy on depth
DENSE_JOB="$(sbatch --dependency=afterok:$DEPTH_JOB_NUM /beegfs/kp1732/meta-net/workflow_scripts/metaNet-rest.sbatch /beegfs/kp1732/meta-net/output/intermediate/dense_step/)"






