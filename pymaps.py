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
        
class Map:
    def __init__(self,id="map"):
        self.id       = id    # div id        
        self.width    = "500px"  # map div width
        self.height   = "300px"  # map div height
        self.center   = (0,0)     # center map latitute coordinate
        self.zoom        = "1"   # zoom level
        self.navcontrols  =   True   # show google map navigation controls
        self.mapcontrols  =   True   # show toogle map type (sat/map/hybrid) controls
        self.points = []         # point list
    
    def __str__(self):
        return self.id
        
    
    def setpoint(self, point):
        """ Add a point (lat,long) """
        self.points.append(point)

class PyMap:
    """
    Python wrapper class for Google Maps API.
            
    """
    
    def __str__(self):
        return "Pymap"
    
    def __init__(self, key=None, maplist=[Map(),]):
        """ Default values """
        self.key      = key      # set your google key
        self.maps     = maplist
    
    
    
    def _navcontroljs(self,map):
        """ Returns the javascript for google maps control"""    
        if map.navcontrols:
            return "%s.addControl(new GSmallMapControl());\n" % (map.id)
        else:
            return ""    
    
    
    def _mapcontroljs(self,map):
        """ Returns the javascript for google maps control"""    
        if map.controls:
            return "%s.addControl(new GMapTypeControl());\n" % (map.id)
        else:
            return ""     
    
    def _renderpointsjs(self,map):
        
        
        js = """   
        var %s_points_with_html = [];
        var %s_points = [];    
        %s
        %s
        
        """ % (map.id, map.id, "".join(["\n %s_points.push(new GLatLng(%s, %s));" % (map.id,k[0], k[1]) for k in map.points if len(k) == 2]), "".join(["\n %s_points_with_html.push(new GLatLng(%s, %s)); %s_html.push('%s');" % (map.id,k[0], k[1],map.id, k[2]) for k in map.points if len(k) == 3]) )
        #% (map.id, map.id,"".join(["\n %s_points.push(new GLatLng(%s, %s));" % (map.id,k[0], k[1]) for k in map.points if len(k) == 2]), \
        #    len([v for v in map.points if len(v) == 2]),\
        #    "".join(["\n %s_points_with_html.push(new GLatLng(%s, %s)); %s_html.push('%s');" % (map.id,k[0], k[1],map.id, k[2]) for k in map.points if len(k) == 3]),\
        #    len([v for v in map.points if len(v) ==3]))

        return js

    def _showdivhtml(self,map):
        """ Returns html for dislaying map """
        html = """\n<div id=\"%s\">\n</div>\n""" % (map.id)
        return html
    
    
    
    def _mapjs(self,map):
        mapjs = """
        %s_points = %s;
        var %s = new Map('%s',%s_points,%s,%s,%s);
        """ % (map.id,map.points,map.id,map.id,map.id,map.center[0],map.center[1],map.zoom)
        return mapjs
   
    def _buildmaps(self):
        for i in self.maps:
            js = self._mapjs(i)
        return js

    def pymapjs(self):
        """ Returns complete javacript for rendering map """
        
        self.js = """\n<script src=\"http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s\" type="text/javascript"></script>
        <script type="text/javascript">
        //<![CDATA[
        function load() {
            if (GBrowserIsCompatible()) {
                
            
            function Point(lat,long,html,icon) {
                  this.gpoint = new GMarker(new GLatLng(lat,long),icon);
                  this.html = html;
                  
               }               
               
               
               function Map(id,points,lat,long,zoom) {
                  this.id = id;
                  this.points = points;
                  this.gmap = new GMap2(document.getElementById(this.id));
                  this.gmap.setCenter(new GLatLng(lat, long), zoom);
                  this.markerlist = markerlist;
                  this.addmarker = addmarker;
                  this.array2points = array2points;
                   
                  function markerlist(array) {
                     for (var i in array) {
                        this.addmarker(array[i]);
                     }
                  }
                  
                  function array2points(map_points) {            
              for (var i in map_points) {  
                points[i] = new Point(map_points[i][0],map_points[i][1],map_points[i][2],map_points[i][3]);         }
              return points;   
            }                  
                  
                  function addmarker(point) {
                     if (point.html) {
                       GEvent.addListener(point.gpoint, "click", function() {
                           point.gpoint.openInfoWindowHtml(point.html);
                       });
                     }
                     this.gmap.addOverlay(point.gpoint);  
                  }
                  
                  this.points = array2points(this.points);
                  this.markerlist(this.points); 
            }  
                
            %s
                
               
            }
        }
        //]]>
        </script>
        
        
        """ % (self.key, self._buildmaps())
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
""" % (self.pymapjs())
        return self.html


if __name__ == "__main__":
        
    g = PyMap()
    g.key = "ABQIAAAAQQRAsOk3uqvy3Hwwo4CclBTrVPfEE8Ms0qPwyRfPn-DOTlpaLBTvTHRCdf2V6KbzW7PZFYLT8wFD0A"    
    p = [1,1]
    s = [2,4,'hello']
    g.maps[0].setpoint(p)
    g.maps[0].setpoint(s)
    print g.showhtml()
    
    
            