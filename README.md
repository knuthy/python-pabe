PABE = Probably An Other Blog Engine (in python)

You need:
* markdown (`easy_install markdown`)
* gitpython (`easy_install gitpython`)
* pygments (`easy_install pygments`)
* web.py (`easy_install web.py`)

To run the blog just do:

    python pabe.py

### Adding articles

Add articles in the `articles` directory. Their structure has to be like this:

    Title: Your title here
    Author: Jhon Smith
    Date: 10:00 25/09/2011
    Tags: one, two, three
    Categories: python, programming

Initialize a repository inside that directroy by doing:

    git init

You can create a bare repository

