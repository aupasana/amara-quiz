#!/usr/bin/perl
use strict;
use warnings;

open(my $data, '<', "database/amara_pada.utf8") or die "Could not open input file $!\n";
open(my $output, '>', "database/tmp_pada.csv") or die "Could not open output file $1\n";

my %mula_artha = (
    # flintstones    => [ "fred", "barney" ],
    # jetsons        => [ "george", "jane", "elroy" ],
    # simpsons       => [ "homer", "marge", "bart" ],
);

while (my $line = <$data>) {
  chomp $line;

  $line =~ s/_/ /g;
  my @fields = split "," , $line;

  my $uid = $fields[0];
  my $pada = $fields[1];
  my $sloka_number = $fields[2] =~ s/^(.*\..*\..*)\..*\..*$/$1/r;
  my $sloka_line = $fields[2] =~ s/^(.*\..*\..*\..*)\..*$/$1/r;
  my $sloka_word = $fields[2];
  my $linga = $fields[3];
  my $varga = $fields[4];
  my $artha = $fields[5];

  if (! $mula_artha{$sloka_number}) {
    $mula_artha{$sloka_number} = [];
  }

  push $mula_artha{$sloka_number}, $artha;

  printf $output ("%d,%s,%s,%s,%s,%s,%s,%s\n", $uid++, $sloka_number, $sloka_line, $sloka_word, $pada, $linga, $varga, $artha);

  # printf $output ("%d,%s,%s,%s,%s,%s,%s\n", $uid++, $fields[0], $sloka_number, $fields[1], $fields[2], $fields[3], $fields[4]);
}

# foreach my $item (@{$HoA{$key}})
# {
#     print "Test item: $nextItem\n";
# }
