import argparse
import subprocess
from .step1_SNVcalling import *
from .step2_annotation_based import *
from .step3_dsRNA_based import *


def run():
    parser = argparse.ArgumentParser(description='Get candidate double-stranded RNA')
    parser.add_argument('-s', '--SNV_PATH',default = str(os.getcwd()),  help='path to output directory (default:~/)')
    parser.add_argument('-o', '--RES_PATH',default = str(os.getcwd()),  help='path to output directory (default:~/)')
    parser.add_argument('-r1', '--read1', help='path to reference FASTA file (default:~/reference.fa)')
    parser.add_argument('-r2', '--read2', help='path to reference FASTA file (default:~/reference.fa)')
    parser.add_argument('-r', '--Reference_file', help='path to reference FASTA file (default:~/reference.fa)')
    parser.add_argument('-rp', '--Repeat_file',  help='path to transcript annotation GTF file #Optional')
    parser.add_argument('-b', '--bwa',default = str(os.getcwd())+"blat",  help='path to blat (default:~/blat)')
    parser.add_argument('-B', '--bedtools',default = str(os.getcwd())+"bedtools",  help='path to bedtools (default:~/bedtools)')
    parser.add_argument('-S', '--samtools',default = str(os.getcwd())+"bedtools",  help='path to bedtools (default:~/bedtools)')
    parser.add_argument('-ds', '--Candidate_dsRNA',default = str(os.getcwd())+"Low_complex.txt",  help='path to output Low_complex.txt (default:~/Low_complex.txt)')
    parser.add_argument('-p', '--cpu',default=1,  help='CPU number (default=1)')
    args = parser.parse_args()

    step1_SNVcalling.main("-o "+args.SNV_PATH+" -r1 "+args.read1+" -r2 "+args.read2+" -R "+args.Reference_file+" -b "+args.bwa+" -B "+args.bedtools+" -s "+args.samtools+" -p "+args.cpu)
    step2_annotation_based.main("-o "+args.RES_PATH+" -s "+args.SNV_PATH+" -rp "+args.Repeat_file)
    step3_dsRNA_based.main("-o "+args.RES_PATH+" -s "+args.SNV_PATH+" -ds "+args.Candidate_dsRNA+" -b "+args.bedtools+" -p "+args.cpu)


if __name__ == '__main__':
    run()
