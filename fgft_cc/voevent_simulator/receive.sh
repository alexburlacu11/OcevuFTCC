IVORN=$(hostname --long | tr -d ' ')/voevent-test
twistd comet -r --print-event \
    --verbose \
    --local-ivo=ivo://$IVORN \
    --eventdb=voevents_received
#--remote=68.169.57.253
