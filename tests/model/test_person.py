from unittest import TestCase
from isatools.model.person import Person
from isatools.model.ontology_annotation import OntologyAnnotation


class TestPerson(TestCase):

    def setUp(self):
        self.person = Person()

    def test_init(self):
        person = Person(roles=['test_role'])
        self.assertTrue(person.roles == [])

        role = OntologyAnnotation(term='test_role')
        person = Person(roles=[role])
        self.assertTrue(person.roles == [role])

    def test_getters(self):
        self.assertTrue(self.person.id == '')
        self.assertTrue(self.person.last_name == '')

    def test_last_name(self):
        self.assertTrue(self.person.last_name == '')
        self.person.last_name = 'test_last_name'
        self.assertTrue(self.person.last_name == 'test_last_name')

        with self.assertRaises(AttributeError) as context:
            self.person.last_name = 1
        self.assertTrue("Person.last_name must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.last_name = None
        self.assertIsNone(self.person.last_name)

    def test_first_name(self):
        self.assertTrue(self.person.first_name == '')
        self.person.first_name = 'test_first_name'
        self.assertTrue(self.person.first_name == 'test_first_name')

        with self.assertRaises(AttributeError) as context:
            self.person.first_name = 1
        self.assertTrue("Person.first_name must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.first_name = None
        self.assertIsNone(self.person.first_name)

    def test_mid_initials_name(self):
        self.assertTrue(self.person.mid_initials == '')
        self.person.mid_initials = 'test_mid_initials'
        self.assertTrue(self.person.mid_initials == 'test_mid_initials')

        with self.assertRaises(AttributeError) as context:
            self.person.mid_initials = 1
        self.assertTrue("Person.mid_initials must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.mid_initials = None
        self.assertIsNone(self.person.mid_initials)

    def test_email(self):
        self.assertTrue(self.person.email == '')
        self.person.email = 'test_email'
        self.assertTrue(self.person.email == 'test_email')

        with self.assertRaises(AttributeError) as context:
            self.person.email = 1
        self.assertTrue("Person.email must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.email = None
        self.assertIsNone(self.person.email)

    def test_phone(self):
        self.assertTrue(self.person.phone == '')
        self.person.phone = 'test_phone'
        self.assertTrue(self.person.phone == 'test_phone')

        with self.assertRaises(AttributeError) as context:
            self.person.phone = 1
        self.assertTrue("Person.phone must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.phone = None
        self.assertIsNone(self.person.phone)

    def test_fax(self):
        self.assertTrue(self.person.fax == '')
        self.person.fax = 'test_fax'
        self.assertTrue(self.person.fax == 'test_fax')

        with self.assertRaises(AttributeError) as context:
            self.person.fax = 1
        self.assertTrue("Person.fax must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.fax = None
        self.assertIsNone(self.person.fax)

    def test_address(self):
        self.assertTrue(self.person.address == '')
        self.person.address = 'test_address'
        self.assertTrue(self.person.address == 'test_address')

        with self.assertRaises(AttributeError) as context:
            self.person.address = 1
        self.assertTrue("Person.address must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.address = None
        self.assertIsNone(self.person.address)

    def test_affiliation(self):
        self.assertTrue(self.person.affiliation == '')
        self.person.affiliation = 'test_affiliation'
        self.assertTrue(self.person.affiliation == 'test_affiliation')

        with self.assertRaises(AttributeError) as context:
            self.person.affiliation = 1
        self.assertTrue("Person.affiliation must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.person.affiliation = None
        self.assertIsNone(self.person.affiliation)

    def test_roles(self):
        self.assertTrue(self.person.roles == [])
        ontology_annotation = OntologyAnnotation(term='test_term',
                                                 term_accession="test_term_accession")
        self.person.roles = [ontology_annotation]
        self.assertTrue(isinstance(self.person.roles[0], OntologyAnnotation))
        self.assertTrue(self.person.roles[0].term == 'test_term')
        self.assertTrue(self.person.roles[0].term_accession == 'test_term_accession')

        expected_string = ("OntologyAnnotation(\n\t"
                           "term=test_term\n\t"
                           "term_source=None\n\t"
                           "term_accession=test_term_accession\n\t"
                           "comments=0 Comment objects\n)")
        self.assertTrue(str(self.person.roles[0]) == expected_string)

        with self.assertRaises(AttributeError) as context:
            self.person.roles = 1
        self.assertTrue("roles must be iterable containing OntologyAnnotations" in str(context.exception))

    def test_repr(self):
        expected_repr = ("isatools.model.Person(last_name='', first_name='', mid_initials='', "
                         "email='', phone='', fax='', address='', affiliation='', roles=[], comments=[])")
        self.assertTrue(repr(self.person) == expected_repr)
        self.assertTrue(hash(self.person) == hash(expected_repr))

    def test_str(self):
        expected_str = ("Person(\n\t"
                        "last_name=\n\t"
                        "first_name=\n\t"
                        "mid_initials=\n\t"
                        "email=\n\t"
                        "phone=\n\t"
                        "fax=\n\t"
                        "address=\n\t"
                        "affiliation=\n\t"
                        "roles=0 OntologyAnnotation objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.person) == expected_str)

    def test_equalities(self):
        a_person = Person(last_name='blog')
        b_person = Person(last_name='blog')
        self.assertTrue(a_person == b_person)
        self.assertTrue(a_person != self.person)
