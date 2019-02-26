#!/usr/bin/perl
use strict;
use warnings;
use open ':std', ':encoding(UTF-8)';

use XML::LibXML;

my $dom = XML::LibXML->load_xml(location => "database/amara_mula.csv");
open(my $output, '>', "database/tmp_mula.csv") or die "Could not open output file $1\n";


my @kanda_names = ("/doc/amara/kANda_1", "/doc/amara/kANda_2", "/doc/amara/kANda_3");
my $uid=0;

foreach my $kanda (@kanda_names) {
  foreach my $sloka ($dom->findnodes($kanda)) {
      foreach my $child ($sloka->childNodes) {
        if ($child->nodeName =~ /Sloka_.*/) {

          my $text = $child->to_literal();

          if ( $child->nodeName() =~ /Sloka_(.*)/ ) {

            my $sloka_number = $1;

            $sloka_number =~ /^([0-9]*\.[0-9]*)/;
            my $varga_number = $1;

            my $line = 1;
            for (grep { /\S/ } split /^/, $text) {
              printf $output ("%d,%s,%s,%s.%d,,%s", $uid++, $varga_number, $sloka_number, $sloka_number, $line++, $_);
            }
          }
        }
    }
  }
}
