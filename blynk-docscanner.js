#!/usr/bin/env node

var Blynk = require('blynk-library');
const exec = require('child_process').exec;

// Set your Blynk auth key below.
var AUTH = 'BLYNK-AUTH-KEY';

var blynk = new Blynk.Blynk(AUTH);

var button_gray = new blynk.VirtualPin(1); // grayscale switch
var select_mode = new blynk.VirtualPin(2); // scan mode
var select_type = new blynk.VirtualPin(6); // document type
var button_scan = new blynk.VirtualPin(4); // scan start button
var button_qual = new blynk.VirtualPin(7); // quality switch

var lcd = new blynk.WidgetLCD(3); // advanced lcd

// Variables controlling scan mode/operation
var scan_is_grayscale = false;
var scan_mode = 'autocrop';
var scan_type = 'receipt';
var scan_quality_high = false;
var scan_in_progress = false;
var scan_file = null;

var is_first_connect = true;

// On connect clear the LCD
blynk.on('connect', function() {
  lcd.clear();
  lcd.print(0, 0, 'Status:');
  if (scan_in_progress)
    lcd.print(0, 1, 'Busy       ');
  else
    lcd.print(0, 1, 'Idle       ');
  if (is_first_connect) {
    blynk.syncAll();
    is_first_connect = false;
  }
});

// Grayscale switch: enable grayscale if 1
button_gray.on('write', function(param) {
  if (param[0] == 1) {
    scan_is_grayscale = true;
  } else {
    scan_is_grayscale = false;
  }
});

// Grayscale switch: enable grayscale if 1
button_gray.on('write', function(param) {
  if (param[0] == 1) {
    scan_quality_high = true;
  } else {
    scan_quality_high = false;
  }
});

// Select box: mode select index 1: auto-crop 2: full page 3: ID card copy
select_mode.on('write', function(param) {
  scan_mode = ['autocrop', 'fullpage', 'idcard'][param[0] - 1];
});

// Select box: type select index 1: receipt 2: bill 3: medical 4: tax 5: cert 6: photo 7: card
select_type.on('write', function(param) {
  scan_type = ['receipt', 'bill', 'medical', 'tax', 'cert', 'photo', 'card'][param[0] - 1];
});

// Scan button: value 1 when pressed
button_scan.on('write', function(param) {
  var scan_cmd = 'hp-scan ';

  // Do nothing is button is being released
  if (param[0] == 0 || scan_in_progress)
    return;

  scan_file = '/tmp/' + scan_type + '_' + new Date().toISOString() + '.png';
  scan_in_progress = true;

  // Build the scan command line
  if (scan_is_grayscale == false) {
    scan_cmd += '-mcolor ';
  }
  if (scan_quality_high == false) {
    scan_cmd += '-r150 ';
  }
  scan_cmd += '-o' + scan_file;

  // Perform the scan
  lcd.clear();
  lcd.print(0, 0, 'Status:');
  lcd.print(0, 1, 'Scanning...');
  var childproc = exec(scan_cmd, { 'maxBuffer': 500000 }, function(err, stdout, stderr) {
    if (err) {
      lcd.print(0, 1, 'Scan error ');
      scan_in_progress = false;
    } else {
      // Auto-crop is requested
      if (scan_mode == 'autocrop') {
        lcd.print(0, 1, 'Cropping...');
        var childproc = exec('./autocrop.py ' + scan_file, function(err, stdout, stderr) {
          if (err) {
            lcd.print(0, 1, 'Crop error ');
            scan_in_progress = false;
          } else {
            lcd.print(0, 1, 'Uploading..');
            var childproc = exec('./dropboxupload.py ' + scan_file, function(err, stdout, stderr) {
              if (err) {
                lcd.print(0, 1, 'DBox error ');
              } else {
                lcd.print(0, 1, 'Done       ');
              }
              scan_in_progress = false;
            });
          }
        });
      } else {
        lcd.print(0, 1, 'Uploading..');

        var childproc = exec('./dropboxupload.py ' + scan_file, function(err, stdout, stderr) {
          if (err) {
            lcd.print(0, 1, 'DBox error ');
          } else {
            lcd.print(0, 1, 'Done       ');
          }
          scan_in_progress = false;
        });
      }
    }

  });

});
