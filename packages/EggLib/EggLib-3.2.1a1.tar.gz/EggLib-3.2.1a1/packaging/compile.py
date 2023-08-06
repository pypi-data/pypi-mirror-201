import subprocess, sys, os, shutil, platform

# list of python 3 sub-versions to compile for
minor_versions = 7, 8, 9, 10

# executable name on windows/posix
executable = os.path.join('Scripts' if platform.system()=='Windows' else 'bin', 'python')

# function to run a command
def run(args):
    ret = subprocess.run(args, shell=False)
    if ret.returncode != 0:
        sys.exit('an error occurred')

# get the script directory and move to EggLib to directory
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(path, '..'))

# run for all python versions
for v in minor_versions:
    version = f'3.{v}'
    print(f'### python {version} ###')

    # precleaning
    if os.path.isdir(f'venv-{version}'):
        shutil.rmtree(f'venv-{version}')

    if platform.system()=='Windows': cmd = ['py', f'-{version}']
    else: cmd = [f'python{version}']

    # compilation
    try:
        print('creating virtual environment')
        run(cmd + ['-m', 'venv', f'venv-{version}'])

        print('setting up environment')
        run([os.path.join(f'venv-{version}', executable), '-m', 'pip', 'install', '--upgrade', 'pip', 'wheel'])

        print('compiling')
        run([os.path.join(f'venv-{version}', executable), 'setup.py', 'build', 'bdist_wheel'])

    # clean environment directory
    finally:
        if os.path.isdir(f'venv-{version}'):
            shutil.rmtree(f'venv-{version}')

    # testing
    startpath = os.getcwd()
    try:
        print('creating virtual environment')
        run(cmd + ['-m', 'venv', f'venv-{version}-testing'])
        os.chdir(f'venv-{version}-testing')

        print('setting up environment')
        run([executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'wheel', 'scipy'])

        print('installing')
        run([executable, '-m', 'pip', 'install', 'egglib', '--no-index', '--find-links', os.path.join('..', 'dist')])

        print('testing')
        run([executable, os.path.join('..', 'test'), '-bictso', os.path.join('..', f'test-output-{version}.txt')])

    # clean environment directory
    finally:
        os.chdir(startpath)
        if os.path.isdir(f'venv-{version}-testing'):
            shutil.rmtree(f'venv-{version}-testing')
