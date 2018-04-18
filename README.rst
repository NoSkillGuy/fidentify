
F-Identify (Face Identify)
##########################

Python Script to identify a known face in a video.

Contents

.. contents:: :local:

Summary
=======

This is a command line python program to identify a known face in a video built using dlib's 
state-of-art face recognition with deep learning. You can also invoke this script 
from another python file.

This is a small and ready-to-run program. There are two dependencies that will get installed 
when you install this repo.
1. open-cv
2. facerecognition

Compatability
=============

This program is compatible with both the versions of python - 2.x and 3.x (recommended).
It is a download-and-run program with no changes to the file.
You will just have to specify parameters through the command line.

Installation
============

You can use **one of the below methods** to download and use this repository.

Using pip

.. code-block:: bash

    $ pip install fidentify

Manually using CLI

.. code-block:: bash

    $ git clone https://github.com/NoSkillGuy/fidentify.git
    $ cd fidentify && sudo python setup.py install

Manually using UI

Go to the `repo on github <https://github.com/NoSkillGuy/fidentify>`__ ==> Click on 'Clone or Download' ==> Click on 'Download ZIP' and save it on your local disk.

Usage - Using Command Line Interface
====================================

If installed via pip or using CLI, use the following command:

.. code-block:: bash

    $ fidentify [Arguments...]

If downloaded via the UI, unzip the file downloaded, go to the 'fidentify' directory and use one of the below commands:

.. code-block:: bash

    $ python3 fidentify.py [Arguments...]
    OR
    $ python fidentify.py [Arguments...]


Usage - From another python file
================================

If you would want to use this library from another python file, you could use it as shown below:

.. code-block:: python

    from fidentify import fidentify

    fidentify_obj = fidentify.fidentify()
    fidentify_obj.identify({<Arguments...>})


Arguments
=========

+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| Argument          | Short hand  | Description                                                                                                                   |
+===================+=============+===============================================================================================================================+
| config_file       | cf          | You can pass the arguments inside a config file. This is an alternative to passing arguments on the command line directly.    |
|                   |             |                                                                                                                               |
|                   |             | Please refer to the                                                                                                           |
|                   |             | `config file format <https://github.com/NoSkillGuy/fidentify/blob/master/README.rst#config-file-format>`__ below              |
|                   |             |                                                                                                                               |
|                   |             | * If 'config_file' argument is present, the program will use the config file and command line arguments will be discarded     |
|                   |             | * Config file can only be in **JSON** format                                                                                  |
|                   |             | * Please refrain from passing invalid arguments from config file. Refer to the below arguments list                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| known_images_path | kip         | Specify the `known images path`. This path should contain images only from these whitelisted formats (jpg, png, gif, bmp).    |
|                   |             | The name of the person is syntactically drawn from the filename without the extension.                                        |
|                   |             | Default known_images_path - 'images/'                                                                                         |
|                   |             | Example:                                                                                                                      |
|                   |             |         - If the file name is Steve Jobs.png, then the name derived is Steve Jobs                                             |
|                   |             |         - If the file name is Elon Musk.png, then the name derived is Elon Musk                                               |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| videos_path       | vp          | The path of the video folder, videos are directly picked from the folder and searches for all the knonw faces listed in       |
|                   |             | known_images_path.                                                                                                            |
|                   |             | NOTE: video path should be full path. Example: for ~/downloads use $HOME/downloads.                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| download_path     | dp          | This is the place where all your fidentify downloads will be located.                                                         |
|                   |             | The path will be auto created if the given download_path doesn't exist.                                                       |
|                   |             | Default download path - `downloads/`                                                                                          |
|                   |             |                                                                                                                               |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| download_format   | df          | Denotes the format/extension of the file that will be downnloaded                                                             |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: json, CSV, inline`                                                                                          |
|                   |             | `Default Value: inline`                                                                                                       |
|                   |             |                                                                                                                               |
|                   |             | If the -df argument is mentioned either `json` or `CSV` and -dp is not metioned `downloads/` path is auto created in the      |
|                   |             | current working directory                                                                                                     |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| help              | h           | show the help message regarding the usage of the above arguments                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+

Config File Format
==================

You can either pass the arguments directly from the command as in the examples below or you can pass it through a config file. Below is a sample of how a config
file looks.

You can pass more than one record through a config file. The below sample consist of two set of records. The code will iterate through each of the record and
download images based on arguments passed.

.. code:: json

    {
        "Arguments":
        {
            "known_images_path": "/users/NoSkillGuy/mysites/fidentify/paths/images_path",
            "videos_path": "/users/NoSkillGuy/mysites/fidentify/paths/videos_path"
            "download_path": "/users/NoSkillGuy/mysites/fidentify/downloads",
            "download_format": "json"
        }
    }


Examples
========

- If you are calling this library from another python file, below is the sample code

.. code-block:: python

    from fidentify import fidentify   #importing the library

    response = fidentify.fidentify()   #class instantiation

    arguments = {
        "known_images_path": "/users/NoSkillGuy/mysites/fidentify/images",
        "download_path":"/users/NoSkillGuy/mysites/fidentify/downloads",
        "download_format":"json"
    }   #creating list of arguments
    
    response.capture(arguments)   #passing the arguments to the function


- If you are passing arguments from a config file, simply pass the config_file argument with name of your JSON file

.. code-block:: bash

    $ fidentify -cf example.json

- Simple example of using arguments

.. code-block:: bash

    $ fidentify --known_images_path /users/NoSkillGuy/mysites/fidentify/images --download_path /users/NoSkillGuy/mysites/fidentify/downloads --download_format json

-  To use the short hand command

.. code-block:: bash

    $ fidentify --kip /users/NoSkillGuy/mysites/fidentify/images --dp /users/NoSkillGuy/mysites/fidentify/downloads --df json

--------------

Troubleshooting
===============

**## fidentify: command not found**

While using the above commands, if you get ``Error: -bash: fidentify: command not found`` then you have to set the correct path variable.

To get the details of the repo, run the following command:

.. code-block:: bash

    $ pip show -f fidentify 

you will get the result like this:

.. code-block:: bash

    Location: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
    Files:
      ../../../bin/fidentify

together they make: ``/Library/Frameworks/Python.framework/Versions/2.7/bin`` which you need add it to the path:

.. code-block:: bash

    $ export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin"


**## [Errno 13] Permission denied creating directory 'downloads'**

When you run the command, it downloads the images in the current directory (the directory from where you are running the command). If you get permission denied error for creating the `downloads directory`, then move to a directory in which you have the write permission and then run the command again.


**## Permission denied while installing the library**

On MAC and Linux, when you get permission denied when installing the library using pip, try doing a user install.

.. code-block:: bash

    $ pip install fidentify --user

You can also run pip install as a superuser with ``sudo pip install fidentify`` but it is not generally a good idea because it can cause issues with your system-level packages.

Contribute
==========

Anyone is welcomed to contribute to this script.
If you would like to make a change, open a pull request.
For issues and discussion visit the
`Issue Tracker <https://github.com/NoSkillGuy/fidentify/issues>`__.

In Development
==============

If this project gets 10 Stars, then i will work on the following 

1. Now it checks every frame of the video. should make this optional. Like how many frames you want to check per second. 
2. Documentation 
3. Examples
4. Tests

Use Cases
=========

1. Suspect Detection: Lets say there is a robbery, we got all the security camera videos, then we can easily check the videos if any known suspect is responsible for the robbery.
2. Someone Missing: Someone went missing, Police can easily get all the security camera videos and then they will automatically know where all places the missing person is.