import sys, os, glob, re, argparse, xlsxwriter
from pathlib import Path
from datetime import datetime
from lxml import etree


from metadata_class import Periodical, Monograph
import dateparse

version='0.2'

mets_ns = { 'mets': 'http://www.loc.gov/METS/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'mods': 'http://www.loc.gov/mods/v3',
            'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
            'premis': 'info:lc/xmlns/premis-v2',
            'xlink': 'http://www.w3.org/1999/xlink',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'copyrightMD': 'http://www.cdlib.org/inside/diglib/copyrightMD' }

def args():

    choices_perio = [item for item in Periodical().metadata]
    choices_mono = [item for item in Monograph().metadata]

    default_mono = ['multi_title', 'multi_uuid', 'volume_title', 'volume_uuid', 'ccnb', 'isbn', 'urnnbn']
    default_perio = ['title', 'title_uuid', 'ccnb', 'issn', 'volume_uuid', 'volume_year', 'volume_no', 'urnnbn', 'base_uuid', 'base_year', 'base_no', 'base_lvl']
    
    parser = argparse.ArgumentParser(
                                     description='Skript určený pro získání metadat z NDK balíčků a jejich zápis do Excel (xlsx) tabulky. Na adrese zadané v prvním argumentu rekurzivně vyhledá všechny soubory mets obsahující metadata, která zapíše do xlsx souboru uvedeného v druhém argumentu.'                                     
                                    )

    parser.add_argument('-s', '--source-mets-files', help="Cesta k adresáři s analyzovanými mets soubory.", metavar='/cesta/k/adresari', type=Path, required=True)
    parser.add_argument('-o', '--output_xlsx', help="Cesta k cílovému souboru včetně jeho názvu.", metavar='cesta/k/novemu/xlsx/souboru', type=Path, required=True)
    parser.add_argument('-d', '--parse-dateissued', help="V cílovém xlsx souboru vytvoří list se seznamem periodik a sloupci obsahujícími hodnoty formátované jako datumy.", action="store_true")
    parser.add_argument('-p', '--periodical-values', nargs='+', help="Povolené hodnoty (oddělujte mezerou): "+", ".join(choices_perio), choices=choices_perio, metavar='', default=default_perio)
    parser.add_argument('-m', '--monograph-values', nargs='+', help="Povolené hodnoty (oddělujte mezerou): "+", ".join(choices_mono), choices=choices_mono, metavar='', default=default_mono)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(version), help="Ukáže verzi skriptu a ukončí se.")

    args = parser.parse_args()
    mets_files = args.source_mets_files
    output_file = args.output_xlsx
    perio_vals = args.periodical_values
    mono_vals = args.monograph_values
    parsed = args.parse_dateissued

    return mets_files, output_file, perio_vals, mono_vals, parsed

def load_mets(path_to_mets):
    '''najde metsy na adrese zadané na vstupu a poskytne slovník {metsy: etree objekty} na výstupu'''

    list_of_mets_files = list(path_to_mets.glob('**/mets_*.xml'))
    list_of_parsed_mets = {mets:etree.parse(mets) for mets in list_of_mets_files}
                          
    
    return list_of_parsed_mets


def get_document_type(parsed_mets):
    '''na základě kořenového elementu určí typ dokumentu a jeho základní úroveň'''

    dtype = parsed_mets.xpath("/mets:mets/@TYPE", namespaces=mets_ns) # monografie nebo periodikum
    suppl = '' # bool
    multi = '' # bool

    match dtype[0]:
        case 'Monograph':
            if (hasXpath(parsed_mets, "//mods:mods[starts-with(@ID, 'MODS_TITLE')]")):
                multi = True
            else:
                multi = False
            if (hasXpath(parsed_mets, "//mods:mods[starts-with(@ID, 'MODS_SUPPL')]") and not hasXpath(parsed_mets, "//mods:mods[starts-with(@ID, 'MODS_VOLUME')]")):
                suppl = True
            else:
                suppl = False
        case 'Periodical':
            multi = False # periodikum vícesvazek neexistuje, nastavujeme na False a více se tím nezabýváme

            if (hasXpath(parsed_mets, "//mods:mods[starts-with(@ID, 'MODS_SUPPL')]") and not hasXpath(parsed_mets, "//mods:mods[starts-with(@ID, 'MODS_ISSUE')]")):
                suppl = True
            else:
                suppl = False
    
    
    return dtype[0], suppl, multi

    
def trim(dirty_string):
    clean_string = re.sub(r'\s|\n', r' ', dirty_string)
    return clean_string

def hasXpath(self, xpath):

    return self.xpath(xpath, namespaces=mets_ns)

def arrayToString(node):
    ''' Cílem je, aby z proměnné byl vždy string. Zajímá nás pouze první nalezená hodnota. Pokud se žádná nenalezla, proměnná musí zůstat prázdná '''
    
    if (type(node) == str):        
        return node
    elif (type(node) == list):   
        if (len(node)):
            stringified_node = node[0]
            return stringified_node
        else:
            node = ''
            return node

def write_to_xlsx(worksheet, dtype, opt_vals, list_of_parsed_mets):

    '''Zapisuje hodnoty do tabulky. Z hodnot na vstupu potřebujeme kromě worksheetu a seznamu metsů i typ dokumentu - abychom věděli, jakou třídu zavolat při vypsání záhlaví a při zakládání instance; a nastavené argumenty, abychom věděli, jaké hodnoty vypsat'''
    row=0
    col=0

    header_class = {}
    match dtype:
        case "Monograph":
            header_class = Monograph()
        case "Periodical":
            header_class = Periodical()
    for opt_val in opt_vals:
        header = header_class.metadata.get(opt_val, {}).get('name')
       # print(opt_val)
        worksheet.write(row, col, header)
        col +=1

    row=1 # nulty radek zabira header
    col=0
    
    for mets in list_of_parsed_mets:
        parsed_mets = list_of_parsed_mets[mets]
        metadata_instance = {}
        #if (get_document_type(parsed_mets)[1] == True):
        
        match dtype:
            case "Monograph":
                metadata_instance = Monograph(get_document_type(parsed_mets)[1])
            case "Periodical":
                metadata_instance = Periodical(get_document_type(parsed_mets)[1])
        
        # zde musim zjistit pomoci get_document_type(), zda obsahuje prilohu ci nikoli
        # pak zalozit instanci
        
        for opt_val in opt_vals:
            xpath = metadata_instance.metadata.get(opt_val, {}).get('xpath')
            biblio_value = get_value_from_xpath(parsed_mets, xpath)
            worksheet.write(row, col, biblio_value)
            col += 1
        row +=1
        col = 0
        # bude to iterace v iteraci, v rámci jednoho metsu musíme proiterovat všechny opt_vals a vyhodnotit přitom xpath
        # ve vnější iteraci musím navýšit row, ve vnitřní col
        
    worksheet.autofit()
    
def write_parsed_perio_to_xlsx(workbook, worksheet, list_of_parsed_mets):
    '''Zapisuje hodnoty do tabulky s formátovanými datumy.'''

    # zápis headeru
    worksheet.write(0, 0, Periodical().metadata.get('title', {}).get('name'))
    worksheet.write(0, 1, Periodical().metadata.get('urnnbn', {}).get('name'))
    worksheet.write(0, 2, Periodical().metadata.get('volume_year', {}).get('name'))
    worksheet.write(0, 3, Periodical().metadata.get('volume_no', {}).get('name'))
    worksheet.write(0, 4, 'zákl. dateIssued start')
    worksheet.write(0, 5, 'zákl. dateIssued konec')
    worksheet.write(0, 6, 'zákl. partNumber')

    row=1 # první řádek obsazuje header, sloupce mám zde napevno dané
    
    metadata_instance = {}
    
    for mets in list_of_parsed_mets:
        parsed_mets = list_of_parsed_mets[mets]
        metadata_instance = Periodical(get_document_type(parsed_mets)[1])

        # musíme rozdělit datumy s pomlčkou
        
        dateIssued_s = ''
        dateIssued_e = ''
        dateIssued = get_value_from_xpath(parsed_mets, metadata_instance.metadata.get('base_year', {}).get('xpath'))
        
        if (re.search(r'-', dateIssued)):
            dateIssued = dateparse.date_tokenizer(dateIssued)
            dateIssued_s = dateIssued['dateIssued_start']
            dateIssued_e = dateIssued['dateIssued_end']
        else:
            dateIssued_s = dateIssued
            dateIssued_e = dateIssued

        # zapisujeme ostatní hodnoty
        
        worksheet.write(row, 0, get_value_from_xpath(parsed_mets, metadata_instance.metadata.get('title', {}).get('xpath')))
        worksheet.write(row, 1, get_value_from_xpath(parsed_mets, metadata_instance.metadata.get('urnnbn', {}).get('xpath')))
        worksheet.write(row, 2, get_value_from_xpath(parsed_mets, metadata_instance.metadata.get('volume_year', {}).get('xpath')))
        worksheet.write(row, 3, get_value_from_xpath(parsed_mets, metadata_instance.metadata.get('volume_no', {}).get('xpath')))
        worksheet.write(row, 6, get_value_from_xpath(parsed_mets, metadata_instance.metadata.get('base_no', {}).get('xpath')))
        # zapisujeme datumy a parsujeme
        try:
            parsed_dateIssued_s = datetime.strptime(dateIssued_s, dateparse.get_dateIssued_format(dateIssued_s)[0])
            parsed_dateIssued_e = datetime.strptime(dateIssued_e, dateparse.get_dateIssued_format(dateIssued_e)[0])

            date_format_s = workbook.add_format({'num_format': dateparse.get_dateIssued_format(dateIssued_s)[1]})
            date_format_e = workbook.add_format({'num_format': dateparse.get_dateIssued_format(dateIssued_e)[1]})
            
            worksheet.write_datetime(row, 4, parsed_dateIssued_s, date_format_s)
            worksheet.write_datetime(row, 5, parsed_dateIssued_e, date_format_e)
        except:
            if (dateIssued == ''):
                print('{}: prázdné pole datumu, neanalyzuji!'.format(mets))
                worksheet.write(row, 4, 'prázdné')
                worksheet.write(row, 5, 'prázdné')            
            else:
            
                print('soubor {} obsahuje datum {}, které se nepodařilo analyzovat!'.format(mets, dateIssued), file=sys.stderr)
                worksheet.write(row, 4, 'chyba!')
                worksheet.write(row, 5, 'chyba!')

        
        
        row+=1
    worksheet.autofit()
def get_value_from_xpath(parsed_mets, xpath):
    '''získá hodnotu z xpath výrazu, udělá z ní string, zbaví jej bílých znaků'''

    biblio_val = parsed_mets.xpath(xpath, namespaces=mets_ns)
    biblio_val = arrayToString(biblio_val)
    biblio_val = trim(biblio_val)

    return biblio_val


def main():
    
    mets_files, output_file, perio_vals, mono_vals, parsed = args()

    list_of_parsed_mets = load_mets(mets_files)
    
    list_of_parsed_perio = {}
    list_of_parsed_mono = {}
    
    # potřebujeme vytřídit monografie od periodik
    
    for mets in list_of_parsed_mets:
        if (get_document_type(list_of_parsed_mets[mets])[0]) == 'Periodical':
            list_of_parsed_perio.update({mets: list_of_parsed_mets[mets]})
        elif (get_document_type(list_of_parsed_mets[mets])[0]) == 'Monograph':
            list_of_parsed_mono.update({mets: list_of_parsed_mets[mets]})
    

    workbook = xlsxwriter.Workbook(output_file) # vytvoří cílový soubor

    
    worksheet_mono = workbook.add_worksheet('Monografie') # vytvoří list pro monografie
    worksheet_perio = workbook.add_worksheet('Periodika') # vytvoří list pro periodika

    
    

    write_to_xlsx(worksheet_mono, 'Monograph', mono_vals, list_of_parsed_mono)
    write_to_xlsx(worksheet_perio, 'Periodical', perio_vals, list_of_parsed_perio)
    if (parsed == True):
        try:
            worksheet_parsed_perio = workbook.add_worksheet('Periodika datumy')
            write_parsed_perio_to_xlsx(workbook, worksheet_parsed_perio, list_of_parsed_perio)
        except:
            print("Nepodařilo se vytvořit list s formátovanými datumy!", file=sys.stderr)            

    workbook.close()
    

if __name__ == "__main__":
    main()
