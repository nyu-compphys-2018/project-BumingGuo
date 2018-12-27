#!/bin/bash

sqrtN=256
let "N = sqrtN*sqrtN"
istart=200

dir0=$SCRATCH/Data/hoomd/melting_hard-disk/sqrtN${sqrtN}
dir=$dir0/analyse/grid
mkdir $dir 

for (( log2Ngrid=9; log2Ngrid<=14; log2Ngrid++ )); do

#for phi in 0.694 0.722 0.720 0.718 0.716 0.714 0.711 0.708 0.705 0.702 0.700 0.698; do
for phi in 0.720 0.719 0.718 0.717 0.716 0.714 0.712 0.710 0.708 0.706 0.704 0.702 0.700 0.699 0.698 0.697; do

fn_in=dump_N${N}_phi${phi}.gsd
fn_out=CID_N${N}_phi${phi}_${log2Ngrid}.dat
name=cid_${sqrtN}^2_${phi}_${log2Ngrid}

echo -e "#!/bin/bash

#SBATCH --job-name=${name}
#SBATCH --error=${name}_%J.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task 2
#SBATCH --time=168:00:00
#SBATCH --mem=8GB

set -x

cd $dir0/phi${phi}
python $dir0/cid.py ${fn_in} ${fn_out} ${log2Ngrid} ${istart}

" > ${name}.sh

echo -e "sbatch ${name}.sh" >> sub.sh

done

done

chmod +x *.sh
