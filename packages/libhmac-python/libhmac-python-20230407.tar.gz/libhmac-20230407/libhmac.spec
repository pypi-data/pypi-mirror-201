Name: libhmac
Version: 20230407
Release: 1
Summary: Library to support various Hash-based Message Authentication Codes (HMAC)
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libhmac
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  openssl 
BuildRequires: gcc  openssl-devel 

%description -n libhmac
Library to support various Hash-based Message Authentication Codes (HMAC)

%package -n libhmac-static
Summary: Library to support various Hash-based Message Authentication Codes (HMAC)
Group: Development/Libraries
Requires: libhmac = %{version}-%{release}

%description -n libhmac-static
Static library version of libhmac.

%package -n libhmac-devel
Summary: Header files and libraries for developing applications for libhmac
Group: Development/Libraries
Requires: libhmac = %{version}-%{release}

%description -n libhmac-devel
Header files and libraries for developing applications for libhmac.

%package -n libhmac-python3
Summary: Python 3 bindings for libhmac
Group: System Environment/Libraries
Requires: libhmac = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libhmac-python3
Python 3 bindings for libhmac

%package -n libhmac-tools
Summary: Several tools for calculating Hash-based Message Authentication Codes (HMAC)
Group: Applications/System
Requires: libhmac = %{version}-%{release}      
      

%description -n libhmac-tools
Several tools for calculating Hash-based Message Authentication Codes (HMAC)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libhmac
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libhmac-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libhmac-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libhmac.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libhmac-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libhmac-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Apr  8 2023 Joachim Metz <joachim.metz@gmail.com> 20230407-1
- Auto-generated

