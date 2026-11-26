"""Maintain discovery entries for the five published English water accessories."""
import argparse
from pathlib import Path

START = '<!-- EN_WATER_ACCESSORIES_START -->'
END = '<!-- EN_WATER_ACCESSORIES_END -->'
ROOT_URL = 'https://www.yuchensy.com/en/'
PRODUCTS = (
    ('housing-union', 'Filter housing union adapter',
     'Removable union with a 1-inch male threaded housing end and a PP-R heat-fusion socket marked 25. Confirm the thread standard, required pipe outside diameter and supplied seal and nut.'),
    ('reducing-elbow', 'Push-fit reducing elbow',
     '90-degree threaded-to-PE push-fit elbow. The 1/2-inch version is on the left in the product photo and the 3/8-inch version is on the right. Confirm the thread standard and tube outside diameter.'),
    ('inline-pressure-reducing-valve', 'Inline pressure-reducing valve',
     'Inline valve for water purifier feed lines. Confirm flow direction, inlet and outlet tube sizes, allowable inlet pressure and outlet setting for the specific valve.'),
    ('four-port-valve', 'Four-port valve',
     'Four ports marked 3/8 inch. Use the manufacturer’s model-specific circuit diagram to verify port assignments and switching conditions.'),
    ('leak-shutoff-device', 'Leak shutoff device',
     'Water-triggered shutoff device that does not require electrical power, according to the supplier. Confirm tube size, placement, reset procedure and the role of the pictured disc.'),
)


def update(source, full):
    lines = [START, '## Water filtration fittings and valves · English']
    for slug, title, detail in PRODUCTS:
        link = f'[{title}]({ROOT_URL}{slug}.html)'
        lines.append(f'- {link}' + (f' — {detail}' if full else ''))
    section = '\n'.join([*lines, END]) + '\n'
    if START in source or END in source:
        if source.count(START) != 1 or source.count(END) != 1:
            raise ValueError('Ambiguous accessory discovery section')
        before, remainder = source.split(START, 1)
        _, after = remainder.split(END + '\n', 1)
        return before + section + after
    marker = '<!-- PRODUCT_TAXONOMY_V2_END -->\n'
    if source.count(marker) != 1:
        raise ValueError('Missing unique product taxonomy boundary')
    return source.replace(marker, marker + '\n' + section, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    for name in ('llms.txt', 'llms-full.txt'):
        path = args.directory / name
        original = path.read_bytes().decode()
        updated = update(original, name == 'llms-full.txt')
        if updated != original:
            path.write_bytes(updated.encode())


if __name__ == '__main__':
    main()
