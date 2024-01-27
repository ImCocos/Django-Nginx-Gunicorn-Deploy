# TZ

 1) Configs(SiteName.ini) **must not** be stored in ap directory(.../app/sites/)
 2) Configs**must be** stored in workdir of project
 3) Configs **must be** named same from now! - *.sitemanager.ini*[discussible]
 4) Class Site in *site_config.py* **must not lose** any methods! You can override them, or something else, but dezentralization should not affect code in *main.py* and it should work as before
    - better to make a few new methods that will be integrated in future
    - better to just add them, and slowly but surely rewrite them through a few commits
 5) Goal of dezentralization is to get rid of sites/ folder in app directory and to store only one file that should store info only about workdirs.
 6) How i see a process of gettings info about site:
    - cmd from user -> resolve -> go to Site class -> load info about **CWD** -> load config from **CWD** -> create instance of Site class -> show info to user
