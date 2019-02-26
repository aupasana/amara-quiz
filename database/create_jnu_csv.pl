#!/usr/bin/perl
use strict;
use warnings;
use open ':std', ':encoding(UTF-8)';

# curl http://sanskrit.jnu.ac.in/amara/viewdata.jsp?wordid=[1-4155] -o "jnu/#1.html"

for (my $i=1; $i <= 4155; $i++) {
  open(my $data, '<', "jnu/$i.html") or die "Could not open input file $!\n";

  my @tokens = ("Base Word", "English", "Hindi", "Kannada", "Bangla", "Oriya", "Punjabi", "Assamese", "Maithili");

  my %values;
  my $values = {};

  foreach my $token (@tokens) {
    $values->{$token} = "";
  }
  $values->{"reference"} = "";

  while (my $line = <$data>) {

    # chomp $line;
    $line =~ s/\R//g;

    # <tr><td bgcolor=ffffff><b>Reference:</b></td><td bgcolor=ffffff>1.1.6</td></tr>
    # <b>Base Word:</b> </td><td bgcolor=d3d3d3>स्वः
    # <b>English:</b></td><td bgcolor=ffffff>Heaven

    if ($line =~ /.*Reference.*>([0-9]*\.[0-9]*\.[0-9]*)<.*/) {
      $values->{"reference"} = $1;
    }

    foreach my $token (@tokens) {
      if ( $line =~ /.*$token.*>(.*)/ ) {
        my $value = $1;
        $value =~ s/,/-/g;
        $values->{$token} = $value;
      }
    }

  }

  print "$i,$values->{'reference'},$values->{'Base Word'},$values->{'English'},$values->{'Hindi'},$values->{'Kannada'},$values->{'Bangla'},$values->{'Oriya'},$values->{'Punjabi'},$values->{'Assamese'},$values->{'Maithili'}\n";
}
