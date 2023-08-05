
# Changelog


## release v0.0.9 - ???

- scroll and highlight last entry in history after double click
- removed obsolete autofill folder
- changed license to APGL
- changed storage model
  - moved `~/.pyclavis_store` to `~/.pyclavis/.pyclavis_store`
    - needs manual file move by end-user
- different configuration path for `.pyclavis` folder
  - if `~/.pyclavis_store` is a normal file then this contains the path of the `.pyclavis` folder
    - e.g. move all `pyclavis` related configuration to an USB stick
  - see [`README`](./README.md) for sample
- sorting history tab entries
- 


## release v0.0.8 - 20221009

- added `init_delay_std` field. delay period after iconify window and start autofill
- layout changed slightly
- password generator default alphabet with more chars
- switch to new `tile.core`
- added icon support (needs some rework...)
- 


## release v0.0.7 - 20220524

- loading fav fix
- 


## release v0.0.6 - 20220426

- migrate to new tile core
- autofill meta commands CNAME PNAME FNAME
- added safe browsing mode (incognito browser tabs where possible)
  - limitation: firefox dont not open a private tab
- added `--export-json` 
- 


## release v0.0.5 - 20211110

- fix adding new credit not shown until app restart
-


## release v0.0.4 - 20211025

- moved autofill to own repo [`github autofill`](https://github.com/kr-g/autofill)
- entry point `pyclavis`
- fix check update and button re-trigger state
- added encrypted store for browser favorites, and dialog
- favorite integration as parameter URL when selected, replacement path -> profile, favorit, env, os.environ
  - cmdline `--export-favorites` added
- 


## first official release v0.0.3 - 20211010

- selected info text 
- double click on credit starts open in browser action
- fix credit name in info string
- download check in own background task (non-blocking)
- added logging
- added `--export` cmd_line command. prints tab separated credit information to stdout
- documentation
- fix delete credit
- 


## release v0.0.2 - 20211009

- ui rework
- added support for storing the master password in a `.pyclavis_key` file 
 (not recommended) in case your computer is already "protected" enough and
 pyclavis should start without the prompt
- passwort generator added
- bug fix, add password. overwrite last entry. resolved by copy values.
- listbox set_index() added
- provider data reload from disk (useful after manual external modification)
- python binary setting in config, defaults to python3
- update check on downloads tab will trigger pip install -U pyclavis
- double click in history start open in browser action
- switch to history tab after app start when history available
- single instance check, only one pyclavis is allowed to run at the same time
- 


## release v0.0.1 - 20211006 

- first unofficial release, tested on linux
- 
