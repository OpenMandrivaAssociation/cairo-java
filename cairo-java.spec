Name:           cairo-java
Version:        1.0.8
Release:        %mkrel 1
Epoch:          0
Summary:        Java bindings for the Cairo library
License:        LGPL
Group:          Development/Java
URL:            http://java-gnome.sourceforge.net/
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/cairo-java/1.0/cairo-java-%{version}.tar.bz2
Source1:        cairo-java-1.0.8.changes
Source2:        cairo-java-1.0.8.md5sum
Source3:        cairo-java-1.0.8.news
Source4:        java-gnome-macros.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:       gtk2 >= 0:2.10.6
Requires:       cairo >= 0:1.2.4
Requires:       libcairo-devel >= 0:1.2.4
Requires:       glib-java >= 0:0.4.0
BuildRequires:  glib-java >= 0:0.4.0
BuildRequires:  gtk2-devel >= 0:2.10.6, gcc-java >= 0:4.1.1
BuildRequires:  docbook-utils
BuildRequires:  jpackage-utils
BuildRequires:  java-devel >= 0:1.4.2

%description
Cairo-java is a language binding that allows developers to write Cairo
applications in Java.  It is part of Java-GNOME.

%package        devel
Summary:        Compressed Java source files for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description    devel
Compressed Java source for %{name}. This is useful if you are developing
applications with IDEs like Eclipse.

%prep
%setup -q
%setup -q -T -D -a 4
%{__aclocal} -I macros --force
%{__autoconf} --force
%{__automake} --copy --force-missing
%{__libtoolize} --automake --copy --force

%build 
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
%{configure2_5x} --with-jardir=%{_javadir}
%{make}

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/api AUTHORS ChangeLog COPYING INSTALL README NEWS 
%{_libdir}/*so* 
%{_libdir}/*la
%{_libdir}/pkgconfig/*
%{_javadir}/*.jar

%files devel
%defattr(-,root,root)
%{_javadir}/*.zip


