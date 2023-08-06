import pathlib, re, glob, os
import setuptools, sysconfig
from setuptools.command.build_ext import build_ext

##### GET VERSION ######################################################

with pathlib.Path('src', 'egglib', '__init__.py').open() as f:
    if mo := re.search('__version__ *= *[>:\'"]((\d+\.)\d\.\d+(?:a|b|rc)?\d+)', f.read()):
        version = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

##### OVERRIDE BUILD_EXT COMMAND #######################################

class build_ext2(build_ext):
    def run(self):
        # get the build path (there should be a better way to get it!)
        build_path = str(pathlib.Path(self.get_ext_fullpath('libegglib')).parent / 'egglib')
        self.library_dirs.append(build_path)

        # get egglib installation options (at some point, we should be able to use the --config-settings option)
        DEBUG = os.environ.get('DEBUG', '0')
        if DEBUG == '0':
            for ext in self.extensions: ext.extra_compile_args.extend(['-g', '-O3'])
        elif DEBUG == '1':
            for ext in self.extensions: ext.extra_compile_args.extend(['-g', '-O0'])
            for ext in self.extensions: ext.define_macros.append(('DEBUG', 1))
        else: raise ValueError(f'invalid value for DEBUG: {DEBUG} (accepted values are 0 and 1)')

        # idem for the options --no-htslib and --require-htslib
        HTSLIB = os.environ.get('HTSLIB', '2')
        if HTSLIB == '0':
            assert self.extensions[-1].name == 'egglib.io._vcfparser'
            del self.extensions[-1]
            super().run() # no error should occur
        elif HTSLIB == '1':
            super().run() # an error might occur but the user should be prepared
        elif HTSLIB == '2':
            try:
                super().run()
            except setuptools.errors.CompileError as e:
                print(e)
                assert self.extensions[-1].name == 'egglib.io._vcfparser'
                del self.extensions[-1]
                return
        else:
            raise ValueError(f'invalid value for HTSLIB: {HTSLIB} (accepted values are 0, 1 and 2)')

##### EXTENSION MODULES ################################################

lib = 'egglib' + str(pathlib.Path(sysconfig.get_config_var('EXT_SUFFIX')).stem)
cpath = pathlib.Path('src', 'cfiles')
cpppath = pathlib.Path('src', 'cppfiles')

def filelist(path, names, ext):
    return [path.joinpath(i).with_suffix(ext) for i in libfiles]

libegglib = setuptools.Extension('egglib.libegglib',
                    sources=[str(cpath.joinpath(n).with_suffix('.c')) for n in ['random']],
                    language='c')

random = setuptools.Extension('egglib.random',
                    sources=[str(cpath.joinpath('randomwrapper').with_suffix('.c'))],
                    language='c',
                    libraries = [lib],
                    extra_link_args = ["-Wl,-rpath=$ORIGIN/."])

vcf = setuptools.Extension('egglib.io._vcfparser',
                    sources=[str(cpath.joinpath('vcfwrapper').with_suffix('.c'))],
                    language='c',
                    libraries = [lib, 'hts'],
                    extra_link_args = ["-Wl,-rpath=$ORIGIN/."])

binding = setuptools.Extension('egglib._eggwrapper',
                    sources=glob.glob(str(pathlib.Path(cpppath, '*.cpp'))),
                    language='c++',
                    swig_opts=['-python', '-c++', '-builtin', '-Wall'],
                    include_dirs = [os.path.join('src', 'cfiles')],
                    libraries = [lib],
                    extra_link_args = ["-Wl,-rpath=$ORIGIN/."])

extensions = [libegglib, binding, random, vcf]

##### MAIN PACKAGE #####################################################

pkg_list = ['egglib',
            'egglib.cli',
            'egglib.test',
            'egglib.test.data',
            'egglib.test.base',
            'egglib.test.coalesce',
            'egglib.test.stats',
            'egglib.test.tools',
            'egglib.test.io',
            'egglib.test.wrappers',
            'egglib.coalesce',
            'egglib.io',
            'egglib.stats',
            'egglib.tools',
            'egglib.wrappers']

setuptools.setup(
    cmdclass={'build_ext': build_ext2},
    version=version,
    package_dir={'egglib': os.path.join(r'src', 'egglib')},
    packages=pkg_list,
    package_data={
        'egglib.wrappers': ['apps.conf'],
        'egglib.test.data': ['*.fas', '*.fa', '*.gb', '*.txt',
                             '*.gff3', '*.sta', '*.gnl', '*.fg',
                             '*.aln', '*.vcf', '*.vcfi', '*.bed',
                             '*.hap', '*.inp', '*.gpop', '*.cds',
                             '*.asnb', '*.bcf', '*.clu']},
    ext_modules=extensions
)
