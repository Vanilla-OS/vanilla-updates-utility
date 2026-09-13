<div align="center">
    <img src="data/icons/hicolor/scalable/apps/org.vanillaos.UpdatesUtility.svg" height="64">
    <h1>Vanilla Updates Utility</h1>

[![Translation Status][weblate-image]][weblate-url]

[weblate-url]: https://hosted.weblate.org/engage/vanilla-os/
[weblate-image]: https://hosted.weblate.org/widgets/vanilla-os/-/vanilla-updates-utility/svg-badge.svg

<p>A frontend in GTK 4 and Libadwaita to manage system updates in Vanilla OS.</p>
<br />
<img src="data/screenshot.png">
</div>

## Build

### Dependencies

- build-essential
- meson
- libadwaita-1-dev
- gettext
- desktop-file-utils
- vso

### Build

```bash
meson setup build
ninja -C build
```

### Install

```bash
sudo ninja -C build install
```

## Run

```bash
vanilla-updates-utility

# embedded mode
vanilla-updates-utility --embedded
```

## Use of Generative AI

Maintainers may use generative AI tools as assistants while working on vanilla-updates-utility. Non-trivial assisted commits disclose the tool, model, and scope of the work.

AI tools may assist with code comments, documentation, repetitive code, and issue triage. Maintainers make project decisions and review every assisted change before it is merged.

Use these trailers for non-trivial assisted commits:

```plain
Assisted-by: <tool>:<model-version>
AI-Scope: <what the tool generated and the prompt or a short prompt summary>
```

Single-line completions, renames, and formatting changes do not need trailers.

Coding agents must also follow [AGENTS.md](AGENTS.md) before changing files,
creating commits, or opening pull requests.
