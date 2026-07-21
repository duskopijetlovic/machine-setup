# Packages for a new machine

Software to install when provisioning a machine. Organized by platform and by
install method, because the same software often has different package names -
or no package at all - across RHEL and FreeBSD.

This is a **read-and-run reference**, not an automated script: review it, then
run the relevant sections by hand. (Promote to a script only if the manual
installs ever become tedious enough to justify the automation.)

---

## RHEL 10.x (dnf)

### Prerequisite: enable EPEL + CRB
Many packages below live in EPEL, which also needs CRB (CodeReady Builder):

```
$ sudo subscription-manager repos --enable codeready-builder-for-rhel-10-x86_64-rpms
$ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
```
(On a non-subscribed/Stream box, enable CRB with:
`sudo dnf config-manager --set-enabled crb`)

### From the base/AppStream/CRB repos
```
$ sudo dnf install \
  vim-enhanced \
  tcsh \
  cronie \
  gnome-screenshot-tool \
  readline-devel \
  gcc \
  make \
  xterm \
  xorg-x11-fonts-misc \
  xrdb \
  aspell \
  keepassxc \
  thunderbird \
  firefox \
  chromium \
  lynx \
  google-carlito-fonts
  # xorg-x11-fonts-misc: traditional X bitmap fonts (fixed 6x13 etc.) - the
  # classic xterm look; weak dep of xterm, listed explicitly so it's guaranteed
  # xrdb: loads ~/.Xresources (xterm colors/fonts/keybindings); XWayland apps
  # read it. Run after login or config change:  xrdb ~/.Xresources
  # lynx: text-based web browser (base repo, exact match: `dnf search lynx`)
  # google-carlito-fonts: Calibri metric-compatible sans-serif. Install this
  # so LibreOffice renders Calibri .docx files with correct metrics/layout.
  # (The orange "font substituted" warning in Writer stays - LibreOffice
  # reports the REQUESTED font, not the substitute - but layout is faithful.)
  # NOTE: RHEL name is google-carlito-fonts; FreeBSD calls it
  # crosextrafonts-carlito (see FreeBSD section + name map).
  # ... add the rest of your everyday packages
```

### LibreOffice on RHEL: official TDF RPMs (NOT a dnf repo package)
LibreOffice is **absent from RHEL's default repos**; the distro `libreoffice`
metapackage is not the install path here. Install the official Document
Foundation (TDF) RPMs instead - this matches the auditable, rpm/dnf-queryable
approach and is what the RHEL box actually runs (packages appear as
`libreoffice26.2-*` / `libobasis26.2-*`, e.g. `dnf search libreoffice`).

```
# Download the current stable RPM tarball from documentfoundation.org
# (keep the download wherever you stage installers; ~/Downloads is fine -
#  the installer uses the extracted RPMs, not the tarball).
$ cd ~/Downloads
$ curl -LO https://download.documentfoundation.org/libreoffice/stable/<version>/rpm/x86_64/LibreOffice_<version>_Linux_x86-64_rpm.tar.gz
# Optional integrity check: grab the matching .sha256 from the same dir, then
#   sha256sum -c LibreOffice_<version>_Linux_x86-64_rpm.tar.gz.sha256

$ tar xzf LibreOffice_<version>_Linux_x86-64_rpm.tar.gz
$ cd LibreOffice_<version>*/RPMS
$ sudo dnf install ./*.rpm     # RPMs hardcode /opt/libreoffice<major.minor>/;
                               # you do NOT choose a target. desktop-integration
                               # RPM (GNOME menus + MIME) is matched by ./*.rpm.
```
The TDF packages install under `/opt/libreoffice26.2/` and do **not** create a
`/usr/bin/libreoffice` wrapper (that's a distro-repackaging convenience). The
real entry point is `/opt/libreoffice26.2/program/soffice`; `.desktop` files
call it by absolute path, so the GNOME app grid works. For a terminal-callable
name, symlink it into `~/.local/bin/` (already on PATH, per-user, auditable):
```
$ ln -s /opt/libreoffice26.2/program/soffice ~/.local/bin/libreoffice
```
The target path carries the version (`libreoffice26.2`), so a future
major.minor upgrade means re-pointing that symlink.

### Third-party repo: Brave browser
Brave is not in the RHEL repos; add its repo and key first, then install:
```
$ sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo
$ sudo rpm --import https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
$ sudo dnf install brave-browser
```

### From EPEL (requires EPEL+CRB enabled, above)
```
$ sudo dnf install \
  remind        # NOTE: verify — may NOT be in EPEL 10; see "from source" below
  # ... other EPEL-only packages
```

### From source (not packaged in EPEL 10)
These have no dnf package on RHEL 10 and are built from upstream. Build deps
(gcc, make, etc.) are in the base section above.

- **remind** - https://dianne.skoll.ca/projects/remind/
  ```
  cd /tmp
  curl -LO https://dianne.skoll.ca/projects/remind/download/remind-<version>.tar.gz
  tar xzf remind-<version>.tar.gz && cd remind-<version>
  ./configure && make && make test && sudo make install   # installs to /usr/local
  ```
- **Claws Mail** - built from source on RHEL 10 (not in EPEL 10).
  # (add build steps / upstream pointer)
- **ttyp0 (UW ttyp0)** - bitmap font used by xterm in `dot.Xresources.desktop`
  (`XTerm*font: -uw-ttyp0-...`). Confirmed NOT packaged on RHEL 10
  (`dnf search ttyp0` -> no matches); without it xterm falls back to `fixed`.
  Upstream: search for "uw-ttyp0" (Uwe Waldmann) - VERIFY current URL before
  building. Build is BDF->PCF via make; install fonts, run mkfontdir, add the
  directory to the font path. (Fill in exact steps on first successful build.)
- **XCursor-Pro (Decay theme)** - cursor theme referenced by
  `Xcursor.theme: Xcursor-Pro-Decay` in `dot.Xresources.desktop`. Confirmed
  NOT packaged on RHEL 10 (`dnf search decay` -> no matches); if absent, the
  resource is silently ignored (default cursor used). Manual install: download
  a release from the XCursor-Pro project (VERIFY current upstream, likely on
  GitHub) and unpack the theme into `~/.icons/` (per-user) or
  `/usr/share/icons/` (system-wide).

---

## FreeBSD 14 (pkg)

```
$ sudo pkg install \
  libreoffice \
  vim \
  remind \
  aspell \
  keepassxc \
  thunderbird \
  firefox \
  chromium \
  lynx \
  crosextrafonts-carlito
  # lynx: text-based web browser. Plain `lynx` is the pkg you want -
  # `pkg search lynx` also lists ja-lynx (multi-byte build) and lynx-current
  # (development); don't grab those by mistake.
  # crosextrafonts-carlito: Calibri metric-compatible font (RHEL calls it
  # google-carlito-fonts). Same purpose - faithful Calibri .docx rendering.
  # ... add the rest
```

Notes on FreeBSD name differences vs RHEL:
- `vim-enhanced` (RHEL)  ->  `vim` (FreeBSD)
- `remind` is packaged in FreeBSD ports (unlike EPEL 10, where it's source-built)
- **LibreOffice**: FreeBSD has a single native pkg `libreoffice` (currently
  26.2.4.2) - just `sudo pkg install libreoffice`. This is simpler than RHEL,
  where LibreOffice is absent from the repos and installed from official TDF
  RPMs into /opt (see RHEL LibreOffice section). Same suite, very different
  install path per platform.
- **carlito font**: `crosextrafonts-carlito` (FreeBSD) vs `google-carlito-fonts`
  (RHEL) - different package names, same Calibri-metric-compatible font.
- **Brave**: not in the standard install line above.
  - RHEL: needs Brave's third-party repo + key first (see RHEL section);
    package name `brave-browser` (native).
  - FreeBSD: packaged as `linux-brave` (the Linux binary under FreeBSD's
    Linux emulation - NOT a native build; Origin www/linux-brave). Install:
    `sudo pkg install linux-brave`  (requires the Linux compat layer enabled).
- (add others as you discover them)

---

## Cross-platform name map (quick reference)

| Purpose              | RHEL 10 (dnf)          | FreeBSD 14 (pkg) | Notes                          |
|----------------------|------------------------|------------------|--------------------------------|
| Office suite         | (TDF RPMs, /opt)       | libreoffice      | RHEL: not in repos, official TDF RPMs -> /opt/libreoffice26.2. FreeBSD: native pkg |
| Vim (full)           | vim-enhanced           | vim              | RHEL `vi` = vim-minimal (tiny) |
| C-shell              | tcsh                   | (base system)    | tcsh is in FreeBSD base        |
| Cron                 | cronie                 | (base system)    | cron is in FreeBSD base        |
| Calendar reminders   | remind (from source)   | remind (pkg)     | not in EPEL 10; source on RHEL |
| Screenshot           | gnome-screenshot-tool  | (n/a — X11)      | Wayland-native on RHEL         |
| X terminal           | xterm                  | xterm            | runs via XWayland on RHEL      |
| Classic X bitmap fonts | xorg-x11-fonts-misc  | xorg-fonts       | xterm's default `fixed` font; verify FreeBSD pkg name |
| Spell checker        | aspell                 | aspell           | same name; may want language dict subpackages |
| Password manager     | keepassxc              | keepassxc        | same name; opens the same .kdbx everywhere |
| Mail client          | thunderbird            | thunderbird      | same name                      |
| Browser (Firefox)    | firefox                | firefox          | same name                      |
| Browser (Chromium)   | chromium               | chromium         | same name                      |
| Browser (Brave)      | brave-browser (3rd-party repo) | linux-brave (Linux emu) | RHEL: add Brave repo+key first, native pkg. FreeBSD: Linux binary, needs Linux compat layer |
| Browser (text)       | lynx                   | lynx             | same name; FreeBSD also has ja-lynx / lynx-current variants - use plain `lynx` |
| Calibri-compat font  | google-carlito-fonts   | crosextrafonts-carlito | different names; same Carlito font for faithful Calibri .docx rendering |
| (add rows as you go) |                        |                  |                                |
