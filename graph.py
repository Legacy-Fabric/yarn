import os
import sys
import subprocess

VERSIONS= [
[
'1.3.2',
'1.4.7',
'1.5.2',
'1.6.4',
'1.7.10',
'1.8.9',
'1.9.4',
'1.10.2',
'1.11.2',
'1.12.2',
'1.13.2'
],
[
'1.8.9',
'1.8.8',
'1.8.7',
'1.8.6',
'1.8.5',
'1.8.4',
'1.8.3',
'1.8.2',
'1.8.2-pre7',
'1.8.2-pre6',
'1.8.2-pre5',
'1.8.2-pre4',
'1.8.2-pre3',
'1.8.2-pre2',
'1.8.2-pre1',
'1.8.1',
'1.8.1-pre5',
'1.8.1-pre4',
'1.8.1-pre3',
'1.8.1-pre2',
'1.8.1-pre1',
'1.8'
],
[
'1.8.3','15w14a'
],
[
'1.7.10',
'1.7.10-pre4',
'1.7.10-pre3',
'1.7.10-pre2',
'1.7.10-pre1',
'1.7.8',
'1.7.7',
'1.7.6',
'1.7.6-pre2',
'1.7.6-pre1',
'1.7.5',
'1.7.4',
'1.7.3',
'1.7.2',
'1.7.1',
'1.7'
],
[
'1.6.4',
'1.6.3',
'1.6.2',
'1.6.1',
'1.6'
],
[
'1.5.2',
'1.5.1',
'1.5'
],
[
'1.4.7',
'1.4.6',
'1.4.5',
'1.4.4',
'1.4.3',
'1.4.2',
'1.4.1',
'1.4'
],
[
'1.3.2',
'1.3.1',
'1.3'
]
]
ROOT = VERSIONS[0][0]

def main():
	args = sys.argv
	
	if len(args) == 0:
		raise Exception('no command given!')
	
	command = args[1]
	
	if command == 'generate':
		if len(args) == 2:
			generate(ROOT, VERSIONS)
		else:
			root = args[2]
			versions = args[3:]
			
			generate(root, versions)
	elif command == 'extend':
		if len(args) > 3:
			frm = args[2:-1]
			to = args[-1]
			
			extend(frm, to)
		else:
			raise Exception('too few arguments for extend command')
	else:
		raise Exception('unknown command ' + command)

def generate(root, mc_versions):
	os.environ['MC_VERSION'] = root
	subprocess.run("./gradlew refreshGraph --stacktrace", shell = True, check = True)
	
	for versions in mc_versions:
		for i in range(1, len(versions)):
			frm = versions[i - 1]
			to = versions[i]
			
			if '|' not in to:
				extend(frm.split('|'), to)

def extend(frm, to):
	os.environ['FROM_MC_VERSIONS'] = ','.join(frm)
	os.environ['MC_VERSION'] = to
	
	subprocess.run("./gradlew extendGraph --stacktrace", shell = True, check = True)

if __name__ == '__main__':
	main()
