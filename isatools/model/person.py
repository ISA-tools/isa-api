from isatools.model.comments import Commentable
from isatools.model.ontologies import OntologyAnnotation


class Person(Commentable):
    """A person/contact that can be attributed to an Investigation or Study.

    Attributes:
        last_name: The last name of a person.
        first_name: The first name of a person.
        mid_initials: The middle initials of a person.
        email: The email address of a person.
        phone: The telephone number.
        fax: The fax number.
        address: The address of a person.
        affiliation: The organization affiliation for a person.
        roles: A list of Orole(s) performed by this person. Roles reported here
            need not correspond to roles held withing their affiliated
            organization.
        comments: Comments associated with instances of this class.
    """

    def __init__(self, last_name='', first_name='', mid_initials='', email='',
                 phone='', fax='', address='', affiliation='', roles=None,
                 comments=None, id_=''):
        super().__init__(comments)

        self.id = id_
        self.__last_name = last_name
        self.__first_name = first_name
        self.__mid_initials = mid_initials
        self.__email = email
        self.__phone = phone
        self.__fax = fax
        self.__address = address
        self.__affiliation = affiliation

        if roles is None:
            self.__roles = []
        else:
            self.__roles = roles

    @property
    def last_name(self):
        """:obj:`str`: the last_name of the person"""
        return self.__last_name

    @last_name.setter
    def last_name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.last_name must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__last_name = val

    @property
    def first_name(self):
        """:obj:`str`: the first_name of the person"""
        return self.__first_name

    @first_name.setter
    def first_name(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.first_name must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__first_name = val

    @property
    def mid_initials(self):
        """:obj:`str`: the mid_initials of the person"""
        return self.__mid_initials

    @mid_initials.setter
    def mid_initials(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.mid_initials must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__mid_initials = val

    @property
    def email(self):
        """:obj:`str`: the email of the person"""
        return self.__email

    @email.setter
    def email(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.email must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__email = val

    @property
    def phone(self):
        """:obj:`str`: the phone number of the person"""
        return self.__phone

    @phone.setter
    def phone(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.phone must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__phone = val

    @property
    def fax(self):
        """:obj:`str`: the fax number of the person"""
        return self.__fax

    @fax.setter
    def fax(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.fax must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__fax = val

    @property
    def address(self):
        """:obj:`str`: the address of the person"""
        return self.__address

    @address.setter
    def address(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.address must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__address = val

    @property
    def affiliation(self):
        """:obj:`str`: the affiliation of the person"""
        return self.__affiliation

    @affiliation.setter
    def affiliation(self, val):
        if val is not None and not isinstance(val, str):
            raise AttributeError(
                'Person.affiliation must be a str or None; got {0}:{1}'
                    .format(val, type(val)))
        else:
            self.__affiliation = val

    @property
    def roles(self):
        """:obj:`list` of :obj:`OntologyAnnotation`: Container for person roles
        """
        return self.__roles

    @roles.setter
    def roles(self, val):
        if val is not None and hasattr(val, '__iter__'):
            if val == [] or all(isinstance(x, OntologyAnnotation)
                                for x in val):
                self.__roles = list(val)
        else:
            raise AttributeError(
                '{0}.roles must be iterable containing OntologyAnnotations'
                    .format(type(self).__name__))

    def __repr__(self):
        return "isatools.model.Person(last_name='{person.last_name}', " \
               "first_name='{person.first_name}', " \
               "mid_initials='{person.mid_initials}', " \
               "email='{person.email}', phone='{person.phone}', " \
               "fax='{person.fax}', address='{person.address}', " \
               "affiliation='{person.affiliation}', roles={person.roles}, " \
               "comments={person.comments})" \
            .format(person=self)

    def __str__(self):
        return """Person(
    last_name={person.last_name}
    first_name={person.first_name}
    mid_initials={person.mid_initials}
    email={person.email}
    phone={person.phone}
    fax={person.fax}
    address={person.address}
    roles={num_roles} OntologyAnnotation objects
    comments={num_comments} Comment objects
)""".format(person=self,
            num_roles=len(self.roles),
            num_comments=len(self.comments))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return (isinstance(other, Person)
                and self.last_name == other.last_name
                and self.first_name == other.first_name
                and self.mid_initials == other.mid_initials
                and self.email == other.email
                and self.phone == other.phone
                and self.fax == other.fax
                and self.address == other.address
                and self.affiliation == other.affiliation
                and self.roles == other.roles
                and self.comments == other.comments)

    def __ne__(self, other):
        return not self == other
