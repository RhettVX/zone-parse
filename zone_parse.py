from argparse import ArgumentParser
from pathlib import Path

from ZoneStuff import Zone

if __name__ == '__main__':
    parser = ArgumentParser(description='A tool for exporting forgelight zones to json')
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    subcmd_export = sub_parsers.add_parser('export')
    subcmd_export.add_argument('path', nargs='+', help='.zones to export')
    subcmd_export.add_argument('-o', '--outdir', default='ZoneJSON',
                               help='directory to dump json output')

    # Handle the args
    args = parser.parse_args()
    zone_files = []
    if args.command == 'export':
        for path in [Path(p) for p in args.path]:
            if path.is_file():
                zone_files.append(path)
            elif path.is_dir():
                zone_files.extend(path.glob('*.zone'))

        outdir = Path(args.outdir)
        outdir.mkdir(exist_ok=True, parents=True)

        print('Exporting zones...')
        for path in zone_files:
            tmp_zone = Zone(path)
            tmp_zone.export_json(path.stem + '.json', Path(args.outdir))
