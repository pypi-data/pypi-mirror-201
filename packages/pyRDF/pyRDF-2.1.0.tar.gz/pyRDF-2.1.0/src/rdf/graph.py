#!/usr/bin/env python

from rdf.terms import IRIRef


_GRAPHLABEL_DEFAULT = IRIRef('')

class Statement(tuple):
    """Statement"""

    subject = None
    predicate = None
    object = None
    graph_label = None

    def __new__(cls, subject, predicate, object, graph_label=None):
        if graph_label is None:
            graph_label = _GRAPHLABEL_DEFAULT

        return super().__new__(cls, (subject, predicate, object, graph_label))

    def __init__(self, subject, predicate, object, graph_label=None):
        self.subject = subject
        self.predicate = predicate
        self.object = object
        self.graph_label = graph_label if graph_label is not None\
                else _GRAPHLABEL_DEFAULT

    def __getnewargs__(self):
        return (self.subject, self.predicate, self.object, self.graph_label)

    def __iter__(self):
        if self.graph_label is _GRAPHLABEL_DEFAULT:
            return iter((self.subject, self.predicate, self.object))
        
        return iter((self.subject, self.predicate, self.object,
                     self.graph_label))

    def __eq__(self, other):
        for resourceA, resourceB in ((self.subject, other.subject),
                                     (self.predicate, other.predicate),
                                     (self.object, other.object),
                                     (self.graph_label, other.graph_label)):
            if resourceA != resourceB:
                return False

        return True

    def __lt__(self, other):
        # ordering following predicate logic: (s, p, o) := p(s, o)
        for resourceA, resourceB in ((self.predicate, other.predicate),
                                     (self.subject, other.subject),
                                     (self.object, other.object),
                                     (self.graph_label, other.graph_label)):
            if resourceA < resourceB:
                return True

        return False

    def __str__(self):
        out = "%s, %s, %s" % (str(self.subject),
                              str(self.predicate),
                              str(self.object))
        if self.graph_label is not _GRAPHLABEL_DEFAULT:
            out += ", %s" % str(self.graph_label)

        return "(" + out + ")"

    def __hash__(self):
        return hash(repr(self))
