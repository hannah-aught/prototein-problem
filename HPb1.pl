# HPb1.pl
# this is essentially the same as HPb.pl, but instead of an n by n grid, it uses an n/4 by n/4 grid.
# October 26, 2016
# formulate an ILP to solve the HP problem
#
# Uses a binary variable X(i,p) to indicate whether or not
# character i is assigned to position p. An earlier effort, in HP.pl
# uses an integer variable X(i) whose value specifies which node on the grid will be assigned
# character i.  
#

open (IN, $ARGV[0]);   # this is the file name where the binary sequence is.
open (OUT, ">$ARGV[0].lp");  # this is the output file used for the concrete ILP formulation 
                             # that is created.

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
$denominator = 4;
$diam = 1 + int($n/$denominator);
#$diam = 3;
print "diameter $diam\n";
$diamsquared = $diam**2;

$k = 1;
foreach $i (1 .. $diam) { # loop through the edges in the diam-by-diam grid to set up
                       # the objective function, and also set up the inequalities to count 
                       # the number of edges whose endpoints are both assigned a character whose
                       # value is 1.
   foreach $j (1 .. $diam) { 

    if ($j < $diam) {
      $kp1 = $k + 1;        # horizontal edges
      $objective .=  "+  C$k,$kp1 ";
#      $secondary .= "+ I$k ";
      $Econstraints .= "I$k + I$kp1 - 2 C$k,$kp1 >= 0\n";   # C can be set to 1 only if both endpoints are assigned 1s.
      $binaries .= "C$k,$kp1\n";
    }

      if ($i < $diam) {
         $kpn = $k + $diam;   # vertical edges
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
   foreach $pos (1 .. $diamsquared) {
      $constraints .= "+ X$i,$pos ";
      $binaries .= "X$i,$pos\n";
   }
   $constraints .= "=  1 \n";
}

foreach $pos (1 .. $diamsquared) {   # set up inequalties to ensure each position is assigned at most one character 
   foreach $i (1 .. $n) {
      $constraints .= "+ X$i,$pos ";
   }
   $constraints .= "<=  1 \n";
}

$gridbase = $diam + 2;        # create inequalities to ensure that chars i and i+1 are neighbors on the grid
                         # first takecare of the general cases, and then do the external rows
                         # and columns.

foreach $row (2 .. $diam-1) {  # middle rows
    foreach $offset (0 .. $diam - 3) {  
        $point = $gridbase + $offset;
        foreach $i (1 .. $n - 1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $diam;
            $pointnn = $point - $diam;

            $constraints .= "X$i,$point ";
            $constraints .= "- X$ip1,$pointp1 - X$ip1,$pointn1 - X$ip1,$pointpn - X$ip1,$pointnn <= 0\n";
        }
     }
$gridbase += $diam;
}

$gridbase = 2;
foreach $offset (0 .. $diam - 3) { # take care of the first row of the grid, minus the points in the
                              # first and last columns.

        $point = $gridbase + $offset;
        foreach $i (1 .. $n - 1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $diam;
            $pointnn = $point - $diam;

            $constraints .= "X$i,$point ";
            $constraints .= "- X$ip1,$pointp1 - X$ip1,$pointn1 - X$ip1,$pointpn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES1\n";
            }
        }
     }

$gridbase = $diam * ($diam - 1) + 2;
foreach $offset (0 .. $diam - 3) { # take care of the last row of the grid, minus the points in the
                              # first and last columns.

        $point = $gridbase + $offset;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $diam;
            $pointnn = $point - $diam;

            $constraints .= "X$i,$point ";
            $constraints .= "- X$ip1,$pointp1 - X$ip1,$pointn1 - X$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES2\n";
            }
        }
     }


$gridbase = $diam  + 1;
foreach $offset (0 .. $diam - 3) { # take care of the first column minus the corners.

        $point = $gridbase + $offset * $diam;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $diam;
            $pointnn = $point - $diam;

            $constraints .= "X$i,$point ";
            $constraints .= "- X$ip1,$pointp1 - X$ip1,$pointpn - X$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES3\n";
            }
        }
     }


$gridbase = 2*$diam;
foreach $offset (0 .. $diam - 3) { # take care of the last column minus the corners.

        $point = $gridbase + $offset * $diam;
        foreach $i (1 .. $n-1) {
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $diam;
            $pointnn = $point - $diam;

            $constraints .= "X$i,$point ";
            $constraints .= "- X$ip1,$pointn1 - X$ip1,$pointpn - X$ip1,$pointnn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES4\n";
               print ("$i, $ip1, $gridbase, $offset, $point, $pointn1, $pointpn, $pointnn \n");
            }
        }
     }


        foreach $i (1 .. $n-1) {
            foreach $point (1, $diam, $diam * ($diam - 1) + 1, $diamsquared) {  # take care of the corner cases
            $ip1 = $i + 1;
            $pointp1 = $point + 1;
            $pointn1 = $point - 1;
            $pointpn = $point + $diam;
            $pointnn = $point - $diam;

          
            if ($point == 1) {
                 $constraints .= "X$i,$point ";
                 $constraints .= "- X$ip1,$pointp1 - X$ip1,$pointpn  <= 0\n";
            if ($pointn1 < 0) {
               print "YIKES5\n";
            }
            }

            if ($point == $diam * ($diam - 1) + 1) {
                 $constraints .= "X$i,$point ";
                 $constraints .= "- X$ip1,$pointp1 - X$ip1,$pointnn  <= 0\n";
            }

            if ($point == $diam) {
                 $constraints .= "X$i,$point ";
                 $constraints .= "- X$ip1,$pointn1 - X$ip1,$pointpn  <= 0\n";
            }

            if ($point == $diamsquared) {
                 $constraints .= "X$i,$point ";
                 $constraints .= "- X$ip1,$pointn1 - X$ip1,$pointnn  <= 0\n";
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

foreach $pos (1 .. $diamsquared) {   # create inequalities to set I$pos to 1 only if a char with value 1 is assigned to $pos
    $assigned1 = "";
    foreach $char (sort {$a <=> $b} keys %ones) {
       $charp1 = $char + 1;
       $assigned1 .= "+ X$charp1,$pos ";
    }
    $binaries .= "I$pos \n";
    $constraints .= "$assigned1 - I$pos = 0 \n";
#    $constraints .= "$assigned1 - I$pos >= 0 \n";
#    $constraints .= "$assigned1 - I$pos <= 0 \n";
}

print OUT "$objective - Offset \n";
#print OUT "$secondary  \n\n";
print OUT "subject to \n";
print OUT "Offset = $neighbors1 \n";
print OUT "$constraints \n\n";
print OUT "$Econstraints \n\n";
print OUT "binary \n";
print OUT "$binaries \n";
print OUT "end";
close OUT;

print "The ILP formulation is in file $ARGV[0].lp \n";
