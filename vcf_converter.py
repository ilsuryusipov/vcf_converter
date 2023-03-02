import os

import configparser


config = configparser.ConfigParser()
config.read('./vcf_converter.ini')


def parse_vcf_raw_data(vcf_raw_data: str) -> list[str]:
    vcf_blocks = []
    for block in vcf_raw_data.split('END:VCARD'):
        _block = block.split('BEGIN:VCARD')
        if len(_block) > 1:
            block = _block[1].strip()
            vcf_blocks.append(block)
        else:
            continue
    return vcf_blocks


def parse_vcf_block(vcf_blocks: list[str]) -> list[dict]:
    record = {
        'FN': None,
        'TEL': None
    }
    rows = vcf_blocks.split('\n')
    for row in rows:
        if row.startswith('FN:'):
            record['FN'] = row.split(':')[1].strip('\n').strip(' ')
            continue
        if row.startswith('TEL;TYPE=Мобильный:'):
            record['TEL'] = row.split(':')[1].strip('\n').strip(' ')
            continue
        if row.startswith('TEL:'):
            record['TEL'] = row.split(':')[1].strip('\n').strip(' ')
            continue
    return record


def convert():
    input_files = config['DEFAULT']['input_files'].split(' ')
    for input_file in input_files:
        output_file = f"{os.path.splitext(input_file)[0]}_converted.txt"
        with open(input_file) as vcf_file:
            vcf_raw_data = vcf_file.read()
            vcf_blocks = parse_vcf_raw_data(vcf_raw_data)
            vcf_records = list(map(parse_vcf_block, vcf_blocks))
            with open(output_file, 'w') as result_file:
                for record in vcf_records:
                    result_file.write(config['DEFAULT']['output_row_format'].format(**record) + '\n')


if __name__ == '__main__':
    convert()
