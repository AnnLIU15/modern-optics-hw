from scripts import get_spd
from glob import glob
import argparse





def main(args):
    if args.base_dir == None:
        raise TypeError('please add the --base_dir flag to run the code')
    for base_dir in args.base_dir:
        save_dir = 'outputs/' + \
            '_'.join(base_dir.replace('\\','/').split('/'))+\
                '_SPD/'
        all_file = glob(base_dir+'/*.csv' ) + glob(base_dir+'/*.txt' )
        get_spd(csv_path=all_file,
                if_show = False,
                base_dir=save_dir)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir',type=str,nargs='+',
                        help='python get_folder_spd.py --base_dir data\CIE_illum data\LAMP')
    args = parser.parse_args()
    main(args=args)
