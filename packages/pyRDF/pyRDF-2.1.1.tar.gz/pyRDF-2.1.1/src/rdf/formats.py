#!/usr/bin/env python

from abc import ABC, abstractmethod
from io import BytesIO, StringIO, TextIOWrapper
import os
from sys import stdout

from rdf.graph import Statement
from rdf.terms import Entity, Literal, BNode, IRIRef, Resource


FORMAT_EXTENSION_MAP = {'ntriples': '.nt', 'nquads': '.nq'}

class RDF_Serialization_Format(ABC):
    """
    General RDF streamer class

    This class is the base class that deals with reading and writung RDF data.
    Normal use is to instantiate one of the subclasses.
    """

    mode = None
    path = None
    _file = None

    def __init__(self, path=None, mode='r', data=None, encoding='utf-8',
                 format="ntriples"):
        self.mode = mode
        self.path = path

        if self.path is None:
            if self.mode == 'r':
                if data is not None:
                    if isinstance(data, str):
                        self._file = StringIO(data)
                    else:  # bytes
                        self._file = TextIOWrapper(BytesIO(data),
                                                   encoding=encoding)
                else:
                    raise Exception("No input source provided")
            elif self.mode == 'w':
                self._file = stdout
            else:
                raise Exception("Unsupported mode: {}".format(self.mode))
        else:
            ext = FORMAT_EXTENSION_MAP[format]
            _, fext = os.path.splitext(self.path)
            if fext != ext:
                raise Warning(f"Expected {ext} format but got {fext} instead")

            self._file = open(self.path, self.mode, encoding=encoding)

    def parse(self):
        for statement in self._file:
            statement = statement.strip()
            if len(statement) <= 0 or statement.startswith('#'):
                continue

            try:
                yield self._parse_statement(statement)
            except:
                raise Exception("Line does not conform to format "\
                                + "specifications: " + statement)

        self._file.seek(0)

    def write(self, statement):
        if type(statement) is tuple:
            statement = Statement(*statement)

        self._file.write(self._serialize_statement(statement) + '\n')

    def close(self):
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    ## Parse functions #####################################

    @abstractmethod
    def _parse_statement(self, statement):
        pass

    def _strip_comment(self, statement):
        for i in range(1, len(statement)):
            if statement[-i] == '#':
                break

        return statement[:-i]

    def _parse_subject(self, statement):
        if statement.startswith("_:"):
            return self._parse_bnode(statement)
        else:  # iriref
            return self._parse_iriref(statement)

    def _parse_predicate(self, statement):
        return self._parse_iriref(statement)

    def _parse_bnode(self, statement):
        entity, remainder = self._parse_entity(statement)
        bnode = entity.value
        if bnode.startswith('_:'):
            bnode = BNode(bnode[2:])
        else:
            raise Exception("Unsuspected format: " + bnode)

        return (bnode, remainder)

    def _parse_graph_label(self, statement):
        if statement.startswith("_:"):
            return self._parse_bnode(statement)
        else:  # iriref
            return self._parse_iriref(statement)

    def _parse_iriref(self, statement):
        entity, remainder = self._parse_entity(statement)
        iriref = entity.value
        if iriref.startswith('<'):
            iriref = IRIRef(iriref[1:-1])
        else:
            raise Exception("Unsuspected format: " + iriref)

        return (iriref, remainder)

    def _parse_entity(self, statement):
        i = 0
        while i < len(statement) and statement[i] not in [u'\u0009', u'\u0020']:
            i += 1

        return (Entity(statement[:i]), statement[i+1:].lstrip())
    
    def _parse_resource(self, statement):
        i = 0
        inside_string = False
        while i < len(statement):
            if not inside_string and statement[i] in [u'\u0009', u'\u0020']:
                # check for white space outside of strings
                break

            if statement[i] == '"' and not (i > 0 and statement[i-1] == '\\'):
                # TODO: check if needs escape
                # if we start or end a string
                # account for possible escaped quotation marks
                inside_string = not inside_string

            i += 1

        return (Resource(statement[:i]), statement[i+1:].lstrip())

    def _parse_object(self, statement):
        resource, remainder = self._parse_resource(statement)
        resource = resource.value

        if resource.startswith('<'):
            object, _ = self._parse_iriref(resource)
            return (object, remainder)
        if resource.startswith("_:"):
            object, _ = self._parse_bnode(resource)
            return (object, remainder)
        if not resource.startswith('"'):
            raise Exception("Unsuspected format: " + resource)

        language = None
        datatype = None
        if resource.endswith('>'):
            # datatype declaration
            for i in range(len(resource)):
                if resource[-i] == '<':
                    break

            datatype = resource[-i+1:-1]
            resource = resource[:-i-2]  # omit ^^
        elif not resource.endswith('"'):
            # language tag
            for i in range(len(resource)):
                if resource[-i] == '@':
                    break

            language = resource[-i+1:]  # omit @-part
            resource = resource[:-i]
        elif not resource.endswith('"'):
            raise Exception("Unsuspected format: " + resource)

        return (Literal(resource, language=language, datatype=datatype),
                remainder)

    ## Serialization functions #####################################

    @abstractmethod
    def _serialize_statement(self, statement):
        pass

    def _serialize_subject(self, subject):
        if isinstance(subject, IRIRef):
            return self._serialize_iriref(subject)
        elif isinstance(subject, BNode):
            return self._serialize_bnode(subject)
        else:
            raise Exception("Unrecognised resource: " + subject)

    def _serialize_predicate(self, predicate):
        return self._serialize_iriref(predicate)

    def _serialize_object(self, object):
        if isinstance(object, IRIRef):
            return self._serialize_iriref(object)
        elif isinstance(object, BNode):
            return self._serialize_bnode(object)
        elif isinstance(object, Literal):
            # literal
            literal = '"' + object.value + '"'
            if object.language is not None:
                literal += '@' + object.language
            elif object.datatype is not None:
                literal += "^^" + self._serialize_iriref(object.datatype)

            return literal
        else:
            raise Exception("Unrecognised resource: " + object)

    def _serialize_graph_label(self, glabel):
        if isinstance(glabel, IRIRef):
            return self._serialize_iriref(glabel)
        elif isinstance(glabel, BNode):
            return self._serialize_bnode(glabel)
        else:
            raise Exception("Unrecognised resource: " + glabel)

    def _serialize_iriref(self, iriref):
        return '<' + iriref.value + '>'

    def _serialize_bnode(self, bnode):
        return '_:' + bnode.value

class NTriples(RDF_Serialization_Format):
    """N-Triples parser and serialization class"""

    def __init__(self, path=None, mode='r', data=None, encoding='utf-8'):
        super().__init__(path, mode, data, encoding, format="ntriples")

    ## Parse functions #####################################

    def _parse_statement(self, statement):
        statement = statement.rstrip(' ')
        if not statement.endswith('.'):
            statement = self._strip_comment(statement)
        statement = statement.rstrip(' .')

        subject, remainder = self._parse_subject(statement)
        predicate, remainder = self._parse_predicate(remainder)
        object, _ = self._parse_object(remainder)

        return Statement(subject, predicate, object)

    ## Serialization functions #####################################

    def _serialize_statement(self, statement):
        subject = self._serialize_subject(statement.subject)
        predicate = self._serialize_predicate(statement.predicate)
        object = self._serialize_object(statement.object)

        return subject + u'\u0020' + predicate + u'\u0020' + object + " ."

class NQuads(RDF_Serialization_Format):
    """N-Quads parser and serialization class"""

    def __init__(self, path=None, mode='r', data=None, encoding='utf-8'):
        super().__init__(path, mode, data, encoding, format="nquads")

    ## Parse functions #####################################

    def _parse_statement(self, statement):
        statement = statement.rstrip(' ')
        if not statement.endswith('.'):
            statement = self._strip_comment(statement)
        statement = statement.rstrip(' .')

        subject, remainder = self._parse_subject(statement)
        predicate, remainder = self._parse_predicate(remainder)
        object, remainder = self._parse_object(remainder)
        graph_label, _ = self._parse_graph_label(remainder)

        return Statement(subject, predicate, object, graph_label)

    ## Serialization functions #####################################

    def _serialize_statement(self, statement):
        subject = self._serialize_subject(statement.subject)
        predicate = self._serialize_predicate(statement.predicate)
        object = self._serialize_object(statement.object)
        graph_label = self._serialize_graph_label(statement.graph_label)

        return subject + u'\u0020' + predicate + u'\u0020' + object\
                + u'\u0020' + graph_label + " ."
