"""

*    Pymaps 0.1 


*    Copyright (C) 2007  Ashley Camba <stuff4ash@gmail.com> http://xthought.org

*

*    This program is free software; you can redistribute it and/or modify

*    it under the terms of the GNU General Public License as published by

*    the Free Software Foundation; either version 2 of the License, or

*    (at your option) any later version.

*

*    This program is distributed in the hope that it will be useful,

*    but WITHOUT ANY WARRANTY; without even the implied warranty of

*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

*    GNU General Public License for more details.

*

*    You should have received a copy of the GNU General Public License

*    along with this program; if not, write to the Free Software

*    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA









"""   
        


class PyMap:
    """
    Python wrapper class for Google Maps API.
            
    """
    
    class Point:
        pass
    
    def __init__(self, key=None):
        """ Default values """
        
        self.id       = "map"    # div id
        self.key      = key      # set your google key
        self.width    = "500px"  # map div width
        self.height   = "300px"  # map div height
        self.centerlat   = 0     # center map latitute coordinate
        self.centerlong  = 0     # center map longitud coordinate
        self.zoom        = "1"   # zoom level
        self.controls    = True  # show google map controls
        self.points = []         # point list
    
    def setpoint(self, point):
        """ Add a point (lat,long) """
        
        self.points.append(point)
    
    def mapcontrol(self):
        """ Returns the javascript for google maps control"""    
        if self.controls:
            return "map.addControl(new GSmallMapControl());\n map.addControl(new GMapTypeControl());"
        else:
            return ""    
    
    def renderpoints(self):
        """ Returns the javascript for all the points in self.points """
        
        if self.points <> []: 
            self.pointjs = """
           function createMarker(point, html) {
               var marker = new GMarker(point);
               GEvent.addListener(marker, "click", function() {
               marker.openInfoWindowHtml(html);
               });
               return marker;
            }  
            
            var points = [];
            %s
            for (var i = 0; i < %s; i++) {
            map.addOverlay(new GMarker(points[i]));
            }
            
            var pointswithhtml = [];
            var html = [];
            %s
            for (var i = 0; i < %s; i++) {
            map.addOverlay(createMarker(pointswithhtml[i],html[i]));
            }            
            
            
            
            """ % ("".join(["\n points.push(new GLatLng(%s, %s));" % (k[0], k[1]) for k in self.points if len(k) == 2]), len(self.points),"".join(["\n points.push(new GLatLng(%s, %s)); html.push('%s');" % (k[0], k[1], k[2]) for k in self.points if len(k) == 3]),len(self.points))

        else:
            self.pointjs = ""
        return self.pointjs

    def showdiv(self):
        """ Returns html for dislaying map """
        
        self.script = """\n<div id=\"%s\">\n</div>\n""" % (self.id)
        return self.script
    
    def markerjs(self): 
        """ Returns javascript for marker windows """
        
        self.markerjs =   """
          function createMarker(point, number) {
          var marker = new GMarker(point);
          GEvent.addListener(marker, "click", function() {
            marker.openInfoWindowHtml("Marker #<b>" + number + "</b>");
          });
          return marker;
        }
	
    """
    def mapjs(self):
        """ Returns complete javacript for rendering map """
        
        self.js = """\n<script src=\"http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s\" type="text/javascript"></script>
        <script type="text/javascript">
        //<![CDATA[
        function load() {
            if (GBrowserIsCompatible()) {
                var map = new GMap2(document.getElementById("map"));
                map.setCenter(new GLatLng(%s, %s), %s);
                
                %s
                
                %s
            }
        }
        //]]>
        </script>
        
        
        """ % (self.key, self.centerlat, self.centerlong, self.zoom, self.renderpoints(), self.mapcontrol())
        return self.js    
    
    
        
    def showhtml(self):
        """returns a complete html page with a map"""
        
        self.html = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title></title>
    %s
  </head>

  <body onload="load()" onunload="GUnload()">
    <div id="map" style="width: 500px; height: 300px"></div>
  </body>
</html>
""" % (self.mapjs)
        return self.html


if __name__ == "__main__":
    g = PyMap()
    p = (1,1)
    g.setpoint(p)
    print g.showhtml()

            