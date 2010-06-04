Introduction
============

Sproutcore applications are deployed to a server from a local development area which
typically consists of several directories, apps, for the applications, and frameworks,
for dependencies of the applications. sc-build is run within the development area to
produce minified javascript and css files to tmp/build/sc. The sc directory contains
subdirectories for each app, storing the minified files under a "hash" directory. The
hash is a long alphanumeric string, unique for each build, and doubling as the name
of the containing directory. For example, after sc-build, you could have this for a
Sproutcore app called myapp:

        ../project/tmp/build/sc/myapp/myapp/en/bb2cb971f4f39dab7bdcfb7707ca1d24188a503/

and in this "hash" directory, you might find:

    * index.html
    * javascript.js

For deployment, you would cd to ../project/tmp/build/, then:

        tar cvfz mysc.tgz sc

You would then have a tarball with your app, as minified files, ready for deploying to
a server. On the server, you would have a directory for the website associated with
this app, and a subdirectory ready to hold the app. This subdirectory would probably
be proxied to a URL, such that if you explode the tarball there, you would be ready
to serve up the Sproutcore application. There is a last step though, for which you
need to pay attention to where you explode the tarball, containing the hierarchy you
see above (sc/myapp/myapp/en/bb2cb971f4f39dab7bdcfb7707ca1d24188a503) and files within 
it. One of the files inside the hash directory is index.html, which includes links to
the hiearchy down to the hash directory files. This index.html needs to be copied to
the proxied directory for your server environment, and it must be done so that the
paths work. After you figure out how to arrange things, you'll have the repetive task
of making a tarball, uploading it, exploding it in the right directory, and moving or 
symlinking the index.html to a proxied directory, each time you need to update the
live app.  If you have more than one Sproutcore app, this can get really tedious. So,
deployment scripts are needed.

Fabric
------

Fabric is a Python library for ssh-type administrative tasks locally and on servers.
Fabric is described at: http://docs.fabfile.org/0.9.1/. It works well for performing
the steps described above, both on the local development system and the server.

This fabfile.py
---------------

Fabric uses a simple scheme, wherein tasks, written as Python methods, are stored in
a fabfile.py file. You could put many such tash methods, along with other Python code,
in a single fabfile.py. You run a task by typing 'fab task' on the command line, which
would find and run the task() method in fabfile.py.

In the example shown here, Fabric is used to deploy multiple Sproutcore apps to a single
server, where johndoe has a normal user account with sudoer privledges. The deployment
directory is a Django project directory, where Django apps live along with Sproutcore
apps. nginx is used to proxy URLs to specific Django and Sproutcore app directories.
For each Sproutcore app, our task is to deploy the fresh sc tarball and copy out 
index.html for each app to the proxied directory.

This fabfile.py is put in a deploy directory at the top level of a Sproutcore project
(in with Buildfile, apps, frameworks) on a local development machine. 

NOTE: This code assumes Python 2.6 or later. If you are using Python 2.5 or earlier,
you'll need to import the new Python *with* statement in a special way described on 
the Fabric web site.

1. Make a tarball of ../tmp/build/sc

2. Send it up to the server, to johndoe's home dir

3. Move it to the django project dir, where django apps and sc and sc apps live

4. Move old sc out of the way

5. Explode tarball to new sc

6. For each Sproutcore app, copy out the index.html to the proxied dir

You run it by issuing 'fab deploy'. fabric picks up the deploy() method defined here.
You will see reports as the Fabric commands are executed, and will see errors as they 
happen. Once working, you might still have some admin tasks to do on the server
before each deployment.
