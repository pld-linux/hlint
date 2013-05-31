Summary:	Haskell Source code suggestions
Name:		hlint
Version:	1.8.45
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/hlint/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a317df7355d572b2aaa7402a76760725
URL:		http://community.haskell.org/~ndm/hlint/
BuildRequires:	cpphs
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-haskell-src-exts
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
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%attr(755,root,root) %{_bindir}/hlint
%{_libdir}/%{ghcdir}/package.conf.d/%{name}.conf
%{_libdir}/%{ghcdir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}
