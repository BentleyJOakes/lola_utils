import sys
import xml.etree.ElementTree as ET

class LoLAConvert:

    def __init__(self):
        pass

    def convert_file(self, filename):

        places, transitions, arcs = self.parse_pnml(filename)

        print("Places: " + str(places))
        print("Transitions: " + str(transitions))
        print("Arcs: " + str(arcs))

        places_with_markings = []
        for place, marking in places.items():
            if int(marking) > 0:
                places_with_markings.append((place, marking))

        lola_file = filename.replace(".xml", ".lola")
        with open(lola_file, 'w') as f:
            f.write("PLACE\n")

            for i, place in enumerate(places):
                f.write("\t" + place)
                if i < len(places) -1:
                    f.write(",\n")
                else:
                    f.write(";\n")

            f.write("\nMARKING\n")
            for i, pm in enumerate(places_with_markings):
                f.write("\t" + pm[0] + " : " + pm[1])
                if i < len(places_with_markings) -1:
                    f.write(",\n")
                else:
                    f.write(";\n")

            for trans in transitions:
                f.write("\nTRANSITION " + trans + "\n")
                consume = {}
                produce = {}

                for arc in arcs:
                    s, t, w = arc
                    if t == trans:
                        consume[s] = w
                    elif s == trans:
                        produce[t] = w

                f.write("\tCONSUME\n")
                for i, s in enumerate(consume):
                    f.write("\t\t" + s + " : " + consume[s])
                    if i < len(consume) - 1:
                        f.write(",\n")
                    else:
                        f.write(";\n")
                f.write("\tPRODUCE\n")
                for i, t in enumerate(produce):
                    f.write("\t\t" + t + " : " + produce[t])
                    if i < len(produce) - 1:
                        f.write(",\n")
                    else:
                        f.write(";\n")

    def parse_pnml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        net = root[0]

        places = {}
        transitions = []
        arcs = []

        for child in net:

            if child.tag == "place":
                name_node = self.get_child_with_name(child, "name")
                name = self.get_child_with_name(name_node, "value").text

                marking_node = self.get_child_with_name(child, 'initialMarking')
                marking_value_node = self.get_child_with_name(marking_node, 'value')
                marking = marking_value_node.text.split(",")[1]

                places[name] = marking

            elif child.tag == "transition":
                name_node = self.get_child_with_name(child, "name")
                name = self.get_child_with_name(name_node, "value").text

                transitions.append(name)

            elif child.tag == "arc":
                source = child.get("source")
                target = child.get("target")

                inscription_node = self.get_child_with_name(child, 'inscription')
                inscription_value_node = self.get_child_with_name(inscription_node, 'value')
                inscription = inscription_value_node.text.split(",")[1]

                arcs.append((source, target, inscription))


        return places, transitions, arcs

    def get_child_with_name(self, node, name):
        for child in node:
            if child.tag == name:
                return child
        raise Exception("On node: " + str(node) +", the child " + name + " was not found!")

if __name__ == "__main__":
    filename = "dining_philo.xml"
    lc = LoLAConvert()
    lc.convert_file(filename)