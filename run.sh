#!/bin/sh

[ $# -ne 1 ] && echo Need Python Script && exit


python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "======= STARTING ======" >> run.txt
echo $0 $@ >> run.txt
pwd >> run.txt
python $@ | tee -a run.txt

