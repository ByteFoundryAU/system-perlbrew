%define installdir /opt/perlbrew
Name: perlbrew
Summary: perlbrew is an admin-free perl installation management tool.
Version: 0.78
Release: 2%{?dist}
License: MIT
Group: Development/Tools
BuildArch: noarch
URL: http://perlbrew.pl
# We use the fatpacked version, and moosh it into an rpm installed to /opt/perlbrew
Source0: https://raw.githubusercontent.com/gugod/App-perlbrew/release-%{version}/perlbrew
Source1: https://raw.githubusercontent.com/miyagawa/cpanminus/master/cpanm
Source2: https://raw.githubusercontent.com/gugod/patchperl-packing/master/patchperl
AutoReqProv: no
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
perlbrew is an admin-free perl installation management tool. This is a highly OIE specific install and wont play nicely with the fedora/epel release

%prep
cp -p %SOURCE0 .
cp -p %SOURCE1 .
cp -p %SOURCE2 .
chmod +x perlbrew patchperl cpanm

%build

%install
PERLBREW_ROOT=%{buildroot}%{installdir} /usr/bin/perl %{_builddir}/perlbrew self-install
cp patchperl cpanm %{buildroot}%{installdir}/bin/

# fix up the PERLBREW_ROOT
/usr/bin/perl -pi -e 's{PERLBREW_ROOT=.*}{PERLBREW_ROOT="%{installdir}"}' %{buildroot}%{installdir}/etc/bashrc
/usr/bin/perl -pi -e 's{PERLBREW_HOME=.*}{PERLBREW_HOME="%{installdir}/home"}' %{buildroot}%{installdir}/etc/bashrc

%clean
rm -rf %{buildroot}

%files
%{installdir}/bin/*
%{installdir}/etc/*
%dir %{installdir}/build
%dir %{installdir}/dists
%dir %{installdir}/perls
%defattr(-,root,root,-)


%changelog
* Thu Feb 23 2017 Dean Hamstead <dean@bytefoundry.com.au> - 0.78-2
- Fix PERLBREW_HOME
* Thu Feb 16 2017 Dean Hamstead <dean@bytefoundry.com.au> - 0.78-1
- Make it work for 0.78
- Simulate install-cpanm and install-patchperl
* Tue Jan 05 2016 Dean Hamstead <dean@bytefoundry.com.au> - 0.74.1-4
- Fixed up PERLBREW_HOME in bashrc
* Tue Jan 05 2016 Dean Hamstead <dean@bytefoundry.com.au> - 0.74.1-3
- Fixed up PERLBREW_HOME perlbrew itself
* Tue Jan 05 2016 Dean Hamstead <dean@bytefoundry.com.au> - 0.74.1-2
- Includes minor fix to my pull request mentioned in 0.74.1-1
* Mon Jan 04 2016 Dean Hamstead <dean@bytefoundry.com.au> - 0.74.1-1
- 0.74.1 version based upon my DISTDIR patches, see https://github.com/gugod/App-perlbrew/pull/497/files
* Fri Jun 19 2015 Brendan Beveridge <brendan@nodeintegration.com.au> - 0.73-1
- Initial creation

