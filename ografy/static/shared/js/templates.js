(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["Polyselect.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=utf-8 />\n<title>Show drawn polygon area</title>\n<meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />\n<script src='https://api.tiles.mapbox.com/mapbox.js/v2.1.5/mapbox.js'></script>\n<link href='https://api.tiles.mapbox.com/mapbox.js/v2.1.5/mapbox.css' rel='stylesheet' />\n<style>\n  body { margin:0; padding:0; }\n  #map { position:absolute; top:0; bottom:0; width:100%; }\n</style>\n</head>\n<body>\n<link href='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-draw/v0.2.2/leaflet.draw.css' rel='stylesheet' />\n<script src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-draw/v0.2.2/leaflet.draw.js'></script>\n<script src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-geodesy/v0.1.0/leaflet-geodesy.js'></script>\n\n<div id='map'></div>\n\n<script>\nL.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';\nvar map = L.mapbox.map('map', 'examples.map-i86nkdio')\n    .setView([38.89399, -77.03659], 17);\n\nvar featureGroup = L.featureGroup().addTo(map);\n\nvar drawControl = new L.Control.Draw({\n  edit: {\n    featureGroup: featureGroup\n  },\n  draw: {\n    polygon: true,\n    polyline: false,\n    rectangle: false,\n    circle: false,\n    marker: false\n  }\n}).addTo(map);\n\nmap.on('draw:created', showPolygonArea);\nmap.on('draw:edited', showPolygonAreaEdited);\n\nfunction showPolygonAreaEdited(e) {\n  e.layers.eachLayer(function(layer) {\n    showPolygonArea({ layer: layer });\n  });\n}\nfunction showPolygonArea(e) {\n  featureGroup.clearLayers();\n  featureGroup.addLayer(e.layer);\n  e.layer.bindPopup((LGeo.area(e.layer) / 1000000).toFixed(2) + ' km<sup>2</sup>');\n  e.layer.openPopup();\n}\n</script>\n</body>\n</html>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["base.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"flex column grow\">\n\t<div class=\"filter container\"></div>\n\t<div class=\"data-view flex grow\"></div>\n\t<div id=\"event-list\"></div>\n</div>\n<aside class=\"detail sidebar flex column\">\n</aside>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["detail.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"detail grow";
if(runtime.contextOrFrameLookup(context, frame, "showMap")) {
output += " text-half ";
;
}
else {
output += " full ";
;
}
output += "\">\n\t<div id=\"detail main-label\" class=\"center main-label\">\n\t\tSelect an Event\n\t</div>\n\t<div class=\"information\">\n\t\t<div id=\"detail datetime-location\" class=\"datetime-location\">\n\t\t\t<div id=\"avatar datetime\" class=\"avatar-datetime\">\n\t\t\t\t<div class=\"avatar\">\n\t\t\t\t\t<img src=\"static/assets/logo_240.png\" alt=\"Avatar\" />\n\t\t\t\t</div>\n\t\t\t\t<div id=\"detail datetime\" class=\"datetime\">\n\t\t\t\t\t<div id=\"detail date\" class=\"detail-date\">\n\t\t\t\t\t\t<label class=\"center label\">Date</label>\n\t\t\t\t\t\t<div id=\"detail date content\" class=\"center content\">\n\t\t\t\t\t\t\tSelect an Event\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t\t<div id=\"detail time\" class=\"detail-time\">\n\t\t\t\t\t\t<label class=\"center label\">Time</label>\n\t\t\t\t\t\t<div id=\"detail time content\" class=\"center content\">\n\t\t\t\t\t\t\tSelect an Event\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div id=\"detail location\" class=\"detail-location\">\n\t\t\t\t<label class=\"center label\">Location</label>\n\t\t\t\t<div id=\"detail location content\" class=\"center content\">\n\t\t\t\t\tSelect an Event\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>\n\t\t<div id=\"detail data\" class=\"detail-data\">\n\t\t\t<label class=\"center label\">Message Body</label>\n\t\t\t<div id=\"detail data content\" class=\"center content\">\n\t\t\t\tSelect an Event\n\t\t\t</div>\n\t\t</div>\n\t</div>\n</div>\n";
if(runtime.contextOrFrameLookup(context, frame, "showMap")) {
output += "\n<div class=\"detail map-half flex grow\">\n\t<div id='mapbox' class='grow'></div>\n</div>\n";
;
}
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["list/event_list.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "eventData");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n<div class=\"event\" event-id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"id", env.autoesc), env.autoesc);
output += "\">\n</div>\n";
;
}
}
frame = frame.pop();
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["list/list.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"main-list grow\">\n\t<div class=\"list title\">\n\t\t<div class=\"list item-provider bold\">\n\t\t\tProvider Name\n\t\t</div>\n\t\t<div class=\"list item-date bold\">\n\t\t\tDate - Time\n\t\t</div>\n\t\t<div class=\"list item-name bold\">\n\t\t\tName\n\t\t</div>\n\t\t<div class=\"list item-data bold\">\n\t\t\tData\n\t\t</div>\n\t</div>\n\t<div class=\"list content\">\n\t</div>\n</div>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["list/list_elements.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "resultData");
if(t_3) {var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n<div class=\"list item\" id=\"";
output += runtime.suppressValue(runtime.memberLookup((t_4),"id", env.autoesc), env.autoesc);
output += "\">\n\t<div class=\"list item-provider\">\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((t_4),"provider_name", env.autoesc), env.autoesc);
output += "\n\t</div>\n\t<div class=\"list item-date\">\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((t_4),"datetime", env.autoesc), env.autoesc);
output += "\n\t</div>\n\t<div class=\"list item-name\">\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((t_4),"name", env.autoesc), env.autoesc);
output += "\n\t</div>\n\t<div class=\"list item-data\">\n\t\t";
output += runtime.suppressValue(runtime.memberLookup((t_4),"data", env.autoesc), env.autoesc);
output += "\n\t</div>\n</div>\n";
;
}
}
frame = frame.pop();
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["map/map.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div id=\"mapbox\" class=\"grow\"></div>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filter.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"flex filter box\">\n\t<div class=\"grow filter options\">\n\t</div>\n\t<div class=\"add-remove-buttons\">\n\t\t<div class=\"filter button remove\">\n\t\t\t<i class=\"icon-minus\"></i>\n\t\t</div>\n\t\t<div class=\"filter button add\">\n\t\t\t<i class=\"icon-plus\"></i>\n\t\t</div>\n\t</div>\n</div>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/date/date_after_field.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"text\">\n\t<input class='date-start' type=\"date\">\n</div>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/date/date_before_field.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"text\">\n\t<input class='date-end' type=\"date\">\n</div>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/date/date_between_fields.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"text\">\n\t<input class='date-start' type=\"date\">\n\t<input class='date-end' type=\"date\">\n</div>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/date/date_dropdown.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<select class=\"date\">\n\t<option value=\"after\">After</option>\n\t<option value=\"before\">Before</option>\n\t<option value=\"between\">Between</option>\n</select>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/message_from/from_text_field.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"from text\">\n\t<input class='from-text' placeholder=\"Name\">\n</div>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/message_to/to_text_field.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"to text\">\n\t<input class='to-text' placeholder=\"Name\">\n</div>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/provider/provider_dropdown.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<select class=\"provider\">\n\t<option value=\"facebook\">Facebook</option>\n\t<option value=\"twitter\">Twitter</option>\n\t<option value=\"steam\">Steam</option>\n\t<option value=\"amazon\">Amazon</option>\n\t<option value=\"dropbox\">Dropbox</option>\n\t<option value=\"fitbit\">FitBit</option>\n\t<option value=\"foursquare\">FourSquare</option>\n\t<option value=\"github\">GitHub</option>\n\t<option value=\"google\">Google</option>\n\t<option value=\"instagram\">Instagram</option>\n\t<option value=\"linkedin\">LinkedIn</option>\n\t<option value=\"reddit\">reddit</option>\n\t<option value=\"spotify\">Spotify</option>\n\t<option value=\"stackoverflow\">Stack Overflow</option>\n\t<option value=\"tumblr\">Tumblr</option>\n\t<option value=\"vimeo\">Vimeo</option>\n</select>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/time/time_after_field.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"text\">\n\t<input class='time-start' type=\"time\">\n</div>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/time/time_before_field.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"text\">\n\t<input class='time-end' type=\"time\">\n</div>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/time/time_between_fields.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<div class=\"text\">\n\t<input class='time-start' type=\"time\">\n\t<input class='time-end' type=\"time\">\n</div>\n";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/filters/time/time_dropdown.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<select class=\"time\">\n\t<option value=\"after\">After</option>\n\t<option value=\"before\">Before</option>\n\t<option value=\"between\">Between</option>\n</select>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["search/initial_filter_dropdown.html"] = (function() {function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
output += "<select class=\"initial\">\n\t<option value=\"date\">Date</option>\n\t<option value=\"time\">Time</option>\n\t<option value=\"provider\">Provider</option>\n\t<option value=\"to\">To</option>\n\t<option value=\"from\">From</option>\n</select>";
cb(null, output);
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};
})();
})();
