# Necessary conditionals
%ifarch ppc64 s390 s390x sparc64 %{arm} alpha
%global SHARP  0
%else
%global SHARP  1
%endif

%ifarch %{ocaml_arches}
%global OCAML  1
%else
%global OCAML  0
%endif

%global DEVIL  1
%global ARRRR  1

# Build with QT applications (currently only gvedit)
# Disabled until the package gets better structuring, see bug #447133
%global QTAPPS 0

%global GTS    1
%global LASI   1

# Not in Fedora yet.
%global MING   0

%if 0%{?rhel}
%global SHARP  0
%global ARRRR  0
%global DEVIL  0
%global GTS    0
%global LASI   0
%endif

# Plugins version
%global pluginsver 6

%global php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
# Fix private-shared-object-provides
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$

# Fix for the 387 extended precision (rhbz#772637)
%ifarch i386 i686
%global FFSTORE -ffloat-store
%endif

Name:			graphviz
Summary:		Graph Visualization Tools
Version:		2.30.1
Release:		23%{?dist}
Group:			Applications/Multimedia
License:		EPL
URL:			http://www.graphviz.org/
Source0:		http://www.graphviz.org/pub/graphviz/ARCHIVE/%{name}-%{version}.tar.gz
Patch2:			graphviz-2.30.1-guile2-fix.patch
# Fix SIGSEGVs on testsuite (#645703).
Patch3:			graphviz-2.26.0-testsuite-sigsegv-fix.patch
# Testsuite now do diff check also in case of err output (#645703).
Patch4:			graphviz-2.26.0-rtest-errout-fix.patch
# Now that libgraph is gone, reflect that in libgvc.pc
Patch5:			graphviz-2.30.1-gvc.pc-no-libgraph.patch
# Lua 5.2
Patch6:			graphviz-2.30.1-lua-5.2.patch
# Accepted upstream, ticket #2302
Patch7:			graphviz-2.30.1-smyrna-doc-opt.patch
# Accepted upstream, ticket #2304
Patch8:			graphviz-2.30.1-gv2gml-options-fix.patch
# Sent upstream, ticket #2305
Patch9:			graphviz-2.30.1-lefty-help.patch
# Sent upstream, ticket #2306
Patch10:		graphviz-2.30.1-prune-help.patch
# Sent upstream, ticket #2307
Patch11:		graphviz-2.30.1-man-fix.patch
# Already in upstream
Patch12:		graphviz-2.32.0-aarch64.patch
# Upstream bug 0002387
Patch13:		graphviz-2.34.0-lefty-getaddrinfo.patch
# Fix yyerror overflow (CVE-2014-0978, CVE-2014-1235)
Patch14:		graphviz-2.30.1-CVE-2014-0978-CVE-2014-1235.patch
# Fix chknum overflow (CVE-2014-1236)
Patch15:		graphviz-2.30.1-CVE-2014-1236.patch
# Fix for ppc64le
Patch16:		graphviz-2.30.1-ppc64le-fix.patch
# Fix for OCaml 4.05
Patch17:		graphviz-2.30.1-ocaml-int64-fix.patch
# Backported from the upstream
Patch18:		graphviz-2.30.1-hard-syntax-errors.patch
# FTBFS fix due to ghostscript rebase which changed API
Patch19:		graphviz-2.30.1-ghostscript-build-fix.patch
# CVE-2020-18032
Patch20:		graphviz-2.30.1-CVE-2020-18032.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:		zlib-devel, libpng-devel, libjpeg-devel, expat-devel, freetype-devel >= 2
BuildRequires:		ksh, bison, m4, flex, tk-devel, tcl-devel >= 8.3, swig, ghostscript
BuildRequires:		fontconfig-devel, libtool-ltdl-devel, ruby-devel, ruby, guile-devel, python-devel
BuildRequires:		libXaw-devel, libSM-devel, libXext-devel, java-devel, php-devel
BuildRequires:		cairo-devel >= 1.1.10, pango-devel, gmp-devel, lua-devel, gtk2-devel, libgnomeui-devel
BuildRequires:		gd-devel, perl-devel, swig >= 1.3.33, automake, autoconf, libtool, qpdf
# Temporary workaound for perl(Carp) not pulled
BuildRequires:		perl-Carp
%if %{SHARP}
BuildRequires:		mono-core
%endif
%if %{DEVIL}
BuildRequires:		DevIL-devel
%endif
%if %{ARRRR}
BuildRequires:		R-devel
%endif
%if %{OCAML}
BuildRequires:		ocaml
%endif
%if %{QTAPPS}
BuildRequires:		qt-devel
%endif
%if %{GTS}
BuildRequires:		gts-devel
%endif
%if %{LASI}
BuildRequires:		lasi-devel
%endif
BuildRequires:		urw-fonts, perl-ExtUtils-Embed, ghostscript-devel, librsvg2-devel
Requires:		urw-fonts
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts).

%package devel
Group:			Development/Libraries
Summary:		Development package for graphviz
Requires:		%{name} = %{version}-%{release}, pkgconfig
Requires:		%{name}-gd = %{version}-%{release}

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts). This package contains development files for 
graphviz.

%if %{DEVIL}
%package devil
Group:			Applications/Multimedia
Summary:		Graphviz plugin for renderers based on DevIL
Requires:		%{name} = %{version}-%{release}

%description devil
Graphviz plugin for renderers based on DevIL. (Unless you absolutely have
to use BMP, TIF, or TGA, you are recommended to use the PNG format instead
supported directly by the cairo+pango based renderer in the base graphviz rpm.)
%endif

%package doc
Group:			Documentation
Summary:		PDF and HTML documents for graphviz

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%package gd
Group:			Applications/Multimedia
Summary:		Graphviz plugin for renderers based on gd
Requires:		%{name} = %{version}-%{release}
Requires(post):		%{_bindir}/dot /sbin/ldconfig
Requires(postun):	%{_bindir}/dot /sbin/ldconfig

%description gd
Graphviz plugin for renderers based on gd.  (Unless you absolutely have to use 
GIF, you are recommended to use the PNG format instead because of the better 
quality anti-aliased lines provided by the cairo+pango based renderer.)

%package graphs
Group:			Applications/Multimedia
Summary:		Demo graphs for graphviz

%description graphs
Some demo graphs for graphviz.

%package guile
Group:			Applications/Multimedia
Summary:		Guile extension for graphviz
Requires:		%{name} = %{version}-%{release}, guile

%description guile
Guile extension for graphviz.

%package java
Group:			Applications/Multimedia
Summary:		Java extension for graphviz
Requires:		%{name} = %{version}-%{release}

%description java
Java extension for graphviz.

%package lua
Group:			Applications/Multimedia
Summary:		Lua extension for graphviz
Requires:		%{name} = %{version}-%{release}, lua

%description lua
Lua extension for graphviz.

%if %{MING}
%package ming
Group:			Applications/Multimedia
Summary:		Graphviz plugin for flash renderer based on ming
Requires:		%{name} = %{version}-%{release}

%description ming
Graphviz plugin for -Tswf (flash) renderer based on ming.
%endif

%if %{OCAML}
%package ocaml
Group:			Applications/Multimedia
Summary:		Ocaml extension for graphviz
Requires:		%{name} = %{version}-%{release}, ocaml

%description ocaml
Ocaml extension for graphviz.
%endif

%package perl
Group:			Applications/Multimedia
Summary:		Perl extension for graphviz
Requires:		%{name} = %{version}-%{release}
Requires:		perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
Perl extension for graphviz.

%package php
Group:			Applications/Multimedia
Summary:		PHP extension for graphviz
Requires:		%{name} = %{version}-%{release}
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}

%description php
PHP extension for graphviz.

%package python
Group:			Applications/Multimedia
Summary:		Python extension for graphviz
Requires:		%{name} = %{version}-%{release}, python

%description python
Python extension for graphviz.

%if %{ARRRR}
%package R
Group:			Applications/Multimedia
Summary:		R extension for graphviz
Requires:		%{name} = %{version}-%{release}, R-core

%description R
R extension for graphviz.
%endif

%package ruby
Group:			Applications/Multimedia
Summary:		Ruby extension for graphviz
Requires:		%{name} = %{version}-%{release}, ruby

%description ruby
Ruby extension for graphviz.

%if %{SHARP}
%package sharp
Group:			Applications/Multimedia
Summary:		C# extension for graphviz
Requires:		%{name} = %{version}-%{release}, mono-core

%description sharp
C# extension for graphviz.
%endif

%package tcl
Group:			Applications/Multimedia
Summary:		Tcl extension & tools for graphviz
Requires:		%{name} = %{version}-%{release}, tcl >= 8.3, tk

%description tcl
Various tcl packages (extensions) for the graphviz tools.

%prep
%setup -q
%patch2 -p1 -b .guile2-fix
%patch3 -p1 -b .testsuite-sigsegv-fix
%patch4 -p1 -b .rtest-errout-fix
%patch5 -p1 -b .cgraph
%patch6 -p1 -b .lua-52
%patch7 -p1 -b .smyrna-doc-opt
%patch8 -p1 -b .gv2gml-options-fix
%patch9 -p1 -b .lefty-help
%patch10 -p1 -b .prune-help
%patch11 -p1 -b .man-fix
%patch12 -p1 -b .aarch64
%patch13 -p1 -b .lefty-getaddrinfo
%patch14 -p1 -b .CVE-2014-0978-CVE-2014-1235
%patch15 -p1 -b .CVE-2014-1236
%patch16 -p1 -b .ppc64le-fix
%patch17 -p1 -b .ocaml-int64-fix
%patch18 -p1 -b .hard-syntax-errors
%patch19 -p1 -b .ghostscript-build-fix
%patch20 -p1 -b .CVE-2020-18032

# Attempt to fix rpmlint warnings about executable sources
find -type f -regex '.*\.\(c\|h\)$' -exec chmod a-x {} ';'

%build
autoreconf -if
# Hack in the java includes we need
sed -i '/JavaVM.framework/!s/JAVA_INCLUDES=/JAVA_INCLUDES=\"_MY_JAVA_INCLUDES_\"/g' configure
sed -i 's|_MY_JAVA_INCLUDES_|-I%{java_home}/include/ -I%{java_home}/include/linux/|g' configure
# Rewrite config_ruby.rb to work with Ruby 1.9
sed -i 's|expand(|expand(Config::|' config/config_ruby.rb
sed -i 's|sitearchdir|vendorarchdir|' config/config_ruby.rb

# get the path to search for ruby/config.h to CPPFLAGS, so that configure can find it
export CPPFLAGS=-I`ruby -e "puts File.join(RbConfig::CONFIG['includedir'], RbConfig::CONFIG['sitearch'])" || echo /dev/null`
%configure --with-x --disable-static --disable-dependency-tracking --without-mylibgd --with-ipsepcola --with-pangocairo --with-gdk-pixbuf \
%if ! %{LASI}
	--without-lasi \
%endif
%if ! %{GTS}
	--without-gts \
%endif
%if ! %{SHARP}
	--disable-sharp \
%endif
%if ! %{OCAML}
	--disable-ocaml \
%endif
%if ! %{MING}
	--without-ming \
%endif
%if ! %{ARRRR}
	--disable-r \
%endif
%if ! %{DEVIL}
	--without-devil \
%endif
%if ! %{QTAPPS}
	--without-qt \
%endif

make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fno-strict-overflow %{?FFSTORE}" \
  CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fno-strict-overflow %{?FFSTORE}"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
	docdir=%{buildroot}%{_docdir}/%{name}-%{version} \
	pkgconfigdir=%{_libdir}/pkgconfig \
	install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
chmod -x %{buildroot}%{_datadir}/%{name}/lefty/*

# Move docs to the right place
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
mv %{buildroot}%{_datadir}/%{name}/doc/* %{buildroot}%{_docdir}/%{name}-%{version}

# Install README
install -m0644 README %{buildroot}%{_docdir}/%{name}-%{version}

# PHP configuration file
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini
; Enable %{name} extension module
extension=gv.so
__EOF__

# Remove executable modes from demos
find %{buildroot}%{_datadir}/%{name}/demo -type f -exec chmod a-x {} ';'

# Move demos to doc
mv %{buildroot}%{_datadir}/%{name}/demo %{buildroot}%{_docdir}/%{name}-%{version}/

# Rename python demos to prevent byte compilation
find %{buildroot}%{_docdir}/%{name}-%{version}/demo -type f -name "*.py" -exec mv {} {}.demo ';'

# Remove dot_builtins, on demand loading should be sufficient
rm -f %{buildroot}%{_bindir}/dot_builtins

# Remove metadata from generated PDFs
pushd %{buildroot}%{_docdir}/%{name}-%{version}/pdf
for f in prune lneato.1 lefty.1 gvgen.1 gc.1 dotty.1 dot.1 cluster.1
do
  if [ -f $f.pdf ]
  then
# ugly, but there is probably no better solution
    qpdf --empty --static-id --pages $f.pdf -- $f.pdf.$$
    mv -f $f.pdf.$$ $f.pdf
  fi
done

# Ghost plugins config
touch %{buildroot}%{_libdir}/graphviz/config%{pluginsver}

%check
# Minimal load test of php extension
LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
php --no-php-ini \
    --define extension_dir=%{buildroot}%{_libdir}/graphviz/php/ \
    --define extension=libgv_php.so \
    --modules | grep gv

# upstream test suite
cd rtest
make rtest

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%{_bindir}/dot -c

%postun
/sbin/ldconfig

%if %{DEVIL}
# run "dot -c" to generate plugin config in %%{_libdir}/graphviz/config*
%post devil
%{_bindir}/dot -c 2>/dev/null || :
/sbin/ldconfig

%postun devil
%{_bindir}/dot -c 2>/dev/null || :
/sbin/ldconfig
%endif

# run "dot -c" to generate plugin config in %%{_libdir}/graphviz/config*
%post gd
%{_bindir}/dot -c 2>/dev/null || :
/sbin/ldconfig

%postun gd
%{_bindir}/dot -c 2>/dev/null || :
/sbin/ldconfig

%if %{MING}
# run "dot -c" to generate plugin config in %%{_libdir}/graphviz/config*
%post ming
%{_bindir}/dot -c 2>/dev/null || :
/sbin/ldconfig

%postun ming
%{_bindir}/dot -c 2>/dev/null || :
/sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/*
%dir %{_libdir}/graphviz
%{_libdir}/*.so.*
%{_libdir}/graphviz/*.so.*
%{_mandir}/man1/*.1*
%{_mandir}/man7/*.7*
%dir %{_datadir}/graphviz
%exclude %{_docdir}/%{name}-%{version}/html
%exclude %{_docdir}/%{name}-%{version}/pdf
%exclude %{_docdir}/%{name}-%{version}/demo
%{_datadir}/graphviz/lefty
%{_datadir}/graphviz/gvpr
%ghost %{_libdir}/graphviz/config%{pluginsver}

%if %{QTAPPS}
%{_datadir}/graphviz/gvedit
%endif

%exclude %{_libdir}/graphviz/*/*
%exclude %{_libdir}/graphviz/libgvplugin_gd.*
%if %{DEVIL}
%exclude %{_libdir}/graphviz/libgvplugin_devil.*
%endif
%if %{MING}
%exclude %{_libdir}/graphviz/libgvplugin_ming.*
%exclude %{_libdir}/graphviz/*fdb
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/graphviz
%{_libdir}/*.so
%{_libdir}/graphviz/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3.gz

%if %{DEVIL}
%files devil
%defattr(-,root,root,-)
%{_libdir}/graphviz/libgvplugin_devil.so.*
%endif

%files doc
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/html
%doc %{_docdir}/%{name}-%{version}/pdf
%doc %{_docdir}/%{name}-%{version}/demo

%files gd
%defattr(-,root,root,-)
%{_libdir}/graphviz/libgvplugin_gd.so.*

%files graphs
%defattr(-,root,root,-)
%dir %{_datadir}/graphviz
%{_datadir}/graphviz/graphs

%files guile
%defattr(-,root,root,-)
%{_libdir}/graphviz/guile/
%{_mandir}/man3/gv.3guile*

%files java
%defattr(-,root,root,-)
%{_libdir}/graphviz/java/
%{_mandir}/man3/gv.3java*

%files lua
%defattr(-,root,root,-)
%{_libdir}/graphviz/lua/
%{_libdir}/lua*/*
%{_mandir}/man3/gv.3lua*

%if %{MING}
%files ming
%defattr(-,root,root,-)
%{_libdir}/graphviz/libgvplugin_ming.so.*
%{_libdir}/graphviz/*fdb
%endif

%if %{OCAML}
%files ocaml
%defattr(-,root,root,-)
%{_libdir}/graphviz/ocaml/
%{_mandir}/man3/gv.3ocaml*
%endif

%files perl
%defattr(-,root,root,-)
%{_libdir}/graphviz/perl/
%{_libdir}/perl*/*
%{_mandir}/man3/gv.3perl*

%files php
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
%{_libdir}/graphviz/php/
%{php_extdir}/gv.so
%{_datadir}/php*/*
%{_mandir}/man3/gv.3php*

%files python
%defattr(-,root,root,-)
%{_libdir}/graphviz/python/
%{_libdir}/python*/*
%{_mandir}/man3/gv.3python*

%if %{ARRRR}
%files R
%defattr(-,root,root,-)
%{_libdir}/graphviz/R/
%{_mandir}/man3/gv.3r.gz
%endif

%files ruby
%defattr(-,root,root,-)
%{_libdir}/graphviz/ruby/
%{_libdir}/*ruby*/*
%{_mandir}/man3/gv.3ruby*

%if %{SHARP}
%files sharp
%defattr(-,root,root,-)
%{_libdir}/graphviz/sharp/
%{_mandir}/man3/gv.3sharp*
%endif

%files tcl
%defattr(-,root,root,-)
%{_libdir}/graphviz/tcl/
%{_libdir}/tcl*/*
# hack to include gv.3tcl only if available
#  always includes tcldot.3tcl, gdtclft.3tcl
%{_mandir}/man3/*.3tcl*
%{_mandir}/man3/tkspline.3tk*


%changelog
* Thu Jul 12 2021 Corentin Labbe <clabbe@baylibre.com> - 2.30.1-23
- Fixed buffer overflow in lib/common/shapes.c
  Resolves: CVE-2020-18032

* Tue Mar  3 2020 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-22
- Made syntax errors hard
  Resolves: rhbz#1679097
- Fixed FTBFS due to ghostscript rebase

* Sat Sep 16 2017 Richard W.M. Jones <rjones@redhat.com> - 2.30.1-21
- Rebuild for OCaml 4.05.0
  resolves: rhbz#1447982

* Thu Aug 31 2017 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-20
- Rebuilt for enabling ocaml binding on aarch64 and ppc64l
  Resolves: rhbz#1378657

* Wed Aug 20 2014 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-19
- Fixed build on ppc64le and other ppc64 variants (lua bindings)
  Resolves: rhbz#1125538

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.30.1-18
- Mass rebuild 2014-01-24

* Fri Jan 10 2014 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-17
- Prevent possible buffer overflow in yyerror()
  Resolves: CVE-2014-1235
- Fix possible buffer overflow problem in chkNum of scanner
  Resolves: CVE-2014-1236

* Tue Jan  7 2014 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-16
- Fixed overflow in yyerror
  Resolves: CVE-2014-0978

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.30.1-15
- Mass rebuild 2013-12-27

* Thu Oct 31 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-14
- Removed metadata from generated PDFs
  Related: rhbz#881173

* Thu Oct 31 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-13
- Fixed multilib conflicts
  Rewrote lefty IO lib to use getaddrinfo instead of gethostbyname
  (by lefty-getaddrinfo patch)
  Resolves: rhbz#881173

* Tue Oct 29 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-12
- Fixed build on aarch64
  Resolves: rhbz#1023792

* Fri Aug 30 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-11
- Rebuild due to php macros change
  Resolves: rhbz#1002865

* Fri Jul 12 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-10
- Various man and built-in help fixes

* Tue Jun 25 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-9
- Fixed handling of the libdir/graphviz directory

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.30.1-8
- rebuild for new GD 2.1.0

* Wed May 15 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-7
- rebuild for lua 5.2

* Tue Apr 23 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-6
- patch libgvc.pc.in to refer to -lcgraph (-lgraph is dead and gone)

* Thu Apr 11 2013 Tom Callaway <spot@fedoraproject.org> - 2.30.1-5
- rebuild for R3 (may not be needed, but better safe than sorry)

* Mon Mar 25 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-4
- Added support for aarch64
  Resolves: rhbz#925487

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 2.30.1-3
- rebuild for http://fedoraproject.org/wiki/Features/Php55
- add explicit BuildRequires: perl-Carp (workaround)

* Thu Mar 14 2013 V??t Ondruch <vondruch@redhat.com> - 2.30.1-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Fri Feb 15 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.1-1
- New version
  Resolves: rhbz#911520
  Resolves: rhbz#704529

* Thu Jan 24 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.0-3
- Used ocaml_arches macros to enable ocaml on supported arches

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.30.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Mon Jan 14 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.30.0-1
- New version
  Resolves: rhbz#895027
- Dropped guile-detect, ocaml4 patches (not needed)
- Fixed bogus date in changelog (guessing)

* Wed Jan  9 2013 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-26
- Rebuilt with -fno-strict-overflow to workaround the overflow problem
  (upstream ticket: http://www.graphviz.org/mantisbt/view.php?id=2244)
- The dot_builtins was removed rather then excluded to fix the dangling
  symlinks problem in debuginfo

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.28.0-25
- rebuild against new libjpeg

* Wed Oct 17 2012 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-24
- Rebuilt for new ocaml

* Fri Aug 17 2012 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-23
- Silenced 'dot -c' errors/warnings in post/postun
- Do not remove dot config in plugins post/postun

* Fri Aug 17 2012 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-22
- dot_builtins no longer installed (lowers implicit deps)
- Fixed post/postuns for plugins
- Removed -ffast-math, added -ffloat-store (on i386) to fix arithmetic on i386

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 2.28.0-20
- Perl 5.16 rebuild

* Sat Jun  9 2012 Richard W.M. Jones <rjones@redhat.com> - 2.28.0-19
- Rebuild for OCaml 4.00.0.
- Enable OCaml on arm and ppc64, since there are working native compilers
  for both.

* Wed May 23 2012 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-18
- Improved docs handling code in spec to be backward compatible with older RPM

* Tue May 22 2012 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-17
- All docs are now installed into /usr/share/doc/graphviz-%%{version}
- Demos packaged as docs not to automatically bring in unnecessary deps

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-16
- Rebuilt for c++ ABI breakage

* Thu Feb 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.28.0-15
- fix CPPFLAGS export so it doesn't cause issues on ARM

* Mon Feb 06 2012 V??t Ondruch <vondruch@redhat.com> - 2.28.0-14
- Rebuilt for Ruby 1.9.3.

* Wed Jan 18 2012 Remi Collet <remi@fedoraproject.org> - 2.28.0-13
- build against php 5.4.0
- add filter to fix private-shared-object-provides
- add %%check for php extension

* Sun Jan 08 2012 Richard W.M. Jones <rjones@redhat.com> - 2.28.0-12
- Rebuild for OCaml 3.12.1.

* Thu Dec  8 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-11
- Added conditionals for ARRRR, DEVIL, QTAPPS (gvedit), GTS, LASI
- Fixed conditionals for SHARP, OCAML
- Built with gts, ghostscript, rsvg and lasi
  Resolves: rhbz#760926
- Disabled gvedit
  Resolves: rhbz#751807
- Fixed rpmlint warnings about executable sources

* Wed Nov  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.28.0-10
- rebuild for R 2.14.0

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.28.0-9
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.28.0-8
- Perl mass rebuild

* Thu Jul 07 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-7
- Added gd as devel requirement

* Fri Jun 17 2011 Marcela Ma??l????ov?? <mmaslano@redhat.com> - 2.28.0-6
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Ma??l????ov?? <mmaslano@redhat.com> - 2.28.0-5
- Perl 5.14 mass rebuild

* Thu May 19 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-4
- Fixed detection of guile 2.x
  Resolves: rhbz#704529

* Fri May 13 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-3
- Corrected license tag, the graphviz license is now EPL

* Fri May 13 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-2
- Recompiled with -fno-strict-aliasing in CXXFLAGS

* Tue May 10 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.28.0-1
- New version 2.28.0
- Added perl-ExtUtils-Embed to BuildRequires, it is now required
- Fixed build failure due to change in php_zend_api macro type
- Removed sparc64, gtk-progname, doc-index-fix, ppc-darwinhack
  patches (all were upstreamed)

* Thu Mar 03 2011 Oliver Falk <oliver@linux-kernel.at> - 2.26.3-5
- Disable mono and ocaml on alpha

* Tue Feb 22 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.26.3-4
- Added urw-fonts to requires (#677114)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Karsten Hopp <karsten@redhat.com> 2.26.3-2
- fix hack for powerpc-darwin8 in configure

* Thu Jan 06 2011 Jaroslav ??karvada <jskarvad@redhat.com> - 2.26.3-1
- New version (#580017)
- Fixed gtk plugin program-name (#640671, gtk-progname patch)
- Fixed broken links in doc index (#642536, doc-index-fix patch)
- Fixed SIGSEGVs on testsuite (#645703, testsuite-sigsegv-fix patch)
- Testsuite now do diff check also in case of err output (#645703,
  rtest-errout-fix patch)
- Testsuite enabled on all arches (#645703)
- Added urw-fonts to BuildRequires
- Compiled with -fno-strict-aliasing
- Fixed rpmlint warnings on spec file
- Removed unused patches

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.26.0-3
- Mass rebuild with perl-5.12.0

* Mon Jan 04 2010 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.26.0-2
- Rebuild for updated ocaml
- Happy new year, Fedora!

* Fri Dec 18 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.26.0-1
- Updated to latest release
- Removed patches that have been applied upstream
- Fixed man page paths (mann -> man3)
- Disabled mono and ocaml for ARM (Jitesh Shah, BZ#532047)
- Disabled regression tests on sparc64 as well as ppc/ppc64 (Dennis Gilmore)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.3-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 2.20.3-4.1
- fix mistake in make rtest fix

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 2.20.3-4
- rebuild for new PHP 5.3.0 ABI (20090626)
- add PHP ABI check
- use php_extdir (and don't own it)
- add php configuration file (/etc/php.d/graphviz.ini)

* Mon Mar  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.20.3-3
- this spec makes baby animals cry... massively clean it up
- hack in java includes to build against openjdk
- add ruby as a BuildRequires (configure checks for /usr/bin/ruby)

* Wed Feb 25 2009 John Ellson <ellson@graphviz.org> 2.20.3-2.2
- fixes for swig changes

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.3-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Karsten Hopp <karsten@redhat.com> 2.20.3-.2
- make it build on s390, s390x (#469044)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.20.3-1.1
- Rebuild for Python 2.6

* Mon Nov 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.20.3-1
- update to 2.20.3

* Sat Nov 22 2008 Rex Dieter <rdieter@fedoraproject.org> 2.16.1-0.7
- respin (libtool)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.16.1-0.6
- fix conditional comparison

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.16.1-0.5
- add Requires for versioned perl (libperl.so)

* Tue Mar 04 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16.1-0.4
- Disable R support

* Mon Mar 03 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16.1-0.2
- New upstream release (fixes BZ#433205, BZ#427376)
- Merged spec changes in from upstream
- Added patch from BZ#432683

* Tue Feb 12 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-3.3
- Added upstream-provided patch for building under GCC 4.3 (thanks John!)

* Thu Jan  3 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-3.2
- Re-added tcl/tk 8.5 patch
- Tweaked ming stuff

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject.org> - 2.16-3.1
- Rebuild against new Tcl 8.5

* Wed Dec 12 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-2
- What the heck?  Can't BR stuff that hasn't even gotten reviewed yet.

* Wed Nov 28 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.16-1
- New upstream release
- Remove arith.h patch

* Tue Sep 04 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.14.1-3
- Patch to resurrect arith.h

* Thu Aug 23 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 2.14.1-2
- Added perl-devel to BR for F7+

* Wed Aug 15 2007 John Ellson <ellson@research.att.com>
- release 2.14.1 - see ChangeLog for details
* Thu Aug 2 2007 John Ellson <ellson@research.att.com>
- release 2.14 - see ChangeLog for details
* Fri Mar 16 2007 Stephen North <north@research.att.com>
- remove xorg-X11-devel from rhel >= 5
* Mon Dec 11 2006 John Ellson <john.ellson@comcast.net>
- fix graphviz-lua description (Fedora BZ#218191)
* Tue Sep 13 2005 John Ellson <ellson@research.att.com>
- split out language bindings into their own rpms so that 
  main rpm doesn't depend on (e.g.) ocaml

* Sat Aug 13 2005 John Ellson <ellson@research.att.com>
- imported various fixes from the Fedora-Extras .spec by Oliver Falk <oliver@linux-kernel.at>

* Wed Jul 20 2005 John Ellson <ellson@research.att.com>
- release 2.4
