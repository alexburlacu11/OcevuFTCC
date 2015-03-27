IVORN=$(hostname --long | tr -d ' ')/voevent-test
twistd comet -r --print-event \
    --verbose \
	--remote=68.169.57.253 \
    --local-ivo=ivo://$IVORN \
	--eventdb=/mnt/shared/voevents_received