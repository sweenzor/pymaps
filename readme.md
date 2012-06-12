Introduction
Pymaps is a little wrapper/hack/script that allows you to create maps (currently only google maps) using python only. The script generates the javascript/html necessary that you can embed in your html pages.

Install
Download the source: http://code.google.com/p/pymaps/source/checkout And place the pymaps module in your python path. Someday it will be an egg :)

Usage
At the moment you have three python objects:

Pymap: Holds all the maps and necesary html/javascript for a complete page/view. This allows you to hold more than one map per page.

Map: A map object contains map properties and a list of points.

Icon: Icon properites that can be used by your points.

Bill Luitje was kind to help out with bad bugs and get the code working better, and also writing a short howto: http://www.lonelycode.com/2008/12/04/google-maps-and-django/