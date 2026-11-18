/**
 * Nature's Nook pickup orders: Google Apps Script web app.
 * Receives orders from naturesnook.co, saves each one as a row in this Google Sheet,
 * and emails the store. Staff then text the customer from the GoTo app.
 *
 * This is a STANDALONE Apps Script project (script.google.com > New project), separate from the iPad drawing form's project,
 * and it only ever adds rows to its own "Orders" tab. Setup is in README.md (same folder). Nothing secret goes in this file:
 * the store email lives in Script Properties (Project Settings > Script Properties).
 */
// Paste the ID of the "NN Mailing List" Google Sheet here (the long code in its web address between /d/ and /edit).
var SPREADSHEET_ID = 'PASTE_SHEET_ID_HERE';
var HEADERS = ['Received', 'Order #', 'Status', 'Name', 'Phone', 'Items', 'Estimated total', 'Note', 'Text OK'];
var MAX_LINES = 30, MAX_QTY = 10, KEEP_DAYS = 90;

function doGet() {
  return json_({ ok: true, service: 'Nature\'s Nook pickup orders' });
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');

    var name = clean_(d.name, 80);
    var phone = String(d.phone || '').replace(/\D/g, '');
    if (phone.length === 11 && phone.charAt(0) === '1') phone = phone.slice(1);
    if (!name || phone.length !== 10) return json_({ ok: false, error: 'bad contact' });
    if (d.consent !== true) return json_({ ok: false, error: 'no consent' });
    if (!Array.isArray(d.items) || !d.items.length || d.items.length > MAX_LINES) return json_({ ok: false, error: 'bad items' });

    // limit each phone number to 5 orders an hour
    var cache = CacheService.getScriptCache(), key = 'p' + phone;
    var n = Number(cache.get(key) || 0);
    if (n >= 5) return json_({ ok: false, error: 'slow down' });
    cache.put(key, String(n + 1), 3600);

    var total = 0, lines = [];
    d.items.forEach(function (it) {
      var qty = Math.max(1, Math.min(MAX_QTY, Math.floor(Number(it.qty) || 1)));
      var price = Math.max(0, Number(it.price) || 0);
      total += qty * price;
      lines.push(qty + ' x ' + clean_(it.brand, 60) + ' ' + clean_(it.name, 120) +
        (it.variant ? ' (' + clean_(it.variant, 120) + ')' : '') + ' [' + clean_(it.upc, 20) + '] $' + price.toFixed(2));
    });

    var sheet = sheet_();
    var id = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MMdd') + '-' +
             ('00' + (sheet.getLastRow())).slice(-3);   // row number keeps it unique per sheet
    var note = clean_(d.note, 300);
    sheet.appendRow([new Date(), id, 'New', name, phone, lines.join('\n'), '$' + total.toFixed(2), note, 'Yes']);

    var to = PropertiesService.getScriptProperties().getProperty('STORE_EMAIL');
    if (to) {
      MailApp.sendEmail(to, 'Pickup order #' + id + ' - ' + name,
        'New pickup order #' + id + '\n\nName: ' + name + '\nPhone: ' + formatPhone_(phone) +
        '\nCustomer agreed to a text about this order: yes\n\n' + lines.join('\n') +
        '\n\nEstimated total: $' + total.toFixed(2) + (note ? '\nNote: ' + note : '') +
        '\n\nOpen the sheet: ' + SpreadsheetApp.openById(SPREADSHEET_ID).getUrl());
    }
    return json_({ ok: true, id: id });
  } catch (err) {
    return json_({ ok: false, error: 'server' });
  } finally {
    try { lock.releaseLock(); } catch (x) {}
  }
}

/** Run once from the Apps Script editor to delete orders older than KEEP_DAYS (also set a daily trigger, see README). */
function purgeOld() {
  var sheet = sheet_(), rows = sheet.getDataRange().getValues(), cutoff = Date.now() - KEEP_DAYS * 864e5;
  for (var r = rows.length - 1; r >= 1; r--) {
    var t = rows[r][0];
    if (t instanceof Date && t.getTime() < cutoff) sheet.deleteRow(r + 1);
  }
}

function sheet_() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID), sh = ss.getSheetByName('Orders') || ss.insertSheet('Orders');
  if (sh.getLastRow() === 0) { sh.appendRow(HEADERS); sh.setFrozenRows(1); }
  return sh;
}
function clean_(v, max) {
  // strip anything that could act as a spreadsheet formula, and cap the length
  return String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').replace(/^[=+\-@]+/, '').slice(0, max).trim();
}
function formatPhone_(p) { return '(' + p.slice(0, 3) + ') ' + p.slice(3, 6) + '-' + p.slice(6); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
