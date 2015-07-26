OctoHub Contrib: Offline Issues
===============================

``offline-issues`` leverages OctoHub to download GitHub issues, and then
parses them into a directory structure of symlinks based on issue
metadata, such as labels and assignees::

    all/:issue.number
    state/:issue.state/:issue.title|slug       -> ../../all/:issue.number
    labels/:issue.label/:issue.title|slug      -> ../../all/:issue.number
    assignee/:assignee.login/:issue.title|slug -> ../../all/:issue.number

Setup
-----

Once OctoHub is installed, add the ``offline issues`` parser to your path::

    cd octohub
    ln -s $(pwd)/contrib/offline-issues/parse.py $HOME/bin/octohub-parse-issues

For each issue tracker or subset::

    ISSUES_DIR=path/to/project/issues
    mkdir -p $ISSUES_DIR

    cd octohub
    cp contrib/offline-issues/update.sh $ISSUES_DIR/
    cd $ISSUES_DIR
    
    # set ISSUES_URI to the desired issue listing
    # reference: http://developer.github.com/v3/issues
    vim update.sh 
    
    # optional, but useful to see what has changed between updates
    echo .raw > .gitignore
    git init
    git add .gitignore update.sh
    git commit -m 'initial commit'
    
    # if ISSUES_URI requires authentication
    export OCTOHUB_TOKEN=... 
    
    ./update.sh

