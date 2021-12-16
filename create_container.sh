DB_psn=$(cat config.txt)
DB_psn="img:${DB_psn}"
docker build -t $DB_psn .
docker run --gpus all -it -v /Docker_vol/syzygy:/syzygy -v /Docker_vol/Gaviota:/Gaviota -v /Docker_vol/samples:/samples -v /Docker_vol/EGTB:/EGTB -v /Docker_vol/Positions:/Positions -v /Docker_vol/failing:/failing -v /Docker_vol/weights:/weights $DB_psn
