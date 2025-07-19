#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	th-abstraction
Summary:	Nicer interface for reified information about data types
Summary(pl.UTF-8):	Ładniejszy interfejs do zreifikowanych informacji o typach danych
Name:		ghc-%{pkgname}
Version:	0.3.2.0
Release:	2
License:	BSD-Like
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/th-abstraction
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	3625dd90af376cb3fedb8acc3feaf02d
URL:		http://hackage.haskell.org/package/th-abstraction
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.3
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-containers >= 0.4
BuildRequires:	ghc-containers < 0.7
BuildRequires:	ghc-ghc-prim
BuildRequires:	ghc-template-haskell >= 2.5
BuildRequires:	ghc-template-haskell < 2.17
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.3
BuildRequires:	ghc-containers-prof >= 0.4
BuildRequires:	ghc-ghc-prim-prof
BuildRequires:	ghc-template-haskell-prof >= 2.5
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.3
Requires:	ghc-containers >= 0.4
Requires:	ghc-ghc-prim
Requires:	ghc-template-haskell >= 2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This package normalizes variations in the interface for inspecting
datatype information via Template Haskell so that packages and support
a single, easier to use informational datatype while supporting many
versions of Template Haskell.

%description -l pl.UTF-8
Ten pakiet normalizuje warianty inrerfejsu do badania informacji o
typach danych poprzez Template Haskell, dzięki czemu pakiety mogą
obsługiwać jeden, prostszy w użyciu typ danych informacyjnych,
obsługując jednocześnie wiele wersji Template Haskell.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-containers-prof >= 0.4
Requires:	ghc-ghc-prim-prof
Requires:	ghc-template-haskell-prof >= 2.4

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md LICENSE README.md
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-abstraction-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-abstraction-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-abstraction-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Datatype
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Datatype/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Datatype/*.dyn_hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-abstraction-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Datatype/*.p_hi
