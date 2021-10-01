from eulxml import xmlmap
from registry.xmlmapper.consts import NS_WC
from registry.xmlmapper.gml.gml import Gml


class Member(xmlmap.XmlObject):
    bounded_by = xmlmap.NodeField(xpath=f"//{NS_WC}boundedBy']/gml:*", node_class=Gml)
    geom = xmlmap.NodeField(xpath=f"//{NS_WC}THE_GEOM']/gml:*", node_class=Gml)


class FeatureCollection(xmlmap.XmlObject):
    number_matched = xmlmap.IntegerField(xpath="@numberMatched")
    number_returned = xmlmap.IntegerField(xpath="@numberReturned")
    bounded_by = xmlmap.NodeField(xpath=f"{NS_WC}boundedBy']/gml:*", node_class=Gml)
    members = xmlmap.NodeListField(xpath=f"{NS_WC}member']", node_class=Member)
