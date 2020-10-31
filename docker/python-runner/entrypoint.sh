#!/bin/bash

COMPILATION_ERROR_CODE=11
TIME_LIMIT_ERROR_CODE=12
RUNTIME_ERROR_CODE=13
WRONG_ANSWER_ERROR_CODE=20

WORKDIR=/tmp/workdir
SOURCEDIR=/source
TESTSDIR=/tests

mkdir $WORKDIR

# Run checks

cd /

export PYTHONPATH=$SOURCEDIR

i=1
for inputpath in $TESTSDIR/input_*; do
    inputname=$(basename $inputpath)
    outputpath=$TESTSDIR/output_${inputname#"input_"}
    resultpath=$WORKDIR/$inputname

    echo -n "Run test case №$i ... "
    cat $inputpath | timeout -s KILL 5 python3 -m source > $resultpath

    if (( $? != 0 )); then
        echo "FAIL"
        exit $TIME_LIMIT_ERROR_CODE
    fi

    diff -Bb $outputpath $resultpath 2>&1 >/dev/null
    if (( $? != 0 )); then
        echo "FAIL"
        echo "Head of expected output:"
        head $outputpath
        echo "Head of actual output:"
        head $resultpath
        exit $(($WRONG_ANSWER_ERROR_CODE + $i - 1))
    else
        echo "OK"
    fi

    ((i++))
done
