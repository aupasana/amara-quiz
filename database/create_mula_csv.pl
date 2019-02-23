#!/usr/bin/perl
use strict;
use warnings;
use open ':std', ':encoding(UTF-8)';

use XML::LibXML;

my $dom = XML::LibXML->load_xml(location => "database/amara_mula.utf8");
open(my $output, '>', "database/tmp_mula.csv") or die "Could not open output file $1\n";


my @kanda_names = ("/doc/amara/kANda_1", "/doc/amara/kANda_2", "/doc/amara/kANda_3");
my $uid=0;

foreach my $kanda (@kanda_names) {
  foreach my $sloka ($dom->findnodes($kanda)) {
      foreach my $child ($sloka->childNodes) {
        if ($child->nodeName =~ /Sloka_.*/) {

          my $text = $child->to_literal();

          if ( $child->nodeName() =~ /Sloka_(.*)/ ) {

            my $line = 1;
            for (grep { /\S/ } split /^/, $text) {
              printf $output ("%d,%s,%s.%d,,%s", $uid++, $1, $1, $line++, $_);
            }
          }
        }
    }
  }
}
