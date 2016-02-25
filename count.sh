#!/usr/bin/env bash
cat f_mupssan20140901.log | awk -F "\|" '{count[$1]++;}END{for (i in count) print i, count[i]}'
