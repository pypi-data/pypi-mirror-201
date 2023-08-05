from .Parse import XMLParser
import json
import argparse

# parser = argparse.ArgumentParser(description='Create config file for the game')
# parser.add_argument('--xml_path', type=str, default=" ", required=True,help='path to xml file')
# parser.add_argument('--config_path', type=str, default=" ", required=True,help='path to config file')

# args = parser.parse_args()
print()
class CreateConfig():
    def __init__(self, xml_path, config_path=None, ):
        self.parser = XMLParser(xml_path)
        if config_path == None:
            self.config_path = config_path
            assert self.config_path != " ", "Please specify a path to the config file"
            assert self.parser != " ", "Please specify a path to the xml file"

    def createConfig(self):
        self.playString, self.beatBase, self.bpm = self.parser.parse()
        config = {
            "playString": self.playString,
            "beatBase": self.beatBase,
            "bpm": self.bpm
        }
        config["playString"] = self.playString.strip()
        if self.config_path is not None:
            with open(self.config_path, 'w') as fp:
                json.dump(config, fp, indent=4)
        else:
            return config

