#!/usr/bin/perl
use strict;
use warnings;

open(my $data, '<', "database/amara_pada.utf8") or die "Could not open input file $!\n";
open(my $output, '>', "database/tmp_pada.csv") or die "Could not open output file $1\n";

my $uid=0;
while (my $line = <$data>) {
  chomp $line;

  $line =~ s/_/ /g;
  my @fields = split "," , $line;

  my $pada = $fields[0];
  my $sloka_number = $fields[1] =~ s/^(.*\..*\..*)\..*\..*$/$1/r;
  my $sloka_line = $fields[1] =~ s/^(.*\..*\..*\..*)\..*$/$1/r;
  my $sloka_word = $fields[1];
  my $linga = $fields[2];
  my $varga = $fields[3];
  my $artha = $fields[4];

  printf $output ("%d,%s,%s,%s,%s,%s,%s,%s\n", $uid++, $sloka_number, $sloka_line, $sloka_word, $pada, $linga, $varga, $artha);

  # printf $output ("%d,%s,%s,%s,%s,%s,%s\n", $uid++, $fields[0], $sloka_number, $fields[1], $fields[2], $fields[3], $fields[4]);
}
