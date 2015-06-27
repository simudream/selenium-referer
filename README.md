# Python Selenium tests with a custom Referer header

Sometimes, websites need to have different behavior for cases when users come
from different sources / search engines. In my use case, our website had to 
set a tracking cookie which would have different values for users that came
grom Google, AOL, Yahoo, or MSN. I had to test that the cookie was being set
correctly for all cases.

When I started writing my test cases, I found that there's no "official" way
to add a custom request header in Selenium. In fact, this is a feature the team
explicitly refused to implement:

[https://code.google.com/p/selenium/issues/detail?id=2047](https://code.google.com/p/selenium/issues/detail?id=2047)

Two possible ways of solving this problem are:

* Create 2 testing profiles in Firefox, and configure one of them with a
  custom referer, for example, using a [RefControl](https://addons.mozilla.org/en-US/firefox/addon/refcontrol/)
  extension. Select the profile dynamically in the unit test.
* Use a proxy server to intercept the request being sent, and inject a
  custom header.
  
First of these options requires manual intervention from the user, so it's
harder to distribute it. You have to explain to the person who's going to be
running the tests how to do all this, as opposed to just installing the needed
packages and running with it.

The current project implements the second option.

While the approach is not new, I could not find any complete solutions. So
I hope this helps someone else.

## What's included

Implementation of proxy server that adds a desired Referer header to 
intercepted requests:
```
referer_proxy.py
```

Base test class inherited from `unittest.TestCase`, and a module with helper
methods for working with `webdriver.Firefox` (opening, closing, navigating
to page, reading cookies, etc.):
```
base_with_proxy.py
utils.py
```

Two sample implementations:
```
test_referer_aol.py
test_referer_msn.py
```

List of required Python packages:
```
requirements.txt
```

Configuration file for running tests:
```
nose.cfg
```

## What's going on

Each test is:

* Starting a proxy server with the desired header parameter.

## Preparing the environment

Optionally, you can create a virtual Python environment for this
project. This is not necessary but recommended.

For example, I want to create an environment inside `../venvs/selenium-referer`:

```
$ virtualenv ../venvs/selenium-referer
$ source ../venvs/selenium-referer/bin/activate
```

Now, the virtual environment's Python will be used in installing further
packages.

## Installing packages

This solution is using `libmproxy` to implement a proxy server. Libmproxy is a
part of `mitmproxy` project (http://mitmproxy.org/).

First, install the Ubuntu package requirements for `mitmproxy`: 

```
$ sudo apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev
```

Then, install the required Python packages:

```
$ pip install -r requirements.txt
```

If you are on the platform other than ubuntu, use the instructions from 
the `mitmproxy` [documentation page](http://mitmproxy.org/doc/install.html)
instead.

On OS X, you should already have OpenSSL installed, so it may be enough to 
simply run:

```
$ pip install -r requirements.txt
```

## Running the tests

Either use PyCharm's nice test runner, or run the tests from command line:

```
$ nosetests --config=nose.cfg
```

Config is provided to list which tests need to be run.

## Running the proxy manually

To make sure that the proxy can be run by the tests, you can simply activate
the virtual environment and run it from command line, for example:

```
$ python referer_proxy.py --referer http://www.boo.com --port 8888
```

If the output is "Running...", then everything is OK. You can stop the server
with `Ctrl + C`.
