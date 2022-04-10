#!/usr/bin/env bash

for test in ./tests/*.reti; do
  sed -n '1p' $test | sed -e 's/^# in://' > ./tests/$(basename --suffix=.reti $test).in
  sed -n '2p' $test | sed -e 's/^# except://' > ./tests/$(basename --suffix=.reti $test).out_except
done
