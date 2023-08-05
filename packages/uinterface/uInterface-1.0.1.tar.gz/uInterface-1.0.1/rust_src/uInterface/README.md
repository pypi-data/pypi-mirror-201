# uInterface

## Table of contents

1. [Table of contents](#table-of-contents)
2. [uInterface (GUI application)](#uinterface-gui-application)
    * [What is uInterface](#what-is-uinterface)
    * [How to install uInterface](#how-to-install-uinterface)
    * [Features of uInterface](#features-of-uinterface)
3. [uInterface (Python & Rust library)](#uinterface-python--rust-library)
    * [What is uInterface library](#what-is-uinterface-library)
    * [How to install uInterface library](#how-to-install-uinterface-library)
    * [How to use uInterface library](#how-to-use-uinterface-library)
4. [Contributing](#contributing)
5. [Mentions & bibliography](#mentions--bibliography)

## uInterface (GUI application)

### What is uInterface

uInterface is an application that can be used alternatively to the UVa judge and uHunt websites. It offers pretty much the same functionalities as them, but with the key advantage that is not having to switch over multiple tabs in your web browser. Following there are a set of instructions to install uInterface, as well as a full-on explanation of the features of this application.

### How to install uInterface

In order to install and use uInterface, you will have to follow the installation guide for your operating system.

#### Windows

Windows installation is as easy as it gets. Just go to [releases](https://github.com/LovetheFrogs/uInterface/releases) and download the latest version of the uInterface windows executable (.exe).

#### Linux

To install the application for linux, go to [releases](https://github.com/LovetheFrogs/uInterface/releases) and download the source code. Once downloaded, extract the files and execute the shell script run_linux.sh. Note you may need to give the script permission to execute with `sudo chmod +x run_linux.sh`. The script will download all the dependencies needed to run the application and run it. Note that once the dependencies are installed, they will not be downloaded next time you execute the script.

### Features of uInterface

uInterface has some unique features, which will be descriped below.

The app allows users to log-in to their UVa judge accounts (same system as uHunt) to see their last submissions and position in the global ranking. Also, they can search for a problem, wich will promt the user with the pdf of that problem, statistics for it and last submissions to the problem by the logged in user (if any submissions were done). Problems can also be submited here by clicking the button *Sumbit this problem*, which will take them to the UVa judge submission page. Note that they will have to be logged in to their UVa judge account on the website, otherwise they will be asked to log-in and take them to the main page of the judge.

## uInterface (Python & Rust library)

### What is uInterface library

For correct development of the GUI application, a Python library was coded using Rust. This library can also be used in Rust and links to both PyPI and crates.io are found at the end of the README under [Mentions & bibliograpy](#mentions--bibliography).

The library(es) provide an easy to use interface to make requests to [uHunt's API](https://uhunt.onlinejudge.org/api). This requests get parsed to a `struct` or a `dictionary` (rust and python respectively), which allow to access the fields of the responses.

### How to install uInterface library

To install the libraries, run either `pip install uInterface` for python or add the following dependency to your `Cargo.toml` file:

```Cargo
uInterface=1.0.0
```

### How to use uInterface library

To get a look on how to use these libraries, go to the PyPI/crates.io page for the libraries ([Mentions & bibliograpy](#mentions--bibliography)) and read the full documentation, which contains the functions implemented by this libraries.

## Contributing

To contribute to the project, please read the short CONTRIBUTING.md file. If you want to submit a new issue, follow the issue templates. Pull requests don't have a template, but they should be linked to an isuue and tagged properly.

## Mentions & bibliography

Special thanks to:

* Felix Halim, creator of uHunt website and uHunt's API
* Universidad de Valladolid, for hosting the UVa judge

### Bibliograpy

* [PyPI library](https://pypi.org/project/uinterface/)
* [crates.io library](https://crates.io/crates/u_interface)
