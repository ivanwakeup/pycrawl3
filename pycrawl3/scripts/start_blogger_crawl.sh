#!/bin/bash

sleep=1000
TIMES=100

until [ $TIMES -lt 0 ]; do
    echo 'starting crawl for potential bloggers...'
    python crawl_potential_bloggers.py &
    sleep $sleep

    printf 'KILLING POTENTIAL BLOGGER CRAWLER!!!!\n\n\n\n'

    kill $(pgrep -f 'python')
    echo 'starting potential blogger analysis'
    python analyze_potential_bloggers.py &
    sleep $sleep


    printf 'KILLING ANALYZER BLOGGER CRAWLER!!!!\n\n\n\n'

    kill $(pgrep -f 'python')
    let TIMES-=1
done

