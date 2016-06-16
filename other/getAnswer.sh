#!/bin/bash

rm -f data.result
rm -f tmp_sed
rm -f tmp_awk

line_num=""
i=1
answer=""
for tmp_var in `awk '{
				   print NR
				   print $2 
				}' awk.out`
do
	if [ $(($i % 2)) == 0 ]; 
	then 
		answer=$tmp_var #There maybe be two ansers
		ans_one=`echo $answer | awk -F, '{print $1}'`
		#ans_two=`echo $answer | awk -F, '{if($2~/^ *$/) print "TEST"}'`
		ans_two=`echo $answer | awk -F, '{print $2}'`
		up="QUESTION "$line_num
		tmp_line=$(($line_num+1))
		bottom="QUESTION "$tmp_line
		echo $up >> data.result 
		#sed -n -e '/^$/ q' -e "/$up$/,/$bottom$/ p" data > tmp_sed
		sed -n "/$up$/,/$bottom$/{/^$/ q; p}" data > tmp_sed
		awk '
			{
				if ($0 !~ /^[A-F]\. / && $0 !~ /^Answer:/ && $0 !~ /^QUESTION/) 
					print $0
			}' tmp_sed >> data.result 
	    echo -e "please enter"	
		read key
		if [ -z $ans_two ]; 
		then
			sed -n "/$up$/,/$bottom$/ {/^$ans_one\. /p}" data >> data.result
		else 
			sed -n "/$up$/,/$bottom$/ {/^$ans_one\. /p}" data >> data.result
			sed -n "/$up$/,/$bottom$/ {/^$ans_two\. /p}" data >> data.result
			#echo "two not null"
		fi
    else 
		line_num=$tmp_var
	fi	
	i=$(($i+1))
done
