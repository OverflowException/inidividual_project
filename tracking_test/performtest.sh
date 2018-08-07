set -e

if [ "$#" != 1 ]
then
    echo "Usage: $0 <algorithm>"
    exit
fi

BIN_PATH=../multiple_tracker/bin

vid_names=(`ls ./config/vid`)
roi_names=(`ls ./config/roi`)
for i in "${!vid_names[@]}"
do
    `${BIN_PATH}/multitracker ./videos/${vid_names[$i]}.avi -r ./config/roi/${roi_names[$i]} -a $1 > ./data/test/${vid_names[$i]}`
done

