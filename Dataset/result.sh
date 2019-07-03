for name in `cat $1`
do
	res=$name"_cubic.pdb"
	nres=`grep ATOM $res | wc | awk '{print $1}'`
	rms=`grep cRMS $res | awk '{print $7}'`
	echo $name "  " $nres " " $rms >>cath2225.res
done
