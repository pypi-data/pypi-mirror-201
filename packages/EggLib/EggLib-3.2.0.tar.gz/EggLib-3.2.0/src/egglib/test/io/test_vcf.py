"""
    Copyright 2023 Thomas Coudoux, Stéphane De Mita, Mathieu Siol

    This file is part of EggLib.

    EggLib is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EggLib is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with EggLib.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest, egglib, pathlib, tempfile, os, shutil
path = pathlib.Path(__file__).parent / '..' / 'data'

class VCF_test(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.d.name)

    def tearDown(self):
        del self.d

    def test_fname(self):
        egglib.io.VCF(str(path / 'b.vcf')) # RuntimeError if htslib is off
        egglib.io.VCF(str(path / 'b.bcf'))
        with self.assertRaisesRegex(OSError, 'cannot open file: .+not\.exist'):
            egglib.io.VCF(str(path / 'not.exist'))
        with self.assertRaisesRegex(ValueError, 'invalid file: .+b\.gff3'):
            egglib.io.VCF(str(path / 'b.gff3'))

    def test_index_default(self): # (only supported on BCF)
        shutil.copyfile(path / 'b.bcf', self.path / 'b.bcf')
        vcf = egglib.io.VCF(str(self.path / 'b.bcf'))
        self.assertFalse(vcf.has_index)
        egglib.io.index_vcf(str(self.path / 'b.bcf'))
        vcf = egglib.io.VCF(str(self.path / 'b.bcf'))
        self.assertTrue(vcf.has_index)

    def test_index_custom(self):
        shutil.copyfile(path / 'b.bcf', self.path / 'b.bcf')
        vcf = egglib.io.VCF(str(self.path / 'b.bcf'))
        self.assertFalse(vcf.has_index)
        egglib.io.index_vcf(str(self.path / 'b.bcf'), str(self.path / 'index'))
        vcf = egglib.io.VCF(str(self.path / 'b.bcf'))
        self.assertFalse(vcf.has_index)
        vcf = egglib.io.VCF(str(self.path / 'b.bcf'), index=str(self.path / 'index'))
        self.assertTrue(vcf.has_index)

    def test_ctor_args(self):
        with self.assertRaisesRegex(ValueError, 'cannot import index from: .+not\.exist'):
            egglib.io.VCF(fname=str(path / 'b.bcf'),
                          index=str(path / 'not.exist'))

        self.assertTrue((path / 'b.gff3').is_file())
        with self.assertRaisesRegex(ValueError, 'cannot import index from: .+b\.gff3'):
            egglib.io.VCF(fname=str(path / 'b.bcf'),
                          index=str(path / 'b.gff3'))

        for ext in 'vcf', 'bcf':
            vcf = egglib.io.VCF(fname=str(path / f'b.{ext}'))
            self.assertEqual(vcf.num_samples, 4)
            self.assertEqual(vcf.get_samples(), ['INDIV1', 'INDIV2', 'INDIV3', 'INDIV4'])

        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=['INDIV1', 'INDIV3', 'INDIV2', 'INDIV4'])
        self.assertEqual(vcf.num_samples, 4)
        self.assertEqual(vcf.get_samples(), ['INDIV1', 'INDIV2', 'INDIV3', 'INDIV4'])

        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=['INDIV2', 'INDIV1', 'INDIV1', 'INDIV4'])
        self.assertEqual(vcf.num_samples, 3)
        self.assertEqual(vcf.get_samples(), ['INDIV1', 'INDIV2', 'INDIV4'])

        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=['INDIV2', 'INDIV4'])
        self.assertEqual(vcf.num_samples, 2)
        self.assertEqual(vcf.get_samples(), ['INDIV2', 'INDIV4'])

        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=[])
        self.assertEqual(vcf.num_samples, 0)
        self.assertEqual(vcf.get_samples(), [])

        with self.assertRaisesRegex(ValueError, 'unknown sample at position 5'):
            vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=['INDIV1', 'INDIV2', 'INDIV3', 'INDIV4', 'INDIV5'])

        with self.assertRaisesRegex(TypeError, 'subset: expect a sequence of strings'):
            vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=1)

        with self.assertRaisesRegex(TypeError, 'subset: expect a sequence of strings'):
            vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), subset=['INDIV1', 1])

    def test_samples(self):
        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'))
        self.assertEqual([vcf.get_sample(i) for i in range(4)], ['INDIV1', 'INDIV2', 'INDIV3', 'INDIV4'])
        with self.assertRaisesRegex(IndexError, 'sample index out of range'):
            vcf.get_sample(4)

    def test_defaults(self):
        for ext in 'vcf', 'bcf':
            vcf = egglib.io.VCF(fname=str(path / f'b.{ext}'))
            self.assertIsNone(vcf.get_id())
            self.assertIsNone(vcf.get_alleles())
            self.assertIsNone(vcf.get_alternate())
            self.assertIsNone(vcf.get_chrom())
            self.assertIsNone(vcf.get_filter())
            self.assertIsNone(vcf.get_formats())
            self.assertIsNone(vcf.get_genotypes())
            self.assertIsNone(vcf.get_infos())
            self.assertIsNone(vcf.get_phased())
            self.assertIsNone(vcf.get_pos())
            self.assertIsNone(vcf.get_quality())
            self.assertIsNone(vcf.get_reference())
            self.assertIsNone(vcf.get_types())
            self.assertFalse(vcf.is_snp())
            self.assertIsNone(vcf.get_errors())
            self.assertIsNone(vcf.get_info('NO.SUCH.TAG'))
            self.assertIsNone(vcf.get_format('NO.SUCH.TAG', 0))

    def compare_values(self, ctrl, v1, v2, idx, k):
        if isinstance(ctrl, list):
            self.assertEqual(len(ctrl), len(v1), msg=f'site index: {idx+1} - {k}')
            self.assertEqual(len(ctrl), len(v2), msg=f'site index: {idx+1} - {k}')
            for i in range(len(ctrl)):
                self.compare_values_i(ctrl[i], v1[i], v2[i], idx, k, tag=f' item #{i+1}')
        else:
            self.compare_values_i(ctrl, v1, v2, idx, k, tag='')

    def compare_values_i(self, ctrl, v1, v2, idx, k, tag):
        if ctrl is None:
            self.assertIsNone(v1, msg=f'site index: {idx+1} - {k}{tag}')
            self.assertIsNone(v2, msg=f'site index: {idx+1} - {k}{tag}')
        elif isinstance(ctrl, float):
            self.assertAlmostEqual(ctrl, v1, msg=f'site index: {idx+1} - {k}', places=6)
            self.assertAlmostEqual(ctrl, v2, msg=f'site index: {idx+1} - {k}', places=6)
        else:
            self.assertEqual(ctrl, v1, msg=f'site index: {idx+1} - {k}')
            self.assertEqual(ctrl, v2, msg=f'site index: {idx+1} - {k}')

    def test_get_info(self):
        ref_infos = [
            {'DP': 100, 'V': [4], 'W': [41, None], 'AA': 'AA', 'BIDON': 'G',
             'ALT':['.'], 'X': 0.2, 'Y': [1.2], 'GOOD': True, 'INT': None},
            {'AA': 'A', 'TRUC': [407, 12]},
            {'AA': 'C', 'P': [4.13]},
            {'AA': 'C', 'ALT': 'G,C'}, # strings can not represented as multiple values
            {'AA': 'G', 'P': [5.3, None, 3.001]},
            {'AA': 'G', 'TRUC': [None, 500400300]},
            {'AA': 'G', 'DP': None},
            {'AA': 'C', 'ALT': '.'}, # string missing values are not recognized
            {'AA': 'CTC', 'TRUC': [20, None]},
            {'AA': 'A', 'TRI': [1, 2], 'ALT': 'C,G,T', 'GOOD': True},
            {'AA': 'A', 'ALT': '.'}
        ]

        for ext in 'vcf', 'bcf':
            vcf = egglib.io.VCF(fname=str(path / f'b.{ext}'))

            for idx, ref in enumerate(ref_infos):
                self.assertTrue(vcf.read(), msg=f'site index: {idx+1}')
                infos = vcf.get_infos()
                self.assertEqual(infos.keys(), ref.keys(), msg=f'site index: {idx+1}')
                with self.assertRaisesRegex(ValueError, 'invalid info key: NOT.EXIST'):
                    vcf.get_info('NOT.EXIST')
                for k, ctrl in ref.items():
                    v1 = infos[k]
                    v2 = vcf.get_info(k)
                    self.compare_values(ctrl, v1, v2, idx, k)
            self.assertFalse(vcf.read())

    def test_get_format(self):
        ref_format = [
            {},
            {'TEST1': [None, 1, None, None]},
            {'TEST2': [[1, 2], [1, None], [None], [1]]},
            {'TEST3': [0.1, 0.2, None, 0.4]},
            {'TEST4': [[None], [0.2], [0.1, 0.2, 0.3, 0.1], [6]]},
            {'TEST5': ['hipidop', 'a string', 'hap', 'hipidop']},
            {},
            {},
            {},
            {'TEST5': ['.', 'nothing', 'not more', 'something!'],
             'TEST1': [702, 703, 704, 705]},
            {}
        ]

        for ext in 'vcf', 'bcf':
            vcf = egglib.io.VCF(fname=str(path / f'b.{ext}'))

            for idx, ref in enumerate(ref_format):
                self.assertTrue(vcf.read(), msg=f'site index: {idx+1}')
                fmts = vcf.get_formats()
                self.assertIsInstance(fmts, list, msg=f'site index: {idx+1}')
                self.assertEqual(len(fmts), 4, msg=f'site index: {idx+1}')
                for idv, fmt in enumerate(fmts):
                    self.assertEqual(fmt.keys(), ref.keys(), msg=f'site index: {idx+1}')
                    for key, ctrl in ref.items():
                        self.compare_values(ctrl[idv], fmt[key], vcf.get_format(key, idv), idx, key)

                with self.assertRaisesRegex(ValueError, 'invalid format key: NOT.EXIST'):
                    vcf.get_format('NOT.EXIST', 0)
                if len(ref) > 0:
                    with self.assertRaisesRegex(IndexError, 'sample index out of range'):
                        vcf.get_format(list(ref)[0], 4)
                    self.assertEqual(vcf.get_format(list(ref)[0], -1),
                                     vcf.get_format(list(ref)[0], 3))
                    self.assertEqual(vcf.get_format(list(ref)[0], -2),
                                     vcf.get_format(list(ref)[0], 2))
                    self.assertEqual(vcf.get_format(list(ref)[0], -3),
                                     vcf.get_format(list(ref)[0], 1))
                    self.assertEqual(vcf.get_format(list(ref)[0], -4),
                                     vcf.get_format(list(ref)[0], 0))
                    with self.assertRaisesRegex(IndexError, 'sample index out of range'):
                        vcf.get_format(list(ref)[0], -5)

            self.assertFalse(vcf.read())

    def test_error(self):
        for ext in 'vcf', 'bcf':
            vcf = egglib.io.VCF(fname=str(path / f'b.{ext}'))
            while vcf.read():
                self.assertEqual(vcf.get_errors(), [])

        s = ('##fileformat=VCFv4.2\n'
             '##contig=<ID=ctg1,len=1000>\n'
             '##INFO=<ID=FLOAT,Number=1,Type=Float,Description="Something">\n'
             '##FORMAT=<ID=INT,Number=1,Type=Integer,Description="Something else">\n'
             '#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	INDIV1	INDIV2	INDIV3	INDIV4\n'
             'ctg1	10	.	A	.	.	PASS	FLOAT=1	INT	1	2	3	4\n'
             'ctg1	20	.	A	.	.	PASS	FLOAT=1.1;DOUBLE=4.5	INT	1	2	3	4\n'
             'ctg1	30	.	A	.	.	PASS	FLOAT=1.1	INT	1	2	XXX	4\n'
             'ctg1	40	.	A	.	.	PASS	FLOAT=1.5	INT	1	2	3	4\n')

        with open(self.path / 'tmp.vcf', 'w') as f:
            f.write(s)

        vcf = egglib.io.VCF(fname=str(self.path / 'tmp.vcf'))
        self.assertTrue(vcf.read())
        self.assertEqual(vcf.get_errors(), [])
        self.assertTrue(vcf.read())
        self.assertGreater(len(vcf.get_errors()), 0)
        with self.assertRaisesRegex(ValueError, 'critical error while reading a variant'):
            vcf.read()
        self.assertTrue(vcf.read())
        self.assertEqual(vcf.get_errors(), [])
        self.assertFalse(vcf.read())

    def helper_test_goto(self, vcf:egglib.io.VCF,
                ctg:str, pos:int = None, limit:str = None,
                expected_ctg_error:bool = False,
                expected_pos_error:bool = False,
                expected_position:int = None):
        if expected_ctg_error:
            with self.assertRaisesRegex(ValueError, f'unknown target name: {ctg}'):
                if pos is None: vcf.goto(ctg)
                elif limit is None: vcf.goto(ctg, pos)
                else: vcf.goto(ctg, pos, limit)
            return
        if expected_pos_error:
            with self.assertRaisesRegex(ValueError, f'position not found: {pos}'):
                if limit is None: vcf.goto(ctg, pos)
                else: vcf.goto(ctg, pos, limit)
            return
        if pos is None: vcf.goto(ctg)
        elif limit is None: vcf.goto(ctg, pos)
        else: vcf.goto(ctg, pos, limit)
        self.assertEqual(vcf.get_chrom(), ctg)
        if expected_position is None and pos is not None:
            expected_position = pos
        if expected_position is not None:
            self.assertEqual(vcf.get_pos(), expected_position)

    def test_goto(self):
        # load without index
        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'))
        with self.assertRaisesRegex(ValueError, 'an index is required'):
            vcf.goto('ctg2')

        # create index and load
        idx = str(path / 'idx')
        egglib.io.index_vcf(str(path / 'b.bcf'), idx)
        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), index=idx)
        self.assertTrue(vcf.has_index)

        # go to a contig
        self.helper_test_goto(vcf, 'ctg2', expected_position=1014)

        # next pos
        self.assertTrue(vcf.read())
        self.assertEqual(vcf.get_chrom(), 'ctg2')
        self.assertEqual(vcf.get_pos(), 1015)

        # go to a position
        self.helper_test_goto(vcf, 'ctg2', 1049)

        # go to an invalid contig
        self.helper_test_goto(vcf, 'ctgN', expected_ctg_error=True)

        # go back near beginning
        self.helper_test_goto(vcf, 'ctg1', 1000)

        # reopen and go to first position of first contig
        vcf = egglib.io.VCF(fname=str(path / 'b.bcf'), index=idx)
        self.helper_test_goto(vcf, 'ctg1', expected_position=999)

        # go to a non-existing position and fix with limit
        self.helper_test_goto(vcf, 'ctg2', 1017, expected_pos_error=True)
        self.helper_test_goto(vcf, 'ctg2', 1017, limit=1019, expected_pos_error=True)
        self.helper_test_goto(vcf, 'ctg2', 1017, limit=1020, expected_position=1019)
        self.helper_test_goto(vcf, 'ctg3', 1067, limit=egglib.io.VCF.END, expected_position=1099)

        with self.assertRaisesRegex(ValueError, '`limit` must be larger than `pos`'):
            self.helper_test_goto(vcf, 'ctg2', 1019, limit=1019)
        with self.assertRaises(TypeError):
            self.helper_test_goto(vcf, 'ctg2', 1019, limit='END')
        with self.assertRaisesRegex(ValueError, '`limit` must be strictly positive'):
            self.helper_test_goto(vcf, 'ctg2', 1019, limit=-10)

        # another test
        self.helper_test_goto(vcf, 'ctg2', 1017, limit=egglib.io.VCF.END, expected_position=1019)

        # go past the end of a contig
        self.helper_test_goto(vcf, 'ctg2', 1200, expected_pos_error=True)
        self.helper_test_goto(vcf, 'ctg2', 1200, limit=1300, expected_pos_error=True)
        self.helper_test_goto(vcf, 'ctg2', 1200, limit=egglib.io.VCF.END, expected_pos_error=True)
        self.assertEqual(vcf.get_info(), None)

        # go back to actual beginning
        self.helper_test_goto(vcf, 'ctg1', expected_position=999)

        # go past the end of the file
        self.helper_test_goto(vcf, 'ctg3', 9999, expected_pos_error=True)
        self.helper_test_goto(vcf, 'ctg3', 9999, limit=10000, expected_pos_error=True)
        self.helper_test_goto(vcf, 'ctg3', 9999, limit=egglib.io.VCF.END, expected_pos_error=True)
        self.assertEqual(vcf.get_info(), None)

##### add methods to test accessors ####################################

accessor_data = {
    'chrom': ['ctg1', 'ctg1', 'ctg1', 'ctg1', 'ctg2', 'ctg2', 'ctg2', 'ctg2', 'ctg2', 'ctg3', 'ctg3'],
    'pos': [999, 1000, 1009, 1010, 1014, 1015, 1019, 1029, 1049, 1059, 1099],
    'id': [['snp1', 'first', 'zero'], ['snp11'], ['snp2'], ['snp21'], [],
           ['snp201', 'snp+'], ['snp3', 'snp3'], ['snp4'], ['snp5'], ['no_snp'], []],
    'reference': ['A', 'A', 'C', 'C', 'G', 'G', 'G', 'C', 'CTC', 'A', 'A'],
    'alternate': [['T'], ['AA'], ['G', 'T'], ['G', 'CTT'], ['TAA'],
                  ['GAA'], ['T'], ['A'], ['ATG'], ['C'], []],
    'alleles': [['A', 'T'], ['A', 'AA'], ['C', 'G', 'T'],
                ['C', 'G', 'CTT'], ['G', 'TAA'], ['G', 'GAA'],
                ['G', 'T'], ['C', 'A'], ['CTC', 'ATG'], ['A', 'C'], ['A']],
    'quality': [4, None, None, None, None, None, None, None, None, None, None],
    'filter': [[], [], ['triple'], ['triple', 'multi'], [], [], [], [], [], [], []],
    'errors': [[], [], [], [], [], [], [], [], [], [], []],
    'phased': [(True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [True], [True]]),
               (True, [[True], [True], [], [True]]),
               (False, [[True, True], [True, False], [False, False], [False, False]]),
               (False, [[True], [True], [False], [True]])],
    'types': [['SNP'], ['INDEL'], ['SNP'], ['SNP', 'INDEL'], ['OTHER'],
              ['INDEL'], ['SNP'], ['SNP'], ['MNP'], ['SNP'], []],
    'is_snp': [True, False, True, False, False, False, True, True, False, True, False],
    'genotypes': [
        [ ['A', 'A'], ['A', 'T'], ['A', 'A'], ['T', 'T'] ],
        [ ['A', 'A'], ['A', 'AA'], ['A', 'A'], ['AA', 'AA'] ],
        [ ['G', 'G'], ['C', 'G'], ['G', 'C'], ['T', 'T'] ],
        [ ['G', 'G'], ['C', 'G'], ['G', 'C'], ['CTT', 'CTT'] ],
        [ ['G', 'TAA'], ['TAA', 'TAA'], ['G', 'G'], ['G', 'G'] ],
        [ ['G', 'GAA'], ['GAA', 'GAA'], ['G', 'G'], ['G', 'G'] ],
        [ ['G', 'G'], ['G', 'T'], ['G', 'G'], ['T', 'T'] ],
        [ ['C', 'C'], ['C', 'A'], ['C', 'C'], ['A', 'A'] ],
        [ ['CTC', 'CTC'], ['CTC', 'ATG'], [None], ['ATG', 'ATG'] ],
        [ ['A', 'A', 'A'], ['A', 'A', 'A'], ['A', 'A', 'C'], ['A', 'C', 'C'] ],
        [ ['A', 'A'], ['A', None], [None, None], [None, None] ]
    ]
}

for what in accessor_data:
    def f(self, what=what):
        attr = what if what == 'is_snp' else f'get_{what}'
        for ext in 'vcf', 'bcf':
            vcf = egglib.io.VCF(fname=str(path / f'b.{ext}'))
            for i, v in enumerate(accessor_data[what]):
                self.assertTrue(vcf.read(), msg=f'read() returned False extension={ext} variant=#{i+1} what={what}')
                val = getattr(vcf, attr)()
                self.assertEqual(val, v,
                    msg=f'extension={ext} variant=#{i+1} what={what} exp={v} received={val}')
            self.assertFalse(vcf.read(), msg=f'extra read() returned True extension={ext} what={what}')
    setattr(VCF_test, f'test_{what}', f)
