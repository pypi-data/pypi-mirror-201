import os
import sys
import subprocess

from kmergenetyper import realignConsensus

def type_genes(args):
    check_for_kma()
    set_up_output_directory(args.output)
    collections = check_prefix_collisions(args)
    if args.illumina != []:
        args.illumina.sort()
        for i in range(0, len(args.illumina), 2):
            prefix = derive_prefix(args.illumina[i])
            if prefix in collections:
                prefix = prefix + '_illumina'
            input_seqs = ' '.join(args.illumina[i:i+2])
            os.system('kma -ipe {} -o {}/{} -t_db {} -ill -md {} -ID 95'.format(input_seqs, args.output, prefix, args.t_db, args.md))
            realignConsensus.realign_consensus(args.output, prefix, args.t_db, args.keep)
    if args.nanopore != []:
        for item in args.nanopore:
            prefix = derive_prefix(item)
            if prefix in collections:
                prefix = prefix + '_nanopore'
            os.system('kma -i {} -o {}/{} -t_db {} -ont -md {} -ID 95'.format(item, args.output, prefix, args.t_db, args.md))
            realignConsensus.realign_consensus(args.output, prefix, args.t_db, args.keep)

def check_prefix_collisions(args):
    prefixes = []
    collisions = []
    if args.illumina != []:
        for i in range(0, len(args.illumina), 2):
            prefix = derive_prefix(args.illumina[i])
            if prefix in prefixes:
                print ('Prefix {} is not unique. Output name has been modified.'.format(prefix))
                collisions.append(prefix)
            else:
                prefixes.append(prefix)
    if args.nanopore != []:
        for item in args.nanopore:
            prefix = derive_prefix(item)
            if prefix in prefixes:
                print ('Prefix {} is not unique. Output name has been modified.'.format(prefix))
                collisions.append(prefix)
            else:
                prefixes.append(prefix)
    return collisions
def derive_prefix(file):
    return os.path.basename(file).split('.')[0]

def set_up_output_directory(output):
    if not os.path.exists(output):
        os.makedirs(output)

def check_for_kma():
    """Checks if kma is installed"""
    try:
        subprocess.call(["kma"], stdout=open(os.devnull, 'wb'))
    except Exception:
        sys.exit("kma is not installed correctly directly in the PATH.")
