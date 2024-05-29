import re


def date_tokenizer(dateIssued):
    ## PARSER DATUMU NEŽERE ROZSAHY DAT. NUTNO ROZDĚLIT, POTÉ PARSOVAT ZVLÁŠŤ. VÝSTUPEM JE DATEISSUED_START A DATEISSUED_END ##

    dateIssued_start = ''
    dateIssued_end = ''

    if (re.match(r'\d{4}-\d{4}', dateIssued)):
        ## rozmezí let ##
        dateIssued_start = re.sub(r'(\d{4})-\d{4}',
                                  r'\1',
                                  dateIssued)
        dateIssued_end = re.sub(r'\d{4}-(\d{4})',
                                  r'\1',
                                  dateIssued)
    
    elif (re.match(r'\d{1,2}\.-\d{1,2}.\d{4}', dateIssued)):
        ## rozmezí měsíců ##
        dateIssued_start = re.sub(r'(\d{1,2})\.-\d{1,2}\.(\d{4})',
                                  r'\1.\2',
                                  dateIssued)
        dateIssued_end   = re.sub(r'\d{1,2}\.-(\d{1,2})\.(\d{4})',
                                  r'\1.\2',
                                  dateIssued)
        
    elif (re.match(r'\d{1,2}.-\d{1,2}\.\d{1,2}\.\d{4}', dateIssued)):
        ## rozmezí dnů v ramci jednoho mesice ##
        dateIssued_start = re.sub(r'(\d{1,2})\.-\d{1,2}\.(\d{1,2}\.\d{4})',
                                  r'\1.\2',
                                  dateIssued)
        dateIssued_end = re.sub(r'\d{1,2}\.-(\d{1,2})\.(\d{1,2}\.\d{4})',
                                  r'\1.\2',
                                  dateIssued)
    elif (re.match(r'\d{1,2}.\d{1,2}.-\d{1,2}\.\d{1,2}\.\d{4}', dateIssued)):
        ## rozmezí dnů v ramci vice mesicu ##
        dateIssued_start = re.sub(r'(\d{1,2}\.\d{1,2})\.-\d{1,2}\.\d{1,2}\.(\d{4})',
                                  r'\1.\2',
                                  dateIssued)
        dateIssued_end = re.sub(r'\d{1,2}\.\d{1,2}\.-(\d{1,2}\.\d{1,2})\.(\d{4})',
                                  r'\1.\2',
                                  dateIssued)
    elif (re.match(r'\d{1,2}.\d{1,2}.\d{4}-\d{1,2}\.\d{1,2}\.\d{4}', dateIssued)):
        ## rozmezí dnů v ramci vice mesicu a let ##
        dateIssued_start = re.sub(r'(\d{1,2}\.\d{1,2}\.\d{4})-\d{1,2}\.\d{1,2}\.\d{4}',
                                  r'\1',
                                  dateIssued)
        dateIssued_end = re.sub(r'\d{1,2}\.\d{1,2}\.\d{4}-(\d{1,2}\.\d{1,2}\.\d{4})',
                                  r'\1',
                                  dateIssued)

    else:
        print('formát datumu', dateIssued, 'nerozpoznán!')
        dateIssued_start = None
        dateIssued_end = None
    
    return {
            'dateIssued_start': dateIssued_start,
            'dateIssued_end': dateIssued_end
            }


def get_dateIssued_format(dateIssued):

    ## POMOCÍ REGEXU ZJIŠŤUJE FORMÁT DATEISSUED DLE VZORCŮ UVEDENÝCH V PPP. VRACÍ VZOREC PARSOVATELNÝ MODULEM DATETIME ##

    date_time = ''
    date_format = ''

    if (re.match(r'\d{1,2}\.\d{4}', dateIssued)):
        date_time = '%m.%Y'
        date_format = 'mm.yyyy'

    elif (re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', dateIssued)):
        date_time = '%d.%m.%Y'
        date_format = 'dd.mm.yyyy'

    elif (re.match(r'\d{4}', dateIssued)):
        date_time = '%Y'
        date_format = 'yyyy'

    else:
        print('formát datumu', dateIssued, 'nerozpoznán!')
        date_time = None
        date_format = None

          
    return date_time, date_format
