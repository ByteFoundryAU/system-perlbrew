# system-perlbrew
Some spec files, that will build a perlbrew that lives in /opt, along with perl's that live in /opt
If you run cpanm, the modules will be installed in /opt

The point is to use perlbrew in production, without having to compile on production and having gcc etc on the prod machine.

The perlbrew is designed to be installed so that various system users can use it (apache, nginx or whatever)

So the workflow is to install the perlbrew and perlbrew-perl rpm's (versions to suit your needs) then to use cpanm to install from CPAN. your darkPAN or a local CPAN mirror. Perl modules are then installed in /opt, giving you a nice clean seperation between your system perl+libraries and your application perl.
