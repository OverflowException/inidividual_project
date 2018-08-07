set -e

rois_info=()

#Start the drawing process if --new parameter is set
if [[ "$1" = "--new" ]]
then
    ./bin/selectroi ./images/panto.bmp ./config/rois
fi

    
#Read in rois file. Each line makes up an element of rois_info array
rois_info=()
while IFS= read -r info
do
    rois_info+=("$info")    
done < ./config/rois


#Generate separate roi configuration files
for i in "${!rois_info[@]}"
do
    echo -e ${rois_info[$i]} > ./config/roi/roi${i}
done

#Generate a corresponding video configuration file 
for i in "${!rois_info[@]}"
do
    params=(${rois_info[$i]})
    
    #Generate CENTER
    let center_x="${params[0]}+${params[2]}/2"
    let center_y="${params[1]}+${params[3]}/2"
    CENTER="CENTER\t${center_x}\t${center_y}"

    #GENERATE RECT
    RECT="RECT\t${params[2]}\t${params[3]}"

    #Generate video configuration file based on vid_templ
    vid_config_file=./config/vid/vid${i}
    cp -f ./config/vid_templ $vid_config_file
    echo -e $CENTER >> $vid_config_file
    echo -e $RECT >> $vid_config_file
done
