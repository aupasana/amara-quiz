#!/usr/bin/perl
use strict;
use warnings;

open(my $data, '<', "database/amara_tokens.utf8") or die "Could not open input file $!\n";
open(my $output, '>', "database/tmp_tokens.csv") or die "Could not open output file $1\n";

my $line_number=0;
while (my $line = <$data>) {
  chomp $line;

  $line =~ s/_/ /g;
  my @fields = split "," , $line;
  my $sloka_number = @fields[1] =~ s/^(.*\..*\..*)\..*\..*$/$1/r;

  printf $output ("%d,%s,%s,%s,%s,%s,%s\n", $line_number,@fields[0], $sloka_number, @fields[1], @fields[2], @fields[3], @fields[4]);
  $line_number++;
}
