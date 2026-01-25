import os
import sys
import subprocess

VERSIONS= [
[
'1.14.4',
'1.14.4-pre7',
'1.14.4-pre6',
'1.14.4-pre5',
'1.14.4-pre4',
'1.14.4-pre3',
'1.14.4-pre2',
'1.14.4-pre1',
'1.14.3',
'1.14.3-pre4',
'1.14.3-pre3',
'1.14.3-pre2',
'1.14.3-pre1',
'1.14.2',
'1.14.2 Pre-Release 4',
'1.14.2 Pre-Release 3',
'1.14.2 Pre-Release 2',
'1.14.2 Pre-Release 1',
'1.14.1',
'1.14.1 Pre-Release 2',
'1.14.1 Pre-Release 1',
'1.14',
'1.14 Pre-Release 5',
'1.14 Pre-Release 4',
'1.14 Pre-Release 3',
'1.14 Pre-Release 2',
'1.14 Pre-Release 1',
'19w14b',
'19w14a',
'19w13b',
'19w13a',
'19w12b',
'19w12a',
'19w11b',
'19w11a',
'19w09a',
'19w08b',
'19w08a',
'19w07a',
'19w06a',
'19w05a',
'19w04b',
'19w04a',
'19w03c',
'19w03b',
'19w03a',
'19w02a',
'18w50a',
'18w49a',
'18w48b',
'18w48a',
'18w47b',
'18w47a',
'18w46a',
'18w45a',
'18w44a',
'18w43c',
'18w43b'
],
[
'19w13b',
'3D Shareware v1.34'
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
