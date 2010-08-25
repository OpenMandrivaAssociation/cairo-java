%define _disable_ld_no_undefined 1

Name:           cairo-java
Version:        1.0.8
Release:        %mkrel 7.0.4
Epoch:          0
Summary:        Java bindings for the Cairo library
License:        LGPLv2
Group:          System/Libraries
URL:            http://java-gnome.sourceforge.net/
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/cairo-java/1.0/cairo-java-%{version}.tar.bz2
Source1:        cairo-java-1.0.8.changes
Source2:        cairo-java-1.0.8.md5sum
Source3:        cairo-java-1.0.8.news
Source4:        java-gnome-macros.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  cairo-devel
BuildRequires:  glib-java-devel
BuildRequires:  docbook-utils
BuildRequires:  java-rpmbuild
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-gcj-compat-devel


%description
Cairo-java is a language binding that allows developers to write Cairo
applications in Java.  It is part of Java-GNOME.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Conflicts:      cairo-java < 1.0.8-2

%description    devel
Development files for %{name}.

%prep
%setup -q
%setup -q -T -D -a 4

%build 
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
export JAVAH=%{_jvmdir}/java-rpmbuild/bin/javah
export GCJ=%{gcj}
export CPPFLAGS="-I%{java_home}/include -I%{java_home}/include/linux"
# workaround:
# libtool does not use pic_flag when compiling, so we have to force it. 
export GCJFLAGS="-O2 -fPIC" 
%{configure2_5x} --with-jardir=%{_javadir}
make

# pack up the java source
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/^lib//")
zipfile=$PWD/$jarname$jarversion-src-%{version}.zip
pushd src/java
%{_bindir}/zip -9 -r $zipfile $(find -name \*.java)
popd

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
%{__rm} -f %{buildroot}%{_libdir}/*.a
%{__rm} -rf %{buildroot}/%{name}-%{version}

# install the src.zip and make a sym link
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/^lib//")
%{__install} -m 644 $jarname$jarversion-src-%{version}.zip $RPM_BUILD_ROOT%{_javadir}/
pushd %{buildroot}%{_javadir}
%{__ln_s} $jarname$jarversion-src-%{version}.zip $jarname$jarversion-src.zip
popd

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/AUTHORS 
%doc %{_docdir}/%{name}-%{version}/COPYING 
%doc %{_docdir}/%{name}-%{version}/INSTALL
%doc %{_docdir}/%{name}-%{version}/README
%doc %{_docdir}/%{name}-%{version}/NEWS 
%{_libdir}/libcairojava-*.so
%{_libdir}/libcairojni-*.so
%{_javadir}/*.jar

%files devel
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/api
#%doc doc/api
%{_javadir}/*.zip
%{_libdir}/libcairojava.so
%{_libdir}/libcairojni.so
%{_libdir}/*la
%{_libdir}/pkgconfig/*


