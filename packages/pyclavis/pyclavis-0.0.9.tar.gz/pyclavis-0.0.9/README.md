
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pyclavis

`pyclavis` a password manager with autofill and predefined templates as download.

the predefined provider and autofill for downloading via `download` tab moved to an own repo. 
[`github autofill`](https://github.com/kr-g/autofill)



## what's new ?

check
[`CHANGELOG`](https://github.com/kr-g/pyclavis/blob/main/CHANGELOG.md)
for latest ongoing, or upcoming news
and also
for known issues, limitations and backlog refer to 
[`BACKLOG`](https://github.com/kr-g/pyclavis/blob/main/BACKLOG.md).
in case it breaks between two versions check `CHANGELOG`
first before creating a ticket / issue on github. thanks.


## platform

tested on linux and python3


## limitations

- see backlog


## installation

    python3 -m pip install pyclavis


## installation on raspberry pi, or fedora

when during startup an error is thrown, such as:

    from PIL import Image, ImageTk, ImageDraw, ImageFont
    ImportError: cannot import name 'ImageTk' from 'PIL' (/usr/lib64/python3.10/site-packages/PIL/__init__.py)

here it is required to install imagetk in addtion 

    # debian ubuntu etc
    sudo apt-get install python3-pil python3-pil.imagetk

    # fedora
    sudo yum install python3-pillow python3-pillow-tk


## general concept

the credential information is kept separately from other 
login and autofill information.

the login process as such is done by using predefined login information (URLs)
and autofill / autotype steps together with the credital.

the predefined login and autofill information can be downloaded from a
remote github repo on the download tab in the application. 

the minimal required steps are done on tabs base, browser, and history.


## first steps

since predefined content is downloaded from github it's recommended to
use github token based access with [`pygitgrab`](https://github.com/kr-g/pygitgrab).
add on settings tab the parameter `-c` to enable this. 
read more on 
[github token access](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

then go to download tab and get the predefined provider and autofill from github.
how to define own custom ones will described later.

then go to base tab.


## a first login round

create a credential first (e.g. for gmail) and select provider pyclavis,
and service google in the listboxes.

below the tabs field the info about the selected configuration is shown.

**optional:** click right on google to see the configuration for that entry.
close the messagebox.

go to tab browser to select the browser to use.

click on button open in browser what will open a browser window with the URL.

confirm any cookie notification if required.

**important:** set the focus now to the users login field in the webpage.

go back to pyclavis, and click on button send key sequence.

the pyclavis window will be minimized and the autofill will enter the login data.

close the browser, and go to tab history.

double click on one of the entries will open the browser with that already 
specified configuration.


### one note on maintaining creditial data

a creditial is specified by

- name
- user
- password
- category

when changing a creditial name or category there is currently no clash detection.
an already existing creditial with the same name, or category will be overwritten
without any further notification.



## enhanced usage with replacement parameter

go to base tab an select `pyclavis-stores`, and `ebay.com`.

right click on the select service `ebay.com`.

you see the following url

    https://signin.ebay.{TLD:com}/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.{TLD:com}%2F

the portion `{TLD:com}` is a replacement parameter with default value `com`.

go to settings tab and click on button open settings folder 
(or use file explorer with path `~/.pyclavis`)

open file `env.json`, or create an empty file `env.json`.
change the json to the following by adding a global `TLD` environment variable.

    {
        "TLD" : "de"
    }

now when clicking on button open in browser the URL above will be modified to

    https://signin.ebay.de/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.de%2F    


## enhanced usage with profile replacement parameter

go to settings tab and click on button open settings folder 
(or use file explorer with path `~/.pyclavis`).


open sub-folder `~/.pyclavis/profiles`.

create a new file `pypi-test.json` with the following content and save it.

    {
        "PYPI" : "test"
    }

go to tab profile and press button reload profile data.

click on entry `pypi-test`

below the tabs field the info about the selected configuration is shown.
it shound have a structure like

    credit @ service << profile_name / browser
    
unselect the entry `pypi-test` by clicking on it again

the selected configuration changes now to 

    credit @ service / browser

click again on entry `pypi-test` to select the profile.

go to base tab, and select provider `pyclavis-dev` and service `org-pypi`.

right click on entry `org-pypi`.

the URL shown is

    https://{PYPI:www}.pypi.org/account/login/
    
    
when clicking on button open in browser it will open the URLs

    https://www.pypi.org/account/login/
    
or 

    https://test.pypi.org/account/login/

depending if the profile is selected or not.


## enhanced usage with favorites 

a favorites URL acts as an additonal replacement parameter `URL`.

use favorites e.g. with the provider-service `generic`, or `generic-2-steps`.

using favorites the selected configuration shows a structure like

    credit @ service << profile_name : favorite / browser



## environment, favorites and profile replacement parameter in detail

replacement of parameters is done by search order

- profile (if selected one as active)
- favorite URL (if selected one as active)
- env.json 
- os.environ (pyhton environment variable)


## creating own provider and autofill

currently there is no dialog to maintain own provider / autofill.
this must be done directly in the folder `~/.pyclavis/downloads/`.

### a sample autofill

create a folder `sample` under path `~/.pyclavis/downloads/`

create a file `~/.pyclavis/downloads/sample.json` with the following content, and save it

    {
        "name":"ebay.com",
        "url" : "https://signin.ebay.{TLD:com}/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.{TLD:com}%2F", 
        "autofill": "{USER}\n{ENTER}\n{DELAY {NDELAY:2000}}\n{PASSWORD}\n{ENTER}"
    }

go to tab download and click button reload from disk.

go to tab base and under provider an entry with name `sample` is shown.

click on it and under service `ebay.com` should appear.


## autofill commands

autofill commands are surrounded by curley brackets

    {command}

some commands have an optional parameter 

| name | description |
| --- | --- | 
| USER | sends the user name  |
| PASSWORD | sends the user password  |
| ENTER | sends keystroke enter  |
| TAB | sends keystroke tab |
| TAB 3 | sends keystroke tab 3 times |
| SELALL | sends keystroke cntrl+a for selecting all content in an input field |
| ENV varname | sends the os.environ variable `varname` |
| DELAY millisec | waits for given number of milli seconds before continue autofill |
| DELAYSTD millisec | sets the delay period between 2 autofill commands to milli seconds |
| DELAYSTD | resets the delay period between 2 autofill commands |

additional meta commands 

| name | description |
| --- | --- | 
| CNAME | name of the credit  |
| PNAME | name of the profile if selected  |
| FNAME | name of the favorite if selected  |


**important:** each command in the json must be separeted by a newline `\n`.

it is possible to combine replacement parameters with commands. 
e.g.

    {DELAY {NDELAY:2000}}
    
this will default to 2000 milli seconds, 
or if `NDELAY` is given in a profile or `env.json`
it will be expanded to the value found there.


**important:** don't name replacement parameter like autofill commands. 
this would lead to name clashes and not to the expected result.
check logging output if unexpected behaviour takes place.


## file and folders

IMPORTANT: 
the directory entry `~/.pyclavis` could be a file or a folder (default).
if the configuration should reside inside a different folder or on a removeable
device this file contains the path to the configuration folder there.


| name | type | description |
| --- | --- | --- | 
| ~/.pyclavis_store | file | contains the encrypted credentials |
| ~/.pyclavis/ | folder | folder for configuration data |
| ~/.pyclavis/ | file | contains path to configuration data folder |
| ~/.pyclavis/downloads | folder | contains the downloaded data  |
| ~/.pyclavis/profiles | folder | contains the profile data |
| ~/.pyclavis/config.json | file | mainly the configuration from settings tab |
| ~/.pyclavis/env.json | file | the environment profile |
| ~/.pyclavis/favorites.crypt.json | file | crypted favorites |
| ~/.pyclavis/history.json | file | history tab |
| ~/.pyclavis/socket.info | file | internal use |
| ~/.pyclavis_key | file | (not recommended) in case your computer is already "protected" enough and pyclavis should start without the prompt this file contains the master password |


### sample: move configuration folder

open a shell and exeute 

    mv ~/.pyclavis ~/.pyclavis_conf
    echo ~/.pyclavis_conf  >  ~/.pyclavis

then start pyclavis 


## security information

the `~/.pyclavis_store` file is encrypted with 256 bit.

## provider and autofill download

the provider and autofill moved to an own repo. 
[`github autofill`](https://github.com/kr-g/autofill)


# all cmd-line opts

all cmd-line opts are described here 
[`README_CMDLINE`](./README_CMDLINE.md)


# license

[`LICENSE`](./LICENSE.md)

