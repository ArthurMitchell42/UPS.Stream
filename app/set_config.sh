#!/usr/bin/sh
FILE=/config/config.txt
echo -n 'name ' > $FILE
echo $USER_NAME >> $FILE
echo -n 'pass ' >> $FILE
echo $PASSWORD >> $FILE
echo -n 'time ' >> $FILE
echo $SERVER_POLL_RATE >> $FILE
echo -n 'addr ' >> $FILE
echo $NUT_SERVER_IP >> $FILE
echo -n 'port ' >> $FILE
echo $NUT_SERVER_PORT >> $FILE
