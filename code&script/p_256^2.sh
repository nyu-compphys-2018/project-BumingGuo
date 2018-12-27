#!/bin/bash

sqrtN=256
let "N = sqrtN*sqrtN"
istart=200

dir0=$SCRATCH/Data/hoomd/melting_hard-disk/sqrtN${sqrtN}
dir=$dir0/analyse
mkdir $dir 

#for phi in 0.694 0.722 0.720 0.718 0.716 0.714 0.711 0.708 0.705 0.702 0.700 0.698; do
for phi in 0.720 0.719 0.718 0.717 0.716 0.714 0.712 0.710 0.708 0.706 0.704 0.702 0.700 0.699 0.698 0.697; do

cd $dir0/phi${phi}

filename=sdf_N${N}_phi${phi}.dat

python $dir0/calc_p.py ${filename} ${phi} ${istart}

mv tmp $dir/p_all_${sqrtN}^2_${phi}.dat
mv tmp_equi $dir/p_${sqrtN}^2_${phi}.dat
mv tmp_p $dir/t_p_${sqrtN}^2_${phi}.dat

done
