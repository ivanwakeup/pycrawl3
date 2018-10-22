#!/bin/bash

sleep=1000

echo 'starting crawl for potential bloggers...'
python crawl_potential_bloggers.py &
sleep $sleep

printf 'KILLING POTENTIAL BLOGGER CRAWLER!!!!\n\n\n\n'

kill $(pgrep -f 'crawl_potential_bloggers.py')
echo 'starting potential blogger analysis'
python analyze_potential_bloggers.py &
sleep $sleep


printf 'KILLING ANALYZER BLOGGER CRAWLER!!!!\n\n\n\n'

kill $(pgrep -f 'analyze_potential_bloggers.py')

python score_bloggers.py



