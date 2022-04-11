#!/usr/bin/env bash

num_tests=0;
not_running_through=();
not_passed=();
  for testfile in ./tests/*$1*.reti; do
    echo -e "\n\033[1;37m===============================================================================";
    echo $testfile;
    echo -e "===============================================================================\033[0;0m";
    ./src/main.py -c -t -a -o -r -p -b 8 -d 32 -D 20 -s 2 -E 8 -U 4 -S 0 -C -m $2 $testfile

    if [[ $? != 0 ]]; then
      not_running_through+=($testfile);
    fi;
    diff ./tests/$(basename --suffix=.reti $testfile).out_except ./tests/$(basename --suffix=.reti $testfile).out
    if [[ $? != 0 ]]; then
      not_passed+=($testfile);
    fi
    ((num_tests++));
done;
echo Running through: $(($num_tests-${#not_running_through[@]})) / $num_tests;
echo Passed: $(($num_tests-${#not_passed[@]})) / $num_tests;
echo Not running through tests: ${not_running_through[*]};
echo Not passed tests: ${not_passed[*]};

if [[ ${#not_passed[@]} != 0 ]]; then
    exit 1
fi
