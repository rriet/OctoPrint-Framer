# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class FramerPlugin(     octoprint.plugin.SimpleApiPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin ):

    # Settings:
    def get_settings_defaults(self):
        return dict(framespeed="1000")
    
    def get_template_vars(self):
        return dict(framespeed=self._settings.get(["framespeed"]))

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    # API settings
    def get_api_commands(self):
        return dict(
            frame=[]
        )

    def on_api_command(self, command, data):
        if command == "frame":
            # Find the file name from the current print job            
            fileName = self._printer.get_current_job()["file"]["path"]
            
            # Try to get the print area from the metatag (for cura files)
            printArea = self._file_manager.get_metadata("local", fileName)["analysis"]["printingArea"]
            
            maxX = "0"
            maxY = "0"
            minX = "0"
            minY = "0"

            if not printArea["maxX"] == 0:
                # the print area was found so we can get the dimensions;
                maxX = str(printArea["maxX"])
                maxY = str(printArea["maxY"])
                minX = str(printArea["minX"])
                minY = str(printArea["minY"])
                
            else:
                # get file path
                filePath = self._file_manager.path_on_disk("local", fileName)
                firstLines = open(filePath).read(1000)

                # If the first lines have the string "; Bounds:" than it's a lightburn file
                if "; Bounds: " in firstLines:
                    startOfLine = firstLines.index( "; Bounds: " ) + len( "; Bounds: " )
                    endOfLine = firstLines[startOfLine:].index( "\n" ) + startOfLine
                    
                    # Get the limist line. It looks like "X18.85 Y204.94 to X185.15 Y387.06" (minX minY to maxX maxY)
                    limits = firstLines[startOfLine:endOfLine].split()
                    
                    # The [1:] removes the first character that represents the letter
                    maxX = limits[3][1:]
                    maxY = limits[4][1:]
                    minX = limits[0][1:]
                    minY = limits[1][1:]
                
                # If the first lines have the string "; X Min:" than it's a Fusion360 file
                elif "; X Min:" in firstLines:
                    # looking for the following string pattern
                    #; Ranges table:
                    #; X: Min=-0.5 Max=63.4 Size=63.9
                    #; Y: Min=-0.5 Max=25.4 Size=25.9

                    # Gets the string after "; Ranges table:" and split in lines
                    rangesTable = firstLines[firstLines.index( "; Ranges table:" ) + len( "; Ranges table:" ) +1 : ].split("\n")
                    
                    # First line
                    minX = rangesTable[0][rangesTable[0].index("Min=") + len("Min=") : rangesTable[0].index(" Max=")]
                    maxX = rangesTable[0][rangesTable[0].index("Max=") + len("Max=") : rangesTable[0].index(" Size=")]

                    # Second line
                    minY = rangesTable[1][rangesTable[1].index("Min=") + len("Min=") : rangesTable[1].index(" Max=")]
                    maxY = rangesTable[1][rangesTable[1].index("Max=") + len("Max=") : rangesTable[1].index(" Size=")]

                # If no string found, the type is unknown...  we have to calculate with brute force
                else:
                    # Read all the line of the file split into a array per line
                    allLines = open(filePath).read().split("\n")
                    
                    for line in allLines:
                        if line.startswith("G0") or line.startswith("G1") or line.startswith("G2"):
                            xCoordLine = "0"
                            yCoordLine = "0"

                            if "X" in line:
                                # Grab from X... untill " " (space)
                                try:
                                    xCoordLine = line[ line.index("X") + 1 : line[line.index("X") + 1:].index(" ")+line.index("X")+1]
                                except:
                                    # if there is exception is because the X command is the end of the line and there is no more spaces
                                    xCoordLine = line[ line.index("X") + 1 :]
                                
                                # If there was a X coordinate in line...
                                # Now we compare with minX, maxX
                                if float(xCoordLine) > float(maxX):
                                    maxX = xCoordLine

                                if float(xCoordLine) < float(minX):
                                    minX = xCoordLine


                            if "Y" in line:
                                # Grab from Y... untill " " (space)
                                try:
                                    yCoordLine = line[ line.index("Y") + 1 : line[line.index("Y") + 1:].index(" ")+line.index("Y")+1]
                                except:
                                    # if there is exception is because the Y command is the end of the line and there is no more spaces
                                    yCoordLine = line[ line.index("Y") + 1 :]

                                # If there was a X coordinate in line...
                                # Now we compare with minX, maxX
                                if float(yCoordLine) > float(maxY):
                                    maxY = yCoordLine

                                if float(yCoordLine) < float(minY):
                                    minY = yCoordLine

            self.moveToLimits(minX, minY, maxX, maxY)
            

    def moveToLimits(self, minX="0", minY="0", maxX="0", maxY="0"):
        # get the speed from the settings
        moveSpeed = self._settings.get(["framespeed"])

        # Send commando to printer to move to the corners
        self._printer.commands("G0 X" + minX +" Y" + minY + " F" + moveSpeed)
        self._printer.commands("G0 X" + minX +" Y" + maxY + " F" + moveSpeed)
        self._printer.commands("G0 X" + maxX +" Y" + maxY + " F" + moveSpeed)
        self._printer.commands("G0 X" + maxX +" Y" + minY + " F" + moveSpeed)
        self._printer.commands("G0 X" + minX +" Y" + minY + " F" + moveSpeed)
        self._printer.commands("G0 X0 Y0 F" + moveSpeed)



    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/framer.js"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "framer": {
                "displayName": "Framer Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "rriet",
                "repo": "OctoPrint-Framer",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/rriet/OctoPrint-Framer/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Framer Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = FramerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
