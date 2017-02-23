%define installdir /opt/perlbrew/perls/perl-5.22.0
%global __os_install_post %{nil}
Name: perlbrew-perl-5.22.0
Summary: perlbrew is an admin-free perl installation management tool.
Version: 1.0
Release: 6%{?dist}
License: (GPL+ or Artistic) and (GPLv2+ or Artistic) and Copyright Only and MIT and Public Domain and UCD
Group: Development/Tools
URL: http://perlbrew.pl
Source0: http://www.cpan.org/src/5.0/perl-5.22.0.tar.bz2
AutoReqProv: no

Requires: perlbrew
BuildRequires: perlbrew

# taken from perl.spec
BuildRequires:  dos2unix, man, groff
BuildRequires:  gdbm-devel, db4-devel, bzip2-devel, zlib-devel
BuildRequires:  bison
BuildRequires:  procps, rsyslog

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
perl 5.22.0 x86_64 for perlbrew

%prep
# We dont need to extract anything %setup -q
# Just do this so we can see it in the build logs
/opt/perlbrew/bin/perlbrew env
echo %{buildroot}

# this is hack land from here on in...
# hack perlbrew to use the build directory for building, as the 'mockbuild' user has no access to /opt/perlbrew/build
mkdir -p /builddir/build/BUILD/bin
mkdir -p /builddir/build/BUILD/build
cp /opt/perlbrew/bin/* /builddir/build/BUILD/bin/
sed -i 's!my\$extract_command="cd @{\[ $self->root \]}/build; \$tarx \$dist_tarball";!my\$extract_command="cd /builddir/build/BUILD/build; \$tarx \$dist_tarball";!' /builddir/build/BUILD/bin/perlbrew
sed -i 's#my\$extracted_dir="@{\[ $self->root \]}/build/$dist_tarball_basename";#my $extracted_dir="/builddir/build/BUILD/build/$dist_tarball_basename";#' /builddir/build/BUILD/bin/perlbrew
sed -i 's|\$self->{log_file}=joinpath(\$self->root,"build.\${installation_name}\${variation}\${append}.log");|\$self->{log_file}=joinpath("/builddir/build/BUILD/","build.\${installation_name}\${variation}\${append}.log");|' /builddir/build/BUILD/bin/perlbrew

%build
# nothing, build and install in 'install'

%install
# This is a merging of the rhel7 and debian build options, with 64int up'd to 64all
# --notest because something is failing, -j 4 has it run stuff in parrallel
/builddir/build/BUILD/bin/perlbrew install --multi --thread --64all --debug -j 4 --verbose --notest \
 -Duselargefiles \
 -Duseithreads \
 -Duse64bitint \
 -D_FORTIFY_SOURCE=2  \
 -Doptimize="$RPM_OPT_FLAGS" \
 -Dmyhostname=localhost \
 -Dperladmin=root@localhost \
 -Duseperlio  \
 -Dpager=/usr/bin/less \
 -Dd_gethostent_r_proto  \
 -Di_db \
 -Di_shadow \
 -Di_syslog \
 -Dd_semctl_semun \
 -Di_gdbm  \
 -Ui_ndbm  \
 -Uafs  \
 -Ud_csh  \
 -Ud_ualarm  \
 -Uusesfio \
 -Uusenm  \
 -Ui_libutil  \
 -Uversiononly  \
 -Ubincompat5005  \
 -Ud_endhostent_r_proto  \
 -Ud_sethostent_r_proto  \
 -Ud_endprotoent_r_proto  \
 -Ud_setprotoent_r_proto  \
 -Ud_endservent_r_proto  \
 -Ud_setservent_r_proto \
 --destdir=%{buildroot} \
%{_sourcedir}/perl-5.22.0.tar.bz2

# 'install' deletes .version, this creates it again. why? nfi
echo "5.022000" > %{buildroot}%{installdir}/.version

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{installdir}/.version
%{installdir}/bin/*
%{installdir}/lib/*
%{installdir}/man/*


%changelog
* Mon Jan 04 2016 Dean Hamstead <dean@bytefoundry.com.au> - 1.0-6
- Uses optimize from variables, myhostname and perladmin are defined
* Mon Jan 04 2016 Dean Hamstead <dean@bytefoundry.com.au> - 1.0-5
- Uses --destdir which i just added to perlbrew
* Wed Nov 11 2015 Dean Hamstead <dean@bytefoundry.com.au> - 1.0-4
- removed "-Duseshrplib" as perlbrew doesnt seem to work right with shared libraries
- Striping gets caught up on libperl.a, disable it via os_install_post=nil
* Tue Nov 03 2015 Dean Hamstead <dean@bytefoundry.com.au> - 1.0-3
- Try to make things go full auto
- Its still a hack-o-thon though
* Fri Jul 17 2015 Brendan Beveridge <brendan@nodeintegration.com.au> - 1.0-2
- Add missing carton bundle
* Fri Jun 19 2015 Brendan Beveridge <brendan@nodeintegration.com.au> - 1.0-1
- Initial creation
