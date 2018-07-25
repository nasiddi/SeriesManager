

class File:
    def __init__(self, location='', e_nr='', series_name='Series Name', e_name=''):
        self.location = location
        self.s_nr = ''
        self.e_nr = e_nr
        self.series_name = series_name
        self.e_name = e_name
        self.double = False
        self.triple = False

    def __str__(self):
        return {'location': self.location, 'series_name': self.series_name, 's_nr': self.s_nr,
                'e_nr': self.e_nr, 'e_name': self.e_name, 'field_selector': 'selectable', 'syncit': 'sync',
                'type_option': {'selected': 'Series', 'options': ['Series', 'HD', 'SD']},
                'episode_option': {'selected': 'Single', 'options': ['Single', 'Double', 'Triple']}}


