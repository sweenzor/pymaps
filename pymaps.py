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




class Pymap:
    """
    Python wrapper class for Google Maps API.
    
    
    
    """
    
    
    def __init__(self, key=None):
        """
        Load default values
        
        """
        self.key      = key
        self.width    = "500px"
        self.height   = "300px"
        self.centerlat   = 0
        self.centerlong  = 0
        self.zoom        = "1"
        self.controls    = True
        self.points = []
    
    def SetPoint(self, point):
        self.points.append(point)
    
    def ControlJS(self):
            if self.controls:
                return "map.addControl(new GSmallMapControl());\n map.addControl(new GMapTypeControl());"
            else:
                return ""    
    
    def RenderPoints(self):
            if self.points <> []: 
                self.pointjs = """var points = [];
                %s
                for (var i = 0; i < %s; i++) {
                    map.addOverlay(new GMarker(points[i]));
                }""" % ("".join(["\n                points.push(new GLatLng(%s, %s));" % (k, v) for k, v in self.points]), len(self.points))
            else:
                self.pointjs = ""
            return self.pointjs
            
        

    def MapJS(self):
        
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
        
        
        """ % (self.key, self.centerlat, self.centerlong, self.zoom, self.RenderPoints(), self.ControlJS())
        return self.js
        

    def ShowMap(self):
        
        self.script = """\n<div id=\"map\">\n</div>\n
        
        
        """ 
        return self.script
    
    def MarkerJS(self): 
        self.markerjs =   """
          function createMarker(point, number) {
          var marker = new GMarker(point);
          GEvent.addListener(marker, "click", function() {
            marker.openInfoWindowHtml("Marker #<b>" + number + "</b>");
          });
          return marker;
        }
		"""
        
    

if __name__ == "__main__":
    g = Pymap()
    print g.ShowMap()
    print g.MapJS()
        
            