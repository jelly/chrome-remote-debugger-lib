# chrome-remote-debugger-lib
Python library to interact with chrome's remote debugging protocol

Start chrom(ium) with the following option:

     chromium --remote-debugging-port=9222

Part of the protocol seems to be documented [here](https://developer.chrome.com/devtools/docs/protocol/1.1/page)

Usage
-----

    from chrome_remote_lib import ChromeShell

    In []: shell = ChromeShell()

    In []: tab1 = shell.tabs()[1]

    In []: tab1.reload()
    Out[]: True

    In []: shell.create_tab('https://github.com')
    Out[]: ChromiumTab()
