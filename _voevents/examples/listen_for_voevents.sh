IVORN=$(hostname --long | tr -d ' ')/voevent-test

twistd comet -r --print-event --save-event \
    --verbose \
    --local-ivo=ivo://$IVORN \
	--eventdb=/mnt/shared/rec