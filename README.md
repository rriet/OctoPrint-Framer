
# OctoPrint-Framer

#### author:
- Ricardo Riet Correa

#### license: 
GNUv3

#### date: 
2022-04-05

#### Links
homepage: https://github.com/rriet/OctoPrint-Framer

source: https://github.com/rriet/OctoPrint-Framer

archive: https://github.com/rriet/OctoPrint-Framer/archive/master.zip

## Description
This plugin adds a button to verify the working area of a Gcode on a CNC or Laser cutter.
It works by extracting the maximum and minimum X and Y and sending a G0 code to move the CNC/Laser to the corner locations.

#### tags:
- Octoprint
- Laser
- CNC

## screenshots:
![Main screen with Frame button](https://github.com/rriet/OctoPrint-Framer/blob/master/assets/img/plugins/framer/screen.png "Frame button and plugin output")
![Settings screen](https://github.com/rriet/OctoPrint-Framer/blob/master/assets/img/plugins/framer/settings.png "Settings screen")

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) or manually using this URL:

    https://github.com/rriet/OctoPrint-Framer/archive/master.zip

## Usage
### Configuration
After installation restart OctoPrint, go to the Settings tab and set the CNC/Laser movement speed.

### Frame function
- Connect the CNC/Laser
- Upload and load the Gcode file
- Home the CNC/Laser or use a G92 code to set the origin point
- Click the Frame button
- Observe the movement of the CNC/Laser to see where the work area is on the plataform. Be ready to stop the machine to avoid colisions.

## Warmings: 
- The plugin will not move the Z axis
- Make sure the area is clear to avoid colisions.

## Disclaimer:
I, the plugin author cannot be held responsible for any damage to equipment or injuries that may arise from using the plugin. I, the plugin author, make no guarantees that this plugin will work or continue to work.

