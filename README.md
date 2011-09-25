### So what the heck is PABE?

Based on [nabe](http://github.com/mklabs/nabe) and it stands for PABE = Probably An Other Blog Engine (in python)

### How to install it?

First you need to have some prerequisites 

* markdown
* gitpython
* pygments
* web.py

Install them using the following command:


    sudo easy_install markdown gitpython pygments web.py


Then run pabe:

    python pabe.py

### Adding articles

Add articles in the `articles` directory. Their structure has to be like this:

    Title: Your title here
    Author: Jhon Smith
    Date: 10:00 25/09/2011
    Tags: one, two, three
    Categories: python, programming
    Content HERE

Initialize a repository inside that directory:

    git init

You can create a `bare` repository if you want.

### License?

Just like nabe, it's based on the DWTFYWT Public License:

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

    Copyright (C) 2008 Simon Rozet <simon@rozet.name>
    Everyone is permitted to copy and distribute verbatim or modified
    copies of this license document, and changing it is allowed as long
    as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

    0. You just DO WHAT THE FUCK YOU WANT TO.

### Thanks to

Of course [mklabs](http://github.com/mklabs) :)
