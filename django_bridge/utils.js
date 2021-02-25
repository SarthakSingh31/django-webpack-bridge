const fs = require('fs');
const path = require('path');

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