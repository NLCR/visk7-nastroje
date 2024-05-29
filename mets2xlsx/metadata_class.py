class Periodical:

    def __init__(self, suppl=False):
        self.suppl = suppl
        self.base_lvl = self.set_suppl()

        self.metadata = {

            'title': {
                'name': "Titul (TITLE)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:titleInfo/mods:title/text()"
                },
            'title_uuid': {
                'name': "UUID (TITLE)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:identifier[@type='uuid']/text()"
                },
            'ccnb': {
                'name': "Číslo ČNB",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:identifier[@type='ccnb']/text()"
                },
            'issn': {
                'name': "ISSN",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:identifier[@type='issn']/text()"
                },
            'record_source': {
                'name': "Zdrojový katal. záznam",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:recordInfo/mods:recordContentSource/text()"
                },
            'record_id': {
                'name': "ID zdroj. katal. záznamu",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:recordInfo/mods:recordIdentifier/text()"
                },
            'volume_no': {
                'name': "partNumber (VOLUME)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_VOLUME')]/mods:titleInfo/mods:partNumber/text()"
                },
            'volume_year': {
                'name': "dateIssued (VOLUME)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_VOLUME')]/mods:originInfo/mods:dateIssued/text()"
                },
            'volume_uuid': {
                'name': "UUID (VOLUME)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_VOLUME')]/mods:identifier[@type='uuid']/text()"
                },
            'urnnbn': {
                'name': "URNNBN (zákl.)",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:identifier[@type='urnnbn']/text()"
                },
            'base_no': {
                'name': "partNumber (zákl.)",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:titleInfo/mods:partNumber/text()"
                },
            'base_year': {
                'name': "dateIssued (zákl.)",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:originInfo/mods:dateIssued/text()"
                },
            'base_uuid': {
                'name': "UUID (zákl.)",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:identifier[@type='uuid']/text()"
                },
            'base_lvl': {
                'name': "Základní úroveň",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/@ID"
                }
            
            }

    def set_suppl(self):
        if (self.suppl == False):
            return 'MODS_ISSUE'
        else:
            return 'MODS_SUPPL'

           

class Monograph:
    
    def __init__(self, suppl=False):
        self.suppl = suppl
        self.base_lvl = self.set_suppl()

        self.metadata = {
            'multi_title': {
                'name': "Titul (TITLE)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:titleInfo/mods:title/text()"
                },
            'multi_uuid': {
                'name': "UUID (TITLE)",
                'xpath': "//mods:mods[starts-with(@ID, 'MODS_TITLE')]/mods:identifier[@type='uuid']/text()"
                },
            'volume_title': {
                'name': "Titul svazku",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:titleInfo/mods:title/text()"
                },
            'volume_uuid': {
                'name': "UUID svazku",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:identifier[@type='uuid']/text()"
                },
            'volume_no': {
                'name': "Číslo svazku",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:titleInfo/mods:partNumber/text()"
                },
            'volume_year': {
                'name': "Datum svazku",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:originInfo/mods:dateIssued/text()"
                },
            'ccnb': {
                'name': "Číslo ČNB",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:identifier[@type='ccnb']/text()"
                },
            'isbn': {
                'name': "ISBN",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:identifier[@type='isbn']/text()"
                },
            'urnnbn': {
                'name': "URNNBN",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:identifier[@type='urnnbn']/text()"
                },
            'record_source': {
                'name': "Zdrojový katal. záznam",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:recordInfo/mods:recordContentSource/text()"
                },
            'record_id': {
                'name': "ID zdroj. katal. záznamu",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/mods:recordInfo/mods:recordIdentifier/text()"
                },
            'base_lvl': {
                'name': "Základní úroveň",
                'xpath': "//mods:mods[starts-with(@ID, '"+ self.base_lvl +"')]/@ID"
                }
            
            }

    def set_suppl(self):        
        if (self.suppl == False):
            return 'MODS_VOLUME'
        else:
            return 'MODS_SUPPL' 

