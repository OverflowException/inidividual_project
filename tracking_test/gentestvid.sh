set -e

if [ "$#" != 1 ]
then
    echo "Usage: $0 <seed image>"
    exit
fi

./bin/gentestvid ./config/vid $1 ./videos/test.avi > ./data/gen
