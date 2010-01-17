#!/usr/bin/env python

# This was cribbed from the tutorial at:
#  http://www.postneo.com/projects/pyxml/

from xml.dom.minidom import Document

# Create a minidom document
doc = Document()

# Create the base element
group = doc.createElement("group")
doc.appendChild(group)

# Create another element
john = doc.createElement("member")

# Set attributes on the element
john.setAttribute("name", "John Doe")
john.setAttribute("uid", "5001")
john.setAttribute("phone", "860-872-1234")

# Append the member element to the group
group.appendChild(john)

# And again...
sally = doc.createElement("member")
sally.setAttribute("name", "Sally Smith")
sally.setAttribute("uid", "5002")
sally.setAttribute("phone", "777-123-4567")
group.appendChild(sally)


print doc.toprettyxml(indent="   ")
