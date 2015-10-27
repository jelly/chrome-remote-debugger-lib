# chrome-remote-debugger-lib
Python library to interact with chrome's remote debugging protocol

Start chrom(ium) with the following option:

     chromium --remote-debugging-port=9222

Part of the protocl seems to be documented [here](https://developer.chrome.com/devtools/docs/protocol/1.1/page)

Usage
-----

    from chrome_remote_lib import ChromeShell

    In [136]: shell = ChromeShell()

    In [137]: tab1 = shell.tabs()[1]

    In [138]: tab1.reload()
    Out[138]: True

    In [139]: tab1.reload()
    Out[139]: True

