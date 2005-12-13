Summary:	A Linux PXE (Preboot eXecution Environment) package
Summary(pl):	Implementacja PXE (Preboot eXecution Environment) dla Linuksa
Name:		pxe
Group:		Networking/Daemons
Version:	1.4.2
Release:	1
License:	GPL
Source0:	http://www.kano.org.uk/projects/pxe/%{name}-%{version}.tar.gz
# Source0-md5:	89dcb359a4c4fce475633dd771e77aa7
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-lockfile.patch
URL:		http://www.kano.org.uk/projects/pxe/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	pxeserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pxe package contains the PXE (Preboot eXecution Environment)
server.

%description -l pl
Pakiet pxe zawiera serwer PXE (Preboot eXecution Environment).

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
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pxe.conf
%attr(754,root,root) /etc/rc.d/init.d/pxe
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pxe
