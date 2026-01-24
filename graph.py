import os
import sys
import subprocess

VERSIONS= [
[
'18w43a',
'18w33a',
'18w32a',
'18w31a',
'18w30b',
'18w30a',
'1.13.2',
'1.13.1',
'1.13',
'1.13.2-pre2',
'1.13.2-pre1',
'1.13.1-pre2',
'1.13.1-pre1',
'1.13-pre10',
'1.13-pre9',
'1.13-pre8',
'1.13-pre7',
'1.13-pre6',
'1.13-pre5',
'1.13-pre4',
'1.13-pre3',
'1.13-pre2',
'1.13-pre1',
'18w22c',
'18w22b',
'18w22a',
'18w21b',
'18w21a',
'18w20c',
'18w20b',
'18w20a',
'18w19b',
'18w19a',
'18w16a',
'18w15a',
'18w14b',
'18w14a',
'18w11a',
'18w10d',
'18w10c',
'18w10b',
'18w10a',
'18w09a',
'18w08b',
'18w08a',
'18w07c',
'18w07b',
'18w07a',
'18w06a',
'18w05a',
'18w03b',
'18w03a',
'18w02a',
'18w01a',
'17w50a',
'17w49b',
'17w49a',
'17w48a',
'17w47b',
'17w47a',
'17w46a',
'17w45b',
'17w45a',
'17w43b',
'17w43a',
'1.12.2-pre2',
'1.12.2-pre1',
'1.12.1-pre1',
'1.12.2',
'1.12.1',
'1.12',
'1.12-pre7',
'1.12-pre6',
'1.12-pre5',
'1.12-pre4',
'1.12-pre3',
'1.12-pre2',
'1.12-pre1',
'17w31a',
'17w18b',
'17w18a',
'17w17b',
'17w17a',
'17w16b',
'17w16a',
'17w15a',
'17w14a',
'17w13b',
'17w13a',
'17w06a',
'16w50a',
'1.11-pre1',
'1.11.2',
'1.11.1',
'1.11',
'16w44a',
'16w43a',
'16w42a',
'16w41a',
'16w40a',
'16w39c',
'16w39b',
'16w39a',
'16w38a',
'16w36a',
'16w35a',
'16w33a',
'16w32b',
'16w32a',
'1.10.2',
'1.10.1',
'1.10',
'1.10-pre2',
'1.10-pre1',
'16w21b',
'16w21a',
'16w20a',
'1.9.3-pre3',
'1.9.3-pre2',
'1.9.3-pre1',
'16w15b',
'16w15a',
'16w14a',
'1.9.4',
'1.9.3',
'1.9.2',
'1.9.1',
'1.9',
'1.9.1-pre3',
'1.9.1-pre2',
'1.9.1-pre1',
'1.9-pre4',
'1.9-pre3',
'1.9-pre2',
'1.9-pre1',
'16w07b',
'16w07a',
'16w06a',
'16w05b',
'16w05a',
'16w04a',
'16w03a',
'16w02a',
'15w51b',
'15w51a',
'15w50a',
'15w49b',
'15w49a',
'15w47c',
'15w47b',
'15w47a',
'15w46a',
'15w45a',
'15w44b',
'15w44a',
'15w43c',
'15w43b',
'15w43a',
'15w42a',
'15w41b',
'15w41a',
'15w40b',
'15w40a',
'15w39c',
'15w39b',
'15w39a',
'15w38b',
'15w38a',
'15w37a',
'15w36d',
'15w36c',
'15w36b',
'15w36a',
'15w35e',
'15w35d',
'15w35c',
'15w35b',
'15w35a',
'15w34d',
'15w34c',
'15w34b',
'15w34a',
'15w33c',
'15w33b',
'15w33a',
'15w32c',
'15w32b',
'15w32a',
'15w31c',
'15w31b',
'15w31a',
'1.8.8',
'1.8.7',
'1.8.6',
'1.8.5',
'1.8.4',
'1.8.3',
'1.8.2',
'1.8.2-pre7',
'1.8.2-pre6',
'1.8.2-pre5'
],
[
'1.9.2','1.RV-Pre1'
],
[
'1.8.8','1.8.9'
],
[
'1.8.3','15w14a'
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
