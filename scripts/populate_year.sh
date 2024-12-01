YEAR=`date +%Y`
mkdir $YEAR -p -v
for D in $(seq 1 25)
do cp -n -v scripts/template.py $YEAR/$D.py
done