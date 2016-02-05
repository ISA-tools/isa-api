#!/usr/bin/env bash

# get the directory where this script is stored
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# the directory whre the SRA XML files are stored
echo "We are in the batch SRA 2 ISA-tab conversion script"
echo "\nArguments are: "
echo $1
echo "\nThis file parent directory is: "
echo ${DIR}

SRA_DIR=${DIR}/../../resources/sra

input_file=${SRA_DIR}/blank.xml
xsl_study_file=${SRA_DIR}/sra-submission-embl-online2isatab-txt.xsl
xsl_submission_file=${SRA_DIR}/sra-study-embl-online2isatab.xsl

IFS=',' read -r -a array <<< "$1"
for index in "${!array[@]}"
do
    elem=${array[index]}
    echo "$index $elem"
    SAXON_HOME=$HOME/Applications/SaxonHE

    if [[ ${elem} =~ ^SRA|ERA  ]]
    then
        echo "$elem is SRA or ERA"
        java -jar ${SAXON_HOME}/saxon9he.jar ${input_file} ${xsl_submission_file} acc-number="${elem}"

        # if there is some error return the error code
        if (($? > 0)); then
            echo -e "Error while processing file: ${elem}\n"
            # exit $?
            # possibly remove the subdirectory for that element??
        fi

    elif [[ ${elem} =~ ^SRP|ERP ]]
    then
        echo "$elem is SRP or ERP"
        java -jar ${SAXON_HOME}/saxon9he.jar ${input_file} ${xsl_study_file} acc-number="${elem}"
        # if there is some error return the error code
        if (($? > 0)); then
            echo -e "Error while processing file: ${elem}\n"
            # exit $?
            # possibly remove the subdirectory for that element??
        fi
    fi

done
# exit 0