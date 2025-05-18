"""
Created on: 10/05/2025 18:32

Author: Shyam Bhuller

Description: Python object to represent a GPX file (and utility functions to parse the xml).
"""
import xml.etree.ElementTree as ET

def xml_match_attrib(elem : ET.Element, attrib : str, value : str) -> bool:
    """ Returns True if a value of an attribute in an xml Element matches the target value.

    Args:
        elem (ET.Element): xml Element.
        attrib (str): attribute name.
        value (str): target value.

    Returns:
        bool: whether there was a match.
    """
    if value:
        return (attrib in elem.attrib) and (elem.attrib[attrib] == value)


def xml_search_elem(elem : ET.ElementTree | ET.Element, attrib : str, value : str) -> ET.Element:
    """ Search an xml Element by attribute value and yield the found Element.

    Args:
        elem (ET.ElementTree | ET.Element): 
        attrib (str): attribute to compare.
        value (str): value of attribute to match.

    Yields:
        Iterator[ET.Element]: Element with the found attribute value.
    """
    for obj in elem.iter():
        if xml_match_attrib(obj, attrib, value):
            yield obj
    return


def xml_search_elem_name(elem : ET.ElementTree | ET.Element, name : str) -> ET.Element:
    """ Search an xml Element by name and yield the found Element.

    Args:
        elem (ET.ElementTree | ET.Element): elements.
        name (str): name of the Elements to match.

    Yields:
        Iterator[ET.Element]: Element with the found attribute value.
    """
    for obj in elem.iter():
        if obj.tag == name:
            yield obj
    return


def xml_search_elem_name_single(elem : ET.ElementTree | ET.Element, name : str) -> ET.Element | None:
    """ Search for a single Element by name. If multiple elements found it returns the first.

    Args:
        elem (ET.ElementTree | ET.Element): elements.
        name (str): name of the Elements to match.

    Returns:
        ET.Element: first found Element.
    """
    return next(xml_search_elem_name(elem, name), None)


def write_xml(xml_tree : ET.ElementTree, file : str):
    """ Write an xml ElementTree to file.

    Args:
        xml_tree (ET.ElementTree): xml tree.
        file (str): output file path
    """
    xml_tree.write(file)
    return


def read_xml(file : str) -> ET.ElementTree:
    """ Read xml file and parse into an ElementTree.

    Args:
        file (str): xml file path.

    Returns:
        ET.ElementTree: xml tree.
    """
    return ET.parse(file)


class GPX:
    def __init__(self, file : str):
        self.xml = read_xml(file)
        self.gpx_head = self.xml.getroot().tag.replace("gpx", "")
        pass

    def tag(self, s : str) -> str:
        """ Infer the tag of xml elements based on the root tag. The tag is a prefix + the element name

        Args:
            s (str): Element name.

        Returns:
            str: Tag.
        """
        return self.gpx_head + s


    def get_paths(self) -> dict[list]:
        """ Returns the paths included in the file. A path is a dictionary with the latitude and lonitude of each node.

        Returns:
            dict[list]: Dictionary of the paths from the file.
        """
        trk = list(xml_search_elem_name(self.xml, self.tag("trk")))

        paths = {}
        for t in trk:
            name = xml_search_elem_name_single(t, self.tag("name")).text
            trk_vec = {"lat" : [], "lon" : []} # assume these must exist in the trkpt for a valid gpx file.
            for e in xml_search_elem_name(t, self.tag("trkpt")):
                trk_vec["lat"].append(float(e.attrib["lat"]))
                trk_vec["lon"].append(float(e.attrib["lon"]))
            paths[name] = trk_vec

        return paths
