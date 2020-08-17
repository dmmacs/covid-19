
cd /srv/www/web/covid
echo `pwd`

date
echo "Getting data from cdc"
./covid_19.py
chmod 666 *.js
retVal=$?

if [ $retVal -ne 0 ]; then
    echo "Failed to Run"
    exit 1
fi


date
