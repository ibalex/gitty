# GITTY
* Do 4 git commands in one with the 'gitty up' command:
    - git pull
    - git add \*
    - git commit -m "(\<username\> - GittyUp)"
    - git push
<br><br>

* Push files to an SSRS server with the 'gitty ssrs' command
<br><br>

### INSTALLATION
* Clone this repository
* cd to it
* type 'pip install .'

### DEPENDENCIES
* Gitty relies primarily on packages 'gitpython' and 'suds'
* Python2.6 users will need to manually install 'gitpython' using easy_installer (pip won't work)

### CONFIGURATION
* Use the config.json file to configure ssrs endpoints 
* config.json can be found relative to your python directory at '/Lib/site-packages/gitty/config.json'
* When adding ssrs servers to the config you may leave the username and password blank and you will be prompted at run time



