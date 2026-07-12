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
  libreoffice \
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
  chromium
  # xorg-x11-fonts-misc: traditional X bitmap fonts (fixed 6x13 etc.) - the
  # classic xterm look; weak dep of xterm, listed explicitly so it's guaranteed
  # xrdb: loads ~/.Xresources (xterm colors/fonts/keybindings); XWayland apps
  # read it. Run after login or config change:  xrdb ~/.Xresources
  # ... add the rest of your everyday packages
```

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
  chromium
  # ... add the rest
```

Notes on FreeBSD name differences vs RHEL:
- `vim-enhanced` (RHEL)  ->  `vim` (FreeBSD)
- `remind` is packaged in FreeBSD ports (unlike EPEL 10, where it's source-built)
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
| Office suite         | libreoffice            | libreoffice      | same name                      |
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
| (add rows as you go) |                        |                  |                                |
