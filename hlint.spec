Summary:	Haskell Source code suggestions
Name:		hlint
Version:	1.9.36
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/hlint/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3953cd1ed8c193c11e54e549832b795d
URL:		http://community.haskell.org/~ndm/hlint/
BuildRequires:	cpphs >= 1.20.1
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-ansi-terminal >= 0.6.2
BuildRequires:	ghc-cmdargs >= 0.10
BuildRequires:	ghc-extra >= 1.4.9
BuildRequires:	ghc-haskell-src-exts >= 1.18.0
BuildRequires:	ghc-refact >= 0.3
BuildRequires:	ghc-transformers
BuildRequires:	ghc-uniplate
BuildRequires:	hscolour
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Obsoletes:	hlint-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
HLint gives suggestions on how to improve your source code.

%prep
%setup -q

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

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
