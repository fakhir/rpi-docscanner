#!/usr/bin/env node

var Blynk = require('blynk-library');

var AUTH = 'b55118d6f782481db927d320e53487a4';

var blynk = new Blynk.Blynk(AUTH);

var button_gray = new blynk.VirtualPin(1); // grayscale switch
var dropbox = new blynk.VirtualPin(2); // selection 1: crop 2: full 3: id
var button_scan = new blynk.VirtualPin(4); // scan start button

var lcd = new blynk.WidgetLCD(3); // advanced lcd

// On connect clear the LCD
blynk.on('connect', function() {
  lcd.clear();
  lcd.print(0, 0, 'Connected');
});
// Grayscale switch: enable grayscale if 1
button_gray.on('write', function(param) {
  console.log('V1:', param[0]);
});
// Dropbox: mode select index 1: auto-crop 2: full page 3: ID card copy
dropbox.on('write', function(param) {
  console.log('V2:', param[0]);
});
// Scan button: value 1 when pressed
button_scan.on('write', function(param) {
  console.log('V4:', param[0]);
});
/*
v9.on('read', function() {
  v9.write(new Date().getSeconds());
});
*/
