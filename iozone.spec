%define f_ver %(echo %{version} | tr '.' '_')

Summary: Filesystem benchmarking utility
Name: iozone
Version: 3.492
Release: 1%{?dist}
License: Distributable, no modification permitted and Public Domain
URL: http://www.iozone.org
Source0: http://www.iozone.org/src/current/iozone%{f_ver}.tgz
Recommends: gnuplot
BuildRequires: dos2unix
BuildRequires: gcc
BuildRequires: make
BuildRequires: sed

%description
IOzone is a filesystem benchmark tool. The benchmark generates and 
measures a variety of file operations. Iozone has been ported to 
many machines and runs under many operating systems.

Iozone is useful for performing a broad filesystem analysis of a vendors
computer platform. The benchmark tests file I/O performance for the following
operations: Read, write, re-read, re-write, read backwards, read strided,
fread, fwrite, random read, pread, mmap, aio_read, aio_write.

%prep
%setup -q -n iozone%{f_ver}
chmod 644 docs/IOzone_msword_98.pdf
chmod 644 docs/Run_rules.doc
pushd src/current
sed -i -e '1i #!/bin/sh' Generate_Graphs
chmod 755 Generate_Graphs
chmod 644 Gnuplot.txt
dos2unix -k iozone_visualizer.pl
iconv -f iso8859-1 -t utf-8 iozone_visualizer.pl > iozone_visualizer.pl.u8 && \
touch -r iozone_visualizer.pl iozone_visualizer.pl.u8 && \
mv iozone_visualizer.pl.u8 iozone_visualizer.pl
popd

%build
%set_build_flags
export CFLAGS="$CFLAGS -DHAVE_PREADV -DHAVE_PWRITEV -fPIE -Wno-unused-but-set-variable"
pushd src/current
%make_build linux
popd

%install
install -dm755 %{buildroot}%{_bindir}
install -dm755 %{buildroot}%{_mandir}/man1

install -p -m755 src/current/iozone %{buildroot}%{_bindir}
install -p -m755 src/current/iozone_visualizer.pl %{buildroot}%{_bindir}
install -p -m755 src/current/fileop %{buildroot}%{_bindir}/iozone_fileop
install -p -m755 src/current/Generate_Graphs %{buildroot}%{_bindir}/iozone_Generate_Graphs
install -p -m755 src/current/gengnuplot.sh %{buildroot}%{_bindir}/iozone_gengnuplot.sh
install -p -m755 src/current/pit_server %{buildroot}%{_bindir}
install -p -m644 docs/iozone.1 %{buildroot}/%{_mandir}/man1/

%files
%license docs/License.txt
%doc docs/IOzone_msword_98.pdf
%doc docs/Run_rules.doc
%doc src/current/Gnuplot.txt
%{_bindir}/iozone
%{_bindir}/iozone_visualizer.pl
%{_bindir}/iozone_fileop
%{_bindir}/iozone_Generate_Graphs
%{_bindir}/iozone_gengnuplot.sh
%{_bindir}/pit_server
%{_mandir}/man1/iozone.1*

%changelog
* Wed Jun 30 2021 Dominik Mierzejewski <rpm@greysector.net> - 3.492-1
- update to 3_492

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.491-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Dominik Mierzejewski <rpm@greysector.net> - 3.491-1
- update to 3_491
- drop upstreamed patch
- add missing shebang line to Generate_Graphs script
- use make_build macro
- prefix generic-named binaries with iozone_

* Mon Nov 02 2020 Dominik Mierzejewski <rpm@greysector.net> - 3.490-1
- update to 3_490
- modernize spec
- drop duplicate doc file

* Fri May 27 2005 Neil Horman <nhorman@redhat.com>
- cleaned up spec file
- packaged for Fedora Extras
