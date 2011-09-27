Summary:	Haskell Source code suggestions
Name:		hlint
Version:	1.8.15
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/hlint/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4ce291cb13ff410bff8f1b9adb9f8a34
Patch0:		%{name}-deps.patch
URL:		http://community.haskell.org/~ndm/hlint/
BuildRequires:	cpphs
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-haskell-src-exts
BuildRequires:	ghc-transformers
BuildRequires:	ghc-uniplate
BuildRequires:	hscolour
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
HLint gives suggestions on how to improve your source code.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
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
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hlint
%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf
%{_libdir}/%{ghcdir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
