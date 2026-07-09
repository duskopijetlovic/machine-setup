# rhel1 - Dell Pro Max Tower T2 FCT 2250

RHEL 10.1, GNOME/Wayland. Hybrid graphics: Intel Arrow Lake iGPU (`i915`)
+ discrete NVIDIA RTX 5070 Ti (GB203, Blackwell, proprietary `nvidia` driver).

> **Scope: rhel1 only.** The NVIDIA / hybrid-GPU notes below do **not** apply
> to the ThinkPad machines (no discrete NVIDIA GPU) or to any other host.

## Display / monitor cabling

- The monitor **must** be plugged into the **NVIDIA card's** HDMI port (on the
  discrete card's bracket), **not** the motherboard/Intel HDMI port.
- Reason: at boot, fbcon claims the NVIDIA framebuffer as the primary console
  (`fbcon: nvidia-drmdrmfb (fb0) is primary device`). If the monitor is on the
  Intel port, GNOME still renders (it does proper multi-GPU output routing),
  but the text VTs render on the NVIDIA GPU's outputs - which then have no
  monitor attached. Symptom: Ctrl+Alt+F3 goes black/frozen; Ctrl+Alt+F2
  returns to GNOME.
- Cable on the NVIDIA port aligns the console GPU and the display GPU, so text
  consoles render correctly.

## Virtual terminals (text consoles)

- VT1 = GDM greeter (spawns on demand; idle after graphical login).
- VT2 = GNOME Wayland session.
- VT3-VT6 = text consoles (getty), reached via Ctrl+Alt+F3 ... F6.
- VTs render **sequentially**: step F3 -> F4 -> F5 -> F6 in order. Jumping
  straight to a not-yet-reached VT may show black until the prior one has been
  activated. The gettys are running the whole time (confirmed via `ps`/
  `systemctl`) - only the framebuffer painting is lazy. (Blackwell fbcon
  maturity; may change with driver/kernel updates.)
- Escape hatch if a VT won't paint: Ctrl+Alt+F2 returns to GNOME. For a shell
  that never depends on VT rendering, use ptyxis in-session or SSH in.

## GPU: display + compute sharing

- The 5070 Ti drives the display **and** is available for compute (Ollama /
  local LLM inference) at the same time.
- Desktop **compute** cost is negligible.
- Desktop **VRAM** cost is ~0.5-1.5 GB against the card's 16 GB. Budget for
  this when sizing local models + context length (e.g. Qwen2.5-Coder).
  `nvidia-smi` shows both the model and the compositor allocation.

## Verify

Confirmed-good config as of **RHEL 10.1, kernel 6.12.0-124.8.1.el10_1**.
Re-run after any driver/kernel update - Blackwell console support is still
maturing and the behaviour above can change.

    # nvidia-drm.modeset=1 present on the kernel cmdline:
    cat /proc/cmdline

    # modeset active (Y):
    sudo cat /sys/module/nvidia_drm/parameters/modeset

    # which GPU has the connected display (card1 = Intel, card2 = NVIDIA):
    for p in /sys/class/drm/card*/card*-*/status; do echo "$p: $(cat "$p")"; done

    # which framebuffer fbcon picked as primary:
    sudo dmesg | grep -i -e fbcon -e "nvidia-drm" -e "frame buffer"

    # VT / session layout (VTNr, TTY, Type per session):
    loginctl list-sessions
