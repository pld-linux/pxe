Name:		pxe
Summary:	A Linux PXE (Preboot eXecution Environment) package
Summary(pl):	Pakiet z implementacj± PXE (Preboot eXecution Environment) dla linuksa
Group:		Networking/Daemons
Version:	1.4.1
Release:	1
License:	GPL
Source0:	http://www.kano.org.uk/projects/pxe/%{name}-%{version}.tar.gz
# Source0-md5:	f438ee1e394540340c00aaa035aecf0b
Source1: 	%{name}.init
Source2: 	%{name}.sysconfig
Patch0:		%{name}-lockfile.patch
Provides:	pxeserver
URL:		http://www.kano.org.uk/projects/pxe/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pxe package contains the PXE (Preboot eXecution Environment)
server.

%description -l pl
Pakiet pxe zawiera serwer PXE(Preboot eXecution Environment).

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-log=/var/log/pxe.log \
	--with-lockfile=/var/run/pxe.pid \
	--with-setuid=daemon
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/{rc.d/init.d,sysconfig}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pxe
if [ -f /var/lock/subsys/pxe ]; then
	/etc/rc.d/init.d/pxe restart >&2
else
	echo "Run \"/etc/rc.d/init.d/pxe start\" to start pxe daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/pxe ]; then
		/etc/rc.d/init.d/pxe stop >&2
	fi
	/sbin/chkconfig --del pxe
fi

%files
%defattr(644,root,root,755)
%doc README LICENCE INSTALL Changes
%attr(755,root,root) %{_sbindir}/pxe
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/pxe.conf
%attr(754,root,root) /etc/rc.d/init.d/pxe
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/pxe
