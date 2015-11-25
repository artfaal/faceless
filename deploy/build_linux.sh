#!/bin/zsh

sh reload.sh
sleep 2
va
ipython run.py &
sleep 2
eos_cp_from_yad
eos_remove_cat
eos_remove_items
eos_xls_to_xsv
eos_write_category
eos_write_items