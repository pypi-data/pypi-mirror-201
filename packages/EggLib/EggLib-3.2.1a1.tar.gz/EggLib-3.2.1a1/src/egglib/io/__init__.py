"""
    Copyright 2015-2023 Stephane De Mita, Mathieu Siol

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

from ._ms import to_ms
from ._fasta import fasta_iter, from_fasta, from_fasta_string
from ._gff3 import GFF3, Gff3Feature
from ._vcf import VcfParser, VcfStringParser, VcfVariant, make_vcf_index, VcfSlidingWindow, VcfWindow, BED
from ._genbank import GenBank, GenBankFeature, GenBankFeatureLocation
from ._legacy import from_clustal, from_staden, from_genalys, get_fgenesh
from ._genepop import from_genepop
from .. import config

#: First available position of a contig.
FIRST = _vcf.FIRST

#: Last available position of a contig.
LAST = _vcf.LAST

try:
    from ._vcfparser import VCF, index_vcf
    config.htslib = 1
except ImportError:
    config.htslib = 0
    def VCF(*args, **kwargs):
        raise NotImplementedError('EggLib was compiled without htslib. Please refer to the installation instruction on https://egglib.org/install.html for more information.')
    def index_vcf(*args, **kwargs):
        raise NotImplementedError('EggLib was compiled without htslib. Please refer to the installation instruction on https://egglib.org/install.html for more information.')
