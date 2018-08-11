set -e

if [ "$#" -lt 1 ]
then
    echo "Usage: $0 <seed image> [--new]"
    exit
fi

roi_info=()

#Start the drawing process if --new parameter is set
#Update roi
if [[ "$2" = "--new" ]]
then
    ./bin/selectroi $1 ./config/roi
fi

#Update vid generation info with mov
    
#Read in rois file. Each line makes up an element of roi_info array
roi_info=()
while IFS= read -r info
do
    roi_info+=("$info")    
done < ./config/roi

#Check number of roi. Should only have 1 roi
if [ "${#roi_info[@]}" -ne 1 ]
then
    echo "${#roi_info[@]} rois selected! Should only be 1!"
    exit
fi

#Generate CENTER
params=(${roi_info[0]})
let center_x="${params[0]}+${params[2]}/2"
let center_y="${params[1]}+${params[3]}/2"
CENTER="CENTER\t${center_x}\t${center_y}"

#Generate vid file
cp -f ./config/mov ./config/vid
echo -e ${CENTER} >> ./config/vid
