#!/usr/bin/env python

# This was cribbed from the tutorial at:
#  http://www.postneo.com/projects/pyxml/
# and subsequently extended based on:
#  http://www.boddie.org.uk/python/XML_intro.html

import xml.dom.minidom

namespace = ("http://www.jamestuttle.net/xmlns/group", "group")

def new_document(ns):
    """Create a new minidom XML document object populated with a root node

    Returns Document(), rootelement """

    # Instantiate a minidom document
    document = xml.dom.minidom.Document()

    # Create root element with namespace
    #  Syntax:  createElementNS("uri", "qualifiedname")
    #  https://developer.mozilla.org/en/DOM/document.createElementNS
    nselement = document.createElementNS(ns[0], ns[1])

    # Add namespace element to document root
    document.appendChild(nselement)

    return document, nselement

# Run the above:
doc, root = new_document(namespace)

# Create a <member> element
john = doc.createElement("member")

# Set attributes on the element
john.setAttribute("name", "John Doe")
john.setAttribute("uid", "5001")
john.setAttribute("phone", "860-872-1234")

# Append the member element to the group
root.appendChild(john)

# And again...
sally = doc.createElement("member")
sally.setAttribute("name", "Sally Smith")
sally.setAttribute("uid", "5002")
sally.setAttribute("phone", "777-123-4567")
root.appendChild(sally)


print doc.toprettyxml(indent="   ")
