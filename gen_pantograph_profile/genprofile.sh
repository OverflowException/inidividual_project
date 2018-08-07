set -e

for config_name in `ls ./config/`
do
    echo -e ${config_name}
    python python/gen_profile.py ./config/${config_name} ./profile/${config_name}.txt
    unix2dos ./profile/${config_name}.txt
done

