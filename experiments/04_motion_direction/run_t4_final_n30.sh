#!/bin/bash
# Final, fully-checked T4 cardinal-direction test: real 6x-calibrated
# delay, shunt-tau bug fix active, C3 now included (real wiring, real
# sign, real gain, real delay) -- all four subtypes, N=30.
cd /Users/pravin/projects/flybrain-sim/experiments/04_motion_direction
source ../../.venv/bin/activate
mkdir -p /tmp/t4_final_n30

BOOST="Mi1:T4a:0.65,Mi1:T4b:0.65,Mi1:T4c:0.65,Mi1:T4d:0.65,Tm3:T4a:0.35,Tm3:T4b:0.35,Tm3:T4c:0.35,Tm3:T4d:0.35,Mi4:T4a:1.10,Mi4:T4b:1.10,Mi4:T4c:1.10,Mi4:T4d:1.10,Mi9:T4a:0.92,Mi9:T4b:0.92,Mi9:T4c:0.92,Mi9:T4d:0.92,C3:T4a:1.49,C3:T4b:1.49,C3:T4c:1.49,C3:T4d:1.49"

for sub in T4a T4b T4c T4d; do
  for cond in pref anti; do
    for seed in $(seq 1 30); do
      out="/tmp/t4_final_n30/${sub}_${cond}_seed${seed}.csv"
      [ -f "$out" ] && continue
      python3 ../../core/simulate.py \
        --edges data_full/edges_R_final_withC3_signed.csv --neurons data_full/neurons_R_final_withC3.csv \
        --stimulus-sequence stimuli_full/seq_aligned_${sub}_${cond}_R.npy --stimulus-sequence-bodyids stimuli_full/seq_aligned_${sub}_${cond}_R_bodyids.csv \
        --frame-duration 10 --duration 600 --input-current 12 --noise-sigma 0.5 --seed $seed \
        --adapt-types Mi1,Tm3 --tau-adapt 40 --adapt-strength 2 \
        --shunt-types T4a,T4b,T4c,T4d --shunt-ach-types Mi1,Tm3 --shunt-gaba-types Mi4,C3 --shunt-glu-types Mi9 \
        --type-boost "$BOOST" --spatial-delay-csv data_full/spatial_delays_t4_withC3.csv \
        --slow-syn-types Mi4,Mi9 --tau-syn-slow 50 \
        --spike-times-out "$out" > "${out%.csv}.log" 2>&1
    done
  done
  echo "$sub done"
done
echo ALL_DONE
