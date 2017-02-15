#!/usr/bin/env python3

"""
Python 3.x.x

For those that compile with NetBeans, this script automatically
updates the server's working .jar files with the newly compiled
ones from /nbdist/.

Run this after compilation, once the server is not running.
"""

import os
import shutil

jars = ['exttools.jar', 'jpcap.jar', 'mina-core.jar',
        'mysql-connector-java-bin.jar',
        'slf4j-api.jar', 'slf4j-jdk14.jar',
        'JDA-3.0.BETA2_108-withDependencies.jar',
        'XiuzSource.jar']

for jar in jars:
    os.remove('dist/' + jar)
    if jar == 'XiuzSource.jar':
        shutil.copy2('nbdist/xiuzsource.jar', 'dist/' + jar)
    else:
        shutil.copy2('nbdist/lib/' + jar, 'dist/' + jar)

print('Jars updated successfully!')
