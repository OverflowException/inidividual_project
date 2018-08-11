set -e

if [ "$#" != 1 ]
then
    echo "Usage: $0 <algorithm>"
    exit
fi

BIN_PATH=../multiple_tracker/bin

${BIN_PATH}/multitracker ./videos/test.avi -r ./config/roi -a $1 > ./data/test

