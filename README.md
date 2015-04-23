# qgis-moor-tools-plugin
Tools for simplifying and automating common tasks for national parks and other protected areas.


Status
------

Although fully functional, this plugin has not yet been polished for release. As a result, some manual configuration is needed for the plugin to work as designed.

Please note this plugin has been developed for very specific use cases and as such may require further work to make it more generic to suit users' wider requirements. Please feel free to create GitHub *issues* for reporting any bugs, queries or feature requests.


Setup
-----

**Start-up Projects**

A configuration file is used to define the list of projects to display to the user on start-up. The path to this file should be specified in the variable `configFilePath` (line 51 in projectselectordialog.py) and defaults to examples\project_selector_config.txt under the plugin's folder.

Each line of the configuration file should take the form:
        
    Label|Path to .qgs file|Selected by default? (0 or 1)


Notice the pipe character (|) used to delimit fields, for example:

    Default Project|Z:\Path\To\Projects\default.qgs|1

Will set the default project to *Z:\Path\To\Projects\default.qgs* with the label *Default Project*. Only one row should end with a 1, all other rows should end in a zero.

**Template Configuration**

The path to a folder containing templates should be specified in the variable `self.templateFileRoot`. This folder should contain a number of .qpt files (print composer templates) and a copyright configuration file called *copyright_selector_config.txt*.

Each line of *copyright_selector_config.txt* should look like:

    Aerial 2006|© Copyright Cartographic Engineering 2006|0

This is a pipe-delimited group of (1) Label, (2) copyright message to be displayed and (3) whether this is the default option (0/1).
