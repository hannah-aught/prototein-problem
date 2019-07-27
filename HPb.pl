# HPb.pl
# October 26, 2016
# formulate an ILP to solve the HP problem
# Uses a binary variable A(i,p) to indicate whether or not
# character i is assigned to position p. An earlier effort, in HP.pl
# uses an integer variable A(i) whose value specifies which node on the grid will be assigned
# character i.  
#

open (IN, $ARGV[0]);
open (OUT, ">$ARGV[0].lp");

print OUT "Maximize\n";

$objective = "";
$constraints = "";
$Econstraints = "";
$binaries = "";
$generals = "";

$sequence = <IN>;
chomp $sequence;
$n = length ($sequence);
print "$sequence, $n \n";
$nsquared = $n**2;

$k = 1;
foreach $i (1 .. $n) { # loop through the edges in the n-by-n grid to set up
                       # the objective function, and also set up the inequalities to count 
                       # the number of edges whose endpoints are both assigned a character whose
                       # value is 1.
   foreach $j (1 .. $n) { 

    if ($j < $n) {
      $kp1 = $k + 1;        # horizontal edges
      $objective .=  "+  C$k,$kp1 ";
#      $secondary .= "+ I$k ";
      $Econstraints .= "I$k + I$kp1 - 2 C$k,$kp1 >= 0\n";   # C can be set to 1 only if both endpoints are assigned 1s.
      $binaries .= "C$k,$kp1\n";
    }

      if ($i < $n) {
         $kpn = $k + $n;   # vertical edges
         $objective .= "+ C$k,$kpn ";
         $Econstraints .= "I$k + I$kpn - 2 C$k,$kpn >= 0\n";
         $binaries .= "C$k,$kpn\n";
      }
      $k = $kp1;
   }
   print "i: $i k: $k\n";
   $k++;   # increment k to account for the last node in each row.
}

foreach $i (1 .. $n) {    # set up inequalities to ensure each character is assigned to one position
   foreach $pos (1 .. $nsquared ) {
      $constraints .= "+ A$i,$pos ";
      $binaries .= "A$i,$pos\n";
   }
   $constraints .= "=  1 \n";
}

foreach $pos (1 .. $nsquared) {   # set up inequalties to ensure each position is assigned at most one character 
   foreach $i (1 .. $n ) {
      $constraints .= "+ A$i,$pos ";
   }
   $constraints .= "<=  1 \n";
}

$gridbase = $n+2;        # create inequalities to ensure that chars i and i+1 are neighbors on the grid
                         # first takecare of the general cases, and then do the external rows
                         # and columns.

foreach $row (2 .. $n-1) {  # middle rows
    foreach $offset (0 .. $n-3) {  
        $point = $gridbase + $offset;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $n;
            $pointnn = $point - $n;

            $constraints .= "A$i,$point ";
            $constraints .= "- A$ip1,$pointp1 - A$ip1,$pointn1 - A$ip1,$pointpn - A$ip1,$pointnn <= 0\n";
        }
     }
$gridbase += $n;
}

$gridbase = 2;
foreach $offset (0 .. $n-3) { # take care of the first row of the grid, minus the points in the
                              # first and last columns.

        $point = $gridbase + $offset;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $n;
            $pointnn = $point - $n;

            $constraints .= "A$i,$point ";
            $constraints .= "- A$ip1,$pointp1 - A$ip1,$pointn1 - A$ip1,$pointpn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES1\n";
            }
        }
     }

$gridbase = $n * ($n-1) + 2;
foreach $offset (0 .. $n-3) { # take care of the last row of the grid, minus the points in the
                              # first and last columns.

        $point = $gridbase + $offset;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $n;
            $pointnn = $point - $n;

            $constraints .= "A$i,$point ";
            $constraints .= "- A$ip1,$pointp1 - A$ip1,$pointn1 - A$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES2\n";
            }
        }
     }


$gridbase = $n + 1;
foreach $offset (0 .. $n-3) { # take care of the first column minus the corners.

        $point = $gridbase + $offset * $n;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $n;
            $pointnn = $point - $n;

            $constraints .= "A$i,$point ";
            $constraints .= "- A$ip1,$pointp1 - A$ip1,$pointpn - A$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES3\n";
            }
        }
     }


$gridbase = 2*$n;
foreach $offset (0 .. $n-3) { # take care of the last column minus the corners.

        $point = $gridbase + $offset * $n;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $n;
            $pointnn = $point - $n;

            $constraints .= "A$i,$point ";
            $constraints .= "- A$ip1,$pointn1 - A$ip1,$pointpn - A$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES4\n";
               print ("$i, $ip1, $gridbase, $offset, $point, $pointn1, $pointpn, $pointnn \n");
            }
        }
     }


        foreach $i (1 .. $n-1) {
            foreach $point (1, $n, $n * ($n-1) + 1, $nsquared) {  # take care of the corner cases
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $n;
            $pointnn = $point - $n;

          
            if ($point == 1) {
                 $constraints .= "A$i,$point ";
                 $constraints .= "- A$ip1,$pointp1 - A$ip1,$pointpn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES5\n";
            }
            }

            if ($point == $n * ($n-1) + 1) {
                 $constraints .= "A$i,$point ";
                 $constraints .= "- A$ip1,$pointp1 - A$ip1,$pointnn  <= 0\n";
            }

            if ($point == $n) {
                 $constraints .= "A$i,$point ";
                 $constraints .= "- A$ip1,$pointn1 - A$ip1,$pointpn  <= 0\n";
            }

            if ($point == $nsquared) {
                 $constraints .= "A$i,$point ";
                 $constraints .= "- A$ip1,$pointn1 - A$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES6\n";
            }
            }
        }
      }

# Now we create the inequalities to determine if a point has been assigned a 1 or not. Assign I$i to 1 if and only if
# grid point $i has been assigned a 1

@input = split(//,$sequence);
%ones = ();
$lastchar = 0;
$neighbors1 = 0;
foreach $char (0 .. $n-1) {    # use hash %ones to record the positions of the 1s in the sequence, and count
                               # the number of adjacent 1s. The objective function is reduced by that count.
   print "$char $input[$char] \n";
   if ($input[$char] eq 1) {
        if ($lastchar == 1) {
           $neighbors1++;   # increment the number of adjacent 1s in the input sequence
        }
      $ones{$char} = 1;
      $lastchar = 1;
   }
   else {
      $lastchar = 0;
   }
}
print "Neighbor count: $neighbors1 \n";

#$constraints2 = "";
foreach $pos (1 .. $nsquared) {   # create inequalities to set I$pos to 1 only if a char with value 1 is assigned to $pos
    $assigned1 = "";
    foreach $char (sort {$a <=> $b} keys %ones) {
       $charp1 = $char + 1;
       $assigned1 .= "+ A$charp1,$pos ";
    }
    $binaries .= "I$pos \n";
    $constraints .= "$assigned1 - I$pos = 0 \n";
#    $constraints2 .= "$assigned1 - I$pos >= 0 \n";
#    $constraints2 .= "$assigned1 - I$pos <= 0 \n";
}

print OUT "$objective - Offset \n";
print OUT "$secondary  \n\n";
print OUT "subject to \n";
print OUT "Offset = $neighbors1 \n";
print OUT "$constraints \n\n";
# print OUT "$constraints2 \n\n";
print OUT "$Econstraints \n\n";
print OUT "binary \n";
print OUT "$binaries \n";
print OUT "end";
close OUT;

print "The ILP formulation is in file $ARGV[0].lp \n";
