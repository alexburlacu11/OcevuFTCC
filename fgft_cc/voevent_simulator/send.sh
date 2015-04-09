
#!/bin/bash
for filename in voevents_to_send/*.xml; do
	comet-sendvo -f "$filename"
    sleep 10
done
