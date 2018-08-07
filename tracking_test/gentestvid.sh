set -e

BIN_PATH=./bin
VIDEO_PATH=./videos
CONFIG_PATH=./config/vid
DATA_PATH=./data/gen

SEED_IMAGE_NAME=./images/panto.bmp

for vid in `ls ${CONFIG_PATH}`
do
    VIDEO_NAME=${VIDEO_PATH}/${vid}.avi
    DATA_NAME=${DATA_PATH}/${vid}
    echo "Generating ${VIDEO_NAME}..."
    #Generate video, redirect data
    ${BIN_PATH}/gentestvid ${CONFIG_PATH}/${vid} ${SEED_IMAGE_NAME} ${VIDEO_NAME} > ${DATA_NAME}
done
