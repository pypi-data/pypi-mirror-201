# uFBT - micro Flipper Build Tool

uFBT is a cross-platform tool for building applications for Flipper Zero. It is a simplified version of [Flipper Build Tool (FBT)](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/documentation/fbt.md).

uFBT enables basic development tasks for Flipper Zero, like building and debugging applications, flashing firmware, creating VSCode development configurations. It uses prebuilt binaries and libraries, so you don't need to build the whole firmware to compile and debug your application for Flipper.

## Installation

uFBT uses your system's Python for running bootstrap code. Minimal supported Python version is 3.8.

### Linux & macOS
`python3 -m pip install --upgrade ufbt`

### Windows
`py -m pip install --upgrade ufbt`

When running actual build tasks, uFBT will download and use its own Python binaries and a toolchain for your platform.

On first run, uFBT will download and install required SDK components from `dev` branch of official firmware. For more information on how to switch to a different version of the SDK, see [Managing the SDK](#managing-the-sdk) section.

## Usage

### Building & running your application

Run `ufbt` in the root directory of your application (the one with `application.fam` file in it). It will build your application and place the resulting binary in `dist` subdirectory.

You can upload and start your application on Flipper attached over  USB using `ufbt launch`.

### Debugging

In order to debug your application, you need to be running the firmware distributed alongside with current SDK version. You can flash it to your Flipper using `ufbt flash` (over ST-Link), `ufbt flash_usb` (over USB) or `ufbt flash_blackmagic` (using Wi-Fi dev board running Blackmagic firmware).

You can attach to running firmware using `ufbt debug` (for ST-Link) or `ufbt blackmagic` (for Wi-Fi dev board).

### VSCode integration

uFBT provides a configuration for VSCode that allows you to build and debug your application directly from the IDE. To deploy it, run `ufbt vscode_dist` in the root directory of your application. Then you can open the project in VSCode (`File`-`Open Folder...`) and use the provided launch (`ctrl+shift+b`) & debugging (`ctrl+shift+d`) configurations.

### Application template

uFBT can create a template for your application. To do this, run `ufbt create APPID=<app_id>` in the directory where you want to create your application. It will create an application manifest and its main source file. You can then build and debug your application using the instructions above.

Application manifests are explained in the [FBT documentation](https://github.com/flipperdevices/flipperzero-firmware/blob/dev/documentation/AppManifests.md).

### Other

 * `ufbt cli` starts a CLI session with the device;
 * `ufbt lint`, `ufbt format` run clang-format on application's sources.

## Managing the SDK

To update the SDK, run `ufbt update`. This will download and install all required SDK components from previously used source.

- To switch to SDK for a different release channel, run `ufbt update --channel=[dev|rc|release]`. 
- To use SDK for a certain release or a not-yet-merged branch from official repo, run `ufbt update --branch=0.81.1` or `ufbt update --branch=owner/my-awesome-feature`. 
    - You can also use branches from other repos, where build artifacts are available from an indexed directory, by specifying `--index-url=<url>`.
    - uFBT also supports 3rd-party update indexers, following the same schema as official firmware. To use them, run `ufbt update --index-url=<url>`, where `<url>` is a URL to the index file, e.g. `https://update.flipperzero.one/firmware/directory.json`.

- uFBT can also download and update the SDK from any fixed URL. To do this, run `ufbt update --url=<url>`.

uFBT stores its state in `.ufbt` subfolder in your home directory. You can override this location by setting `UFBT_DIR` environment variable.


### ufbt-bootstrap

Updating the SDK is handled by uFBT component called _bootstrap_. It has a dedicated entry point, `ufbt-bootstrap`, with additional options that might be useful in certain scenarios. Run `ufbt-bootstrap --help` to see them.

### Troubleshooting

If something goes wrong and uFBT state becomes corrupted, you can reset it by running `ufbt clean`. If that doesn't work, you can try removing `.ufbt` subfolder manually from your home folder.
