#!/usr/bin/env bash

for test in ./tests/*.reti; do
  sed -n '1p' $test | sed -e 's/^# in://' > ./${test%.reti}.in
  sed -n '2p' $test | sed -e 's/^# expected://' > ./${test%.reti}.out_expected
done
