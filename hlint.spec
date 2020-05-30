Summary:	Haskell Source code suggestions
Name:		hlint
Version:	3.1.3
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/hlint/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4626b8e4333462c29cdd565c789d2220
URL:		http://hackage.haskell.org/package/hlint
BuildRequires:	cpphs >= 1.20.1
BuildRequires:	ghc >= 8.10.0
BuildRequires:	hscolour >= 1.21
BuildRequires:	ghc-aeson >= 1.1.2.0
BuildRequires:	ghc-ansi-terminal >= 0.6.2
BuildRequires:	ghc-base
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-cmdargs >= 0.10
BuildRequires:	ghc-containers
BuildRequires:	ghc-data-default >= 0.3
BuildRequires:	ghc-directory
BuildRequires:	ghc-extra >= 1.7.1
BuildRequires:	ghc-file-embed
BuildRequires:	ghc-filepath
BuildRequires:	ghc-filepattern >= 0.1.1
BuildRequires:	ghc-ghc-lib-parser-ex >= 8.10.0.11
BuildRequires:	ghc-process
BuildRequires:	ghc-refact >= 0.3
BuildRequires:	ghc-text
BuildRequires:	ghc-transformers
BuildRequires:	ghc-uniplate >= 1.5
BuildRequires:	ghc-unordered-containers
BuildRequires:	ghc-utf8-string
BuildRequires:	ghc-vector
BuildRequires:	ghc-yaml >= 0.5.0
BuildRequires:	rpmbuild(macros) >= 1.608
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
