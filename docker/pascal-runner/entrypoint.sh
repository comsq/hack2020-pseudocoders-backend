#!/bin/bash

COMPILATION_ERROR_CODE=11
TIME_LIMIT_ERROR_CODE=12
RUNTIME_ERROR_CODE=13
WRONG_ANSWER_ERROR_CODE=20

WORKDIR=/tmp/workdir
SOURCEDIR=/source
TESTSDIR=/tests

mkdir $WORKDIR

# Compile source

cd $SOURCEDIR
fpc main.pas -o$WORKDIR/main

if (( $? != 0 )); then
    exit $COMPILATION_ERROR_CODE
fi

# Run checks

cd $WORKDIR

i=1
for inputpath in $TESTSDIR/input_*; do
    inputname=$(basename $inputpath)
    outputpath=$TESTSDIR/output_${inputname#"input_"}
    resultpath=$WORKDIR/$inputname

    echo -n "Run test case №$i ... "
    cat $inputpath | timeout -s KILL -t 5 $WORKDIR/main > $resultpath

    if (( $? != 0 )); then
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
