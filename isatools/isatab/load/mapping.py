investigation_sections_mapping: dict[str, dict[str, str]] = {
    'ontology_sources': {
        'current_section_key': 'ONTOLOGY SOURCE REFERENCE',
        'next_section_key': 'INVESTIGATION'
    },
    'investigation': {
        'current_section_key': 'INVESTIGATION',
        'next_section_key': 'INVESTIGATION PUBLICATIONS'
    },
    'i_publications': {
        'current_section_key': 'INVESTIGATION PUBLICATIONS',
        'next_section_key': 'INVESTIGATION CONTACTS'
    },
    'i_contacts': {
        'current_section_key': 'INVESTIGATION CONTACTS',
        'next_section_key': 'STUDY'
    }
}


def get_investigation_base_output() -> dict[str, list]:
    return {
        'studies': [],
        's_design_descriptors': [],
        's_publications': [],
        's_factors': [],
        's_assays': [],
        's_protocols': [],
        's_contacts': [],
    }


study_sections_mapping: dict[str, dict[str, str]] = {
    'studies': {
        'current_section_key': 'STUDY',
        'next_section_key': 'STUDY DESIGN DESCRIPTORS'
    },
    's_design_descriptors': {
        'current_section_key': 'STUDY DESIGN DESCRIPTORS',
        'next_section_key': 'STUDY PUBLICATIONS'
    },
    's_publications': {
        'current_section_key': 'STUDY PUBLICATIONS',
        'next_section_key': 'STUDY FACTORS'
    },
    's_factors': {
        'current_section_key': 'STUDY FACTORS',
        'next_section_key': 'STUDY ASSAYS'
    },
    's_assays': {
        'current_section_key': 'STUDY ASSAYS',
        'next_section_key': 'STUDY PROTOCOLS'
    },
    's_protocols': {
        'current_section_key': 'STUDY PROTOCOLS',
        'next_section_key': 'STUDY CONTACTS'
    },
    's_contacts': {
        'current_section_key': 'STUDY CONTACTS',
        'next_section_key': 'STUDY'
    }
}