Summary:	ParMETIS - Parallel Graph Partitioning and Fill-reducing Matrix Ordering
Summary(pl.UTF-8):	ParMETIS - równoległy podział grafu i tworzenie porządków redukujący macierzy
Name:		parmetis
Version:	4.0.3
Release:	1
License:	non-profit or evaluation use
Group:		Libraries
#Source0Download: http://glaros.dtc.umn.edu/gkhome/metis/parmetis/download
Source0:	http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/%{name}-%{version}.tar.gz
# NoSource0-md5:	f69c479586bf6bb7aff6a9bc0c739628
Patch0:		%{name}-cmake.patch
NoSource:	0
URL:		http://glaros.dtc.umn.edu/gkhome/metis/parmetis/overviews
BuildRequires:	cmake >= 2.8
BuildRequires:	metis-devel
BuildRequires:	mpi-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ParMETIS is an MPI-based parallel library that implements a variety of
algorithms for partitioning unstructured graphs, meshes, and for
computing fill-reducing orderings of sparse matrices. ParMETIS extends
the functionality provided by METIS and includes routines that are
especially suited for parallel AMR computations and large scale
numerical simulations. The algorithms implemented in ParMETIS are
based on the parallel multilevel k-way graph-partitioning, adaptive
repartitioning, and parallel multi-constrained partitioning schemes
developed at the Department of Computer Science and Engineering at the
University of Minnesota.

%description -l pl.UTF-8
ParMETIS to oparta na MPI biblioteka równoległa implementująca różne
algorytmy do podziału grafów bez struktur lub siatek oraz tworzenia
porządków redukujących dla macierzy rzadkich. ParMETIS rozszerza
funkcjonalność biblioteki METIS i zawiera procedury dopasowane
szczególnie do równoległych obliczeń AMR oraz wielkoskalowych
symulacji numerycznych. Algorytmy zaimplementowane w ParMETIS są
oparte na schematach równoległych podziałów wielopoziomowych,
podziałów adaptacyjnych oraz równoległych podziałów z wieloma
ograniczeniami opracowanych na wydziale informatyki (Depratment of
Computer Science and Engineering) Uniwersytetu w Minnesocie.

%package devel
Summary:	Header files for ParMETIS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ParMETIS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	metis-devel
Requires:	mpi-devel

%description devel
Header files for ParMETIS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ParMETIS.

%package static
Summary:	Static ParMETIS library
Summary(pl.UTF-8):	Statyczna biblioteka ParMETIS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ParMETIS library.

%description static -l pl.UTF-8
Statyczna biblioteka ParMETIS.

%prep
%setup -q
%patch0 -p1

%build
mkdir -p build-shared build-static
srcdir="$(pwd)"
cd build-static
%cmake .. \
	-DGKLIB_PATH="$srcdir/metis/GKlib" \
	-DMETIS_PATH="$srcdir/metis" \
	-DMPI_LIBRARIES="-lmpi"
%{__make}
cd ../build-shared
%cmake .. \
	-DGKLIB_PATH="$srcdir/metis/GKlib" \
	-DMETIS_PATH="$srcdir/metis" \
	-DMPI_LIBRARIES="-lmpi" \
	-DSHARED=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C build-shared install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{mtest,ptest}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE.txt
%attr(755,root,root) %{_bindir}/parmetis
%attr(755,root,root) %{_bindir}/pometis
%attr(755,root,root) %{_libdir}/libparmetis.so

%files devel
%defattr(644,root,root,755)
%doc manual/manual.pdf
%{_includedir}/parmetis.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libparmetis.a
