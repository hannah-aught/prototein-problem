for name in `cat $1`
do
	pdb=$name".pdb"
	res=$name"_cubic.pdb"
	../ChainGrowth/Mol2Lattice.ifort -i $pdb -o $res -t 1 -l 3.8 1>/dev/null 2>/dev/null
done
