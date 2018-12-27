#!/bin/bash

sqrtN=256
seed=100

dir0=$HOME/Jobs/hoomd/melting_hard-disk
mkdir $dir0/data/sqrtN${sqrtN}

for phi in 0.697 0.698 0.699 0.700 0.702 0.704 0.706 0.708 0.710 0.712 0.714 0.716 0.717 0.718 0.719 0.720; do

dir=$dir0/data/sqrtN${sqrtN}/phi${phi}
mkdir $dir

let "seed = seed + 1"
name=melting_${sqrtN}^2_${phi}

echo -e "#!/bin/bash

#SBATCH --job-name=${name}
#SBATCH --output=${name}_%J.out
#SBATCH --error=${name}_%J.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task 2
#SBATCH --gres=gpu:1
#SBATCH --partition=v100_sxm2_4,v100_pci_2,p100_4
#SBATCH --time=120:00:00
#SBATCH --mem=8GB

set -x

module purge
module load hoomd-blue/openmpi/intel/2.6.1

cd $dir
python $dir0/hard-disk.py --mode=gpu --user='${sqrtN} ${phi} ${seed}'

" > ${name}.sh

echo -e "sbatch ${name}.sh" >> sub.sh

done

chmod +x *.sh
