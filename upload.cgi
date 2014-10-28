#!/usr/bin/perl

use strict;
use warnings;
use MIME::Base64;

&Main();

sub Main()
{
	my %POST = %{ &DecodePost() };

	# canvas.toDataURL() ==> data:TYPE,DATA
	# TYPE = image/png, image/jpeg, ...
	# DATA = Base64 encoded data
	my ( $type, $img ) = split( /\,/, $POST{ 'img' }, 2 );
	# Binary data.
	my $bin = decode_base64( $img );

	if ( ! ($type =~ /data\:image\/(.+)/ ) ) { &PrintJson( '{"code":"1"}' ); }

	my $filename = 'sample.' . $1;
	if ( ! open( IMG, "> $filename" ) ) { &PrintJson( '{"code":"2"}' ); }
	binmode( IMG );
	print IMG $bin;
	close( IMG );

	&PrintJson( '{"code":"0"}' );
}

sub PrintJson()
{
	my ( $json ) = ( @_ );
	print "Content-Type: application/json; charset=utf-8\n";
	printf( "Content-Length: %d\n", length( $json ) );
	print "\n";
	print $json;
	exit( 0 );
}

sub DecodePost()
{
	my ( @names ) = ( @_ );
	my %ret;
	if ( ($ENV{'CONTENT_LENGTH'} || 0) <= 0 ){ return \%ret; }

	my $que;
	read ( STDIN, $que, $ENV{'CONTENT_LENGTH'} );
	my @args = split( /&/, $que );

	foreach ( @args )
	{
		unless( $_ =~ /\=/ ){ next; }
		my ( $name, $val ) = split( /=/, $_, 2 );
		$val =~ tr/+/ /;
		$val =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack('C', hex($1))/eg;
		$val =~ s/\r//g;
		$ret{ $name } = $val;
	}

	foreach ( @names ) { unless ( exists( $ret{ $_ } ) ){ $ret{ $_ } = ''; } }

	return \%ret;
}
