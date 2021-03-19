// Copyright 2021 UW-IT, University of Washington
// SPDX-License-Identifier: Apache-2.0

const fs = require('fs');
const path = require('path');

/**
 * A helper function to write the manifest to a file.
 * @param {string} filePath Location to store the manifest.json to.
 * @param {object} manifest_data A object representing the manifest.
 */
function writeToFile(filePath, manifest_data) {
  const fileDir = path.dirname(filePath);
  if (!fs.existsSync(fileDir)){
    fs.mkdirSync(fileDir, { recursive: true });
  }
  fs.writeFile(filePath, JSON.stringify(manifest_data, null, 2), (err) => {
    if (err) return console.log(err);
  });
}

module.exports = { writeToFile };