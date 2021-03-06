function onOpen() {
    var ss = SpreadsheetApp.getActive();
    var items = [
        {name: 'Deduplicate for mail merge', functionName: 'deDupe'},
    ];
    ss.addMenu('Staff list', items);
}

function deDupe() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var source = ss.getSheetByName("Form Responses");
    var target = ss.getSheetByName("Deduped for mail merge");

    target.clear();

    target.appendRow(['Data automatically generated by "Deduplicate for mail merge" script']);
    // Copy header row
    source.getRange(1, 1, 1, source.getMaxColumns()).copyTo(target.getRange(2, 1));
    var targetRow = 3;

    var range = source.getRange(1, 1, source.getMaxRows(), source.getMaxColumns());
    var data = range.getValues();
    var phones = [];
    for (var i = 0; i < data.length; i++) {
        var row = data[i];
        var phone = row[10].toString();
        // Strip out anything that's not a number
        phone = phone.replace(/\D+/g, '');
        if (phones.indexOf(phone) == -1) {
            phones.push(phone);
            var rowRange = source.getRange(i + 1, 1, 1, source.getMaxColumns());
            rowRange.copyTo(target.getRange(targetRow++, 1));
        }
    }
}
