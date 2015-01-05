/** Copyright (C) 2015  James Tatum

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
  */

/**
 * Sort the spreadsheet by department, position, and fan name.
 *
 * For more information on using the Spreadsheet API, see
 * https://developers.google.com/apps-script/service_spreadsheet
 */
function sortStaffList() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var rows = sheet.getDataRange();
  var numRows = rows.getNumRows();
  var values = rows.getValues();
  
  var range = sheet.getRange(4,1,sheet.getMaxRows(), sheet.getMaxColumns()).activate();
  range.sort([{column:3}, {column:4}, {column:1}]);
  sheet.setActiveRange(sheet.getRange(4, 1));
  // TODO: Should delete blank rows from the end of the sheet

};

function onOpen() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var entries = [{
    name : "Sort",
    functionName : "sortStaffList"
  }];
  spreadsheet.addMenu("Staff list", entries);
};
