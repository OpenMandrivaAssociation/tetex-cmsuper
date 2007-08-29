%define name            tetex-cmsuper
%define version         0.3.3
%define	texmfdir	%{_datadir}/texmf

Summary:	The CM-Super font set
Name:		%{name}
Version:	%{version}
Release:	%mkrel 8
License:	GPL
Group:		Publishing
Source0:	ftp://ftp.dante.de/pub/tex/fonts/ps-type1/cm-super.tar.bz2
BuildArch:	noarch
Requires(post): tetex >= 3.0
Requires(preun): tetex >= 3.0
Requires(postun): tetex >= 3.0
Requires:	tetex-dvips >= 3.0
Requires:	tetex-dvipdfm >= 3.0
Requires:	ghostscript
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The CM-Super package contains Type 1 fonts converted from METAFONT
fonts and covers entire EC/TC, ECC and LH fonts (Computer Modern font
families). All European and Cyrillic writings are covered. Each Type 1
font program contains ALL glyphs from the following standard LaTeX
font encodings: T1, TS1, T2A, T2B, T2C, X2, and also Adobe
StandardEncoding (585 glyphs per non-SC font and 468 glyphs per SC
font), and could be reencoded to any of these encodings using standard
dvips or pdftex facilities (the corresponding support files are also
included).

%prep
%setup -q -n cm-super

%build
gzip -d afm/*.afm.gz

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{texmfdir}/fonts/{afm,type1}/public/cm-super \
	$RPM_BUILD_ROOT%{texmfdir}/fonts/enc/dvips/cm-super \
	$RPM_BUILD_ROOT%{texmfdir}/fonts/map/dvips/cm-super \
	$RPM_BUILD_ROOT%{_bindir}
 
install -m 644 pfb/*.pfb \
	$RPM_BUILD_ROOT%{texmfdir}/fonts/type1/public/cm-super

install -m 644 afm/*.afm \
	$RPM_BUILD_ROOT%{texmfdir}/fonts/afm/public/cm-super

install -m 644 dvips/*.enc $RPM_BUILD_ROOT%{texmfdir}/fonts/enc/dvips/cm-super
install -m 644 dvips/*.map $RPM_BUILD_ROOT%{texmfdir}/fonts/map/dvips/cm-super

cat > $RPM_BUILD_ROOT%{_bindir}/tetex-addfonts-cmsuper <<EOF
#!/bin/sh
if [ -x %_bindir/updmap-sys ]; then
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t1.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t1.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-ts1.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t2a.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t2b.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t2c.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-x2.map
fi
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/tetex-removefonts-cmsuper <<EOF
#!/bin/sh
%_bindir/updmap-sys --quiet --disable cm-super-t1.map
%_bindir/updmap-sys --quiet --disable cm-super-t1.map
%_bindir/updmap-sys --quiet --disable cm-super-ts1.map
%_bindir/updmap-sys --quiet --disable cm-super-t2a.map
%_bindir/updmap-sys --quiet --disable cm-super-t2b.map
%_bindir/updmap-sys --quiet --disable cm-super-t2c.map
%_bindir/updmap-sys --quiet --disable cm-super-x2.map
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
if [ -x %_bindir/updmap-sys ]; then
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t1.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t1.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-ts1.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t2a.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t2b.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-t2c.map
	%_bindir/updmap-sys --quiet --enable Map=cm-super-x2.map
fi
exit 0

%preun
if [ "$1" = "0" ]; then
	%_bindir/updmap-sys --quiet --disable cm-super-t1.map
	%_bindir/updmap-sys --quiet --disable cm-super-t1.map
	%_bindir/updmap-sys --quiet --disable cm-super-ts1.map
	%_bindir/updmap-sys --quiet --disable cm-super-t2a.map
	%_bindir/updmap-sys --quiet --disable cm-super-t2b.map
	%_bindir/updmap-sys --quiet --disable cm-super-t2c.map
	%_bindir/updmap-sys --quiet --disable cm-super-x2.map
fi
exit 0

%postun
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%triggerin -- tetex
if [ "$2" -ge 1 ]; then
	if [ -x %_bindir/updmap-sys ]; then
		%_bindir/updmap-sys --quiet
	fi
fi
exit 0

%triggerpostun -- tetex
if [ "$2" -ge 1 ]; then
	if [ -x %_bindir/updmap-sys ]; then
		%_bindir/updmap-sys --quiet
	fi
fi
exit 0

%files
%defattr(-,root,root)
%doc ChangeLog COPYING FAQ INSTALL README TODO
%attr(755,root,root) %{_bindir}/*
%{texmfdir}/fonts/enc/dvips/cm-super/*
%{texmfdir}/fonts/map/dvips/cm-super/*
%{texmfdir}/fonts/afm/public/cm-super/*.afm
%{texmfdir}/fonts/type1/public/cm-super/*.pfb
