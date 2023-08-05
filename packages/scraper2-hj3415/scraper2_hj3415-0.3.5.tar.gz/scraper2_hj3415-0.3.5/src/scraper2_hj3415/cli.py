from .nfscrapy import run as nfsrun
from .miscrapy import run as mirun
from .krx import krx
from util_hj3415 import utils
import argparse


def miscraper():
    spiders = ['mihistory', 'mi']

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders}")

    parser.add_argument('-d', '--db_path', help="Set mongo database path")
    args = parser.parse_args()

    if args.spider in spiders:
        if args.spider == 'mihistory':
            years = 2
            print(f"We will collect MI data for past {years} years.")
            mirun.mi_history(years, args.db_path) if args.db_path else mirun.mi_history(years)
        elif args.spider == 'mi':
            mirun.mi_all(args.db_path) if args.db_path else mirun.mi_all()
    else:
        print(f"The spider option should be in {spiders}")


def nfscraper():
    spiders = ['c101', 'c106', 'c103', 'c104']

    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help=f"Spiders - {spiders}")
    parser.add_argument('target', help="Target for scraping (type 6digit code or 'all')")

    parser.add_argument('-d', '--db_path', help="Set mongo database path")
    args = parser.parse_args()

    if args.spider in spiders:
        if args.spider == 'c101':
            if args.target == 'all':
                nfsrun.c101(krx.get_codes(), args.db_path) if args.db_path else nfsrun.c101(krx.get_codes())
            elif utils.is_6digit(args.target):
                nfsrun.c101([args.target, ], args.db_path) if args.db_path else nfsrun.c101([args.target, ])
        if args.spider == 'c103':
            if args.target == 'all':
                x = input("It will take a long time. Are you sure? (y/N)")
                if x == 'y' or x == 'Y':
                    nfsrun.c103(krx.get_codes(), args.db_path) if args.db_path else nfsrun.c103(krx.get_codes())
            elif utils.is_6digit(args.target):
                nfsrun.c103([args.target, ], args.db_path) if args.db_path else nfsrun.c103([args.target, ])
        if args.spider == 'c104':
            if args.target == 'all':
                x = input("It will take a long time. Are you sure? (y/N)")
                if x == 'y' or x == 'Y':
                    nfsrun.c104(krx.get_codes(), args.db_path) if args.db_path else nfsrun.c104(krx.get_codes())
            elif utils.is_6digit(args.target):
                nfsrun.c104([args.target, ], args.db_path) if args.db_path else nfsrun.c104([args.target, ])
        if args.spider == 'c106':
            if args.target == 'all':
                nfsrun.c106(krx.get_codes(), args.db_path) if args.db_path else nfsrun.c106(krx.get_codes())
            elif utils.is_6digit(args.target):
                nfsrun.c106([args.target, ], args.db_path) if args.db_path else nfsrun.c106([args.target, ])
    else:
        print(f"The spider option should be in {spiders}")


def analyser():
    pass


if __name__ == '__main__':
    miscraper()
