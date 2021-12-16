/etc/init.d/mysql start
mysql -uroot -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456ab';FLUSH PRIVILEGES;"
python3 /Py/sampling_positions.py $(cat config.txt)
python3 /Py/samples_DTM.py $(cat config.txt)
python3 /Py/second_best_for_draw.py $(cat config.txt)
DB_dir=$(cat config.txt)
mkdir DB_dir
cp -r /var/lib/mysql/EGTB $DB_dir
cp -r $DB_dir /EGTB 
python3 /Py/Wrong_play.py $(cat config.txt)
