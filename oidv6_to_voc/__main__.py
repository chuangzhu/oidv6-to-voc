from . import convert
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Convert OIDv6 dataset to VOC XML format')
    parser.add_argument(
        'annotation',
        type=str,
        nargs='*',
        help='Annotation file(s), e.g. oidv6-train-annotations-bbox.csv')
    parser.add_argument(
        '-d',
        '--desc',
        type=str,
        required=True,
        help='Class description file, e.g. class-descriptions-boxable.csv')
    parser.add_argument('--imgd',
                        '-i',
                        type=str,
                        required=True,
                        help='Directory of dataset images')
    parser.add_argument('--outd',
                        '-o',
                        type=str,
                        default='converted.d',
                        help='Output directory')
    args = parser.parse_args()
    convert(args.annotation, args.desc, args.imgd, args.outd)

if __name__ == '__main__':
    main()
