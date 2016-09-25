# Updates *.jar files after compiling with NetBeans.
# Placed in main folder.

import os
import shutil

jars = ['exttools.jar', 'jpcap.jar', 'mina-core.jar', 'mysql-connector-java-bin.jar', 'slf4j-api.jar', 'slf4j-jdk14.jar', 'XiuzSource.jar']

for jar in jars:
	os.remove('dist/' + jar)
	if jar == 'xiuzsource.jar':
		shutil.copy('nbdist/xiuzsource.jar', 'dist/' + jar)
	else:
		shutil.copy('nbdist/lib/' + jar, 'dist/' + jar)

print("Jars successfully updated!")