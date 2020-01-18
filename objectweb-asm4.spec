# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           objectweb-asm4
Version:        4.0
Release:        3%{?dist}
Epoch:          0
Summary:        A code manipulation tool to implement adaptable systems
License:        BSD
URL:            http://asm.objectweb.org/
Group:          Development/Libraries
Source0:        http://download.forge.objectweb.org/asm/asm-%{version}.tar.gz
Source1:        asm4-%{version}-MANIFEST.MF
Patch0:         asm4-%{version}-no-classpath-in-manifest.patch
# Needed by asm-xml.jar
Requires:       xml-commons-jaxp-1.3-apis
Requires:       jpackage-utils >= 0:1.7.4
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  objectweb-anttask
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  zip
BuildArch:      noarch

%description
ASM is a code manipulation tool to implement adaptable systems.

%package javadoc
Group:         Documentation
Summary:       Javadoc for %{name}
Requires:      jpackage-utils

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n asm-%{version}
sed -i 's/\r//' LICENSE.txt README.txt
%patch0 -p0

# update asm gId
sed -i "s|<groupId>asm</groupId>|<groupId>org.ow2.asm</groupId>|" archive/*.pom

mkdir META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF

%build

ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install

# jars
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
for jar in output/dist/lib/*.jar; do
  install -m 644 ${jar} %{buildroot}%{_javadir}/%{name}/
done

touch META-INF/MANIFEST.MF
zip -u output/dist/lib/all/asm-all-%{version}.jar META-INF/MANIFEST.MF
install -m 644 output/dist/lib/all/asm-all-%{version}.jar %{buildroot}%{_javadir}/%{name}/
install -pm 644 output/dist/lib/all/asm-all-%{version}.pom %{buildroot}%{_mavenpomdir}/JPP.%{name}-asm-all-%{version}.pom

# pom
for pom in output/dist/lib/*.pom; do
  install -pm 644 ${pom} %{buildroot}%{_mavenpomdir}/JPP.%{name}-`basename ${pom}`
done

%add_maven_depmap JPP.%{name}-asm-%{version}.pom %{name}/asm-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-analysis-%{version}.pom %{name}/asm-analysis-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-commons-%{version}.pom %{name}/asm-commons-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-tree-%{version}.pom %{name}/asm-tree-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-util-%{version}.pom %{name}/asm-util-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-xml-%{version}.pom %{name}/asm-xml-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-all-%{version}.pom %{name}/asm-all-%{version}.jar
%add_maven_depmap JPP.%{name}-asm-parent-%{version}.pom

# javadoc
install -p -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr output/dist/doc/javadoc/user/* %{buildroot}%{_javadocdir}/%{name}

%files
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 04.0-3
- Mass rebuild 2013-12-27

* Thu Aug 02 2012 gil cattaneo <puntogil@libero.it> 0:4.0-2
- Fixed epoch

* Thu Jul 26 2012 gil cattaneo <puntogil@libero.it> 0:4.0-1
- Upgrade to 4.0
- Rename objectweb-asm4
- Adapt to current guidelines
- Fixed poms groupId org.ow2.asm
- Fixed Group field

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 0:3.3.1-2
- Use poms produced by the build not foreign ones.
- Adpat to current guidelines.

* Mon Apr 04 2011 Chris Aniszczyk <zx@redhat.com> 0:3.3.1
- Upgrade to 3.3.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Orion Poplawski <orion@cora.nwra.com>  0:3.2.1-2
- Change depmap parent id to asm (bug #606659)

* Thu Apr 15 2010 Fernando Nasser <fnasser@redhat.com> 0:3.2.1
- Upgrade to 3.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:3.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5.1
- build for Fedora

* Tue Oct 23 2008 David Walluck <dwalluck@redhat.com> 0:3.1-5
- add OSGi manifest (Alexander Kurtakov)

* Mon Oct 20 2008 David Walluck <dwalluck@redhat.com> 0:3.1-4
- remove Class-Path from MANIFEST.MF
- add unversioned javadoc symlink
- remove javadoc scriptlets
- fix directory ownership
- remove build requirement on dos2unix

* Fri Feb 08 2008 Ralph Apel <r.apel@r-apel.de> - 0:3.1-3jpp
- Add poms and depmap frags with groupId of org.objectweb.asm !
- Add asm-all.jar 
- Add -javadoc Requires post and postun
- Restore Vendor, Distribution

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-2jpp
- Fix EOL of txt files
- Add dependency on jaxp 

* Thu Nov 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.1-1jpp
- Upgrade to 3.1

* Wed Aug 22 2007 Fernando Nasser <fnasser@redhat.com> - 0:3.0-1jpp
- Upgrade to 3.0
- Rename to include objectweb- prefix as requested by ObjectWeb

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.1-2jpp
- First JPP 1.7 build

* Thu Oct 06 2005 Ralph Apel <r.apel at r-apel.de> 0:2.1-1jpp
- Upgrade to 2.1

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:2.0.RC1-1jpp
- First release of the 2.0 line.