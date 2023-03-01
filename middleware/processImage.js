var express = require('express');
var router = express.Router();
var path = require('path');
const fs = require('fs');
const morgan = require('morgan');
const multer = require('multer');
const process = require('process');
const { spawnSync } = require('child_process');
const { callbackify } = require('util');
const { finished } = require('stream');

const processImage = {};

processImage.getSimilarImages = function (req, res, next) {
  var dataToSend;
  var dataToJSON;
  // spawn new child process to call the python script
  const python = spawnSync('python', ['bin/processImages.py', req.file.path, 'public/images/indexed'], {encoding: 'utf-8'});
  req.result = python.stdout;
  console.log(python.stdout);
  // collect data from script
  // python.stdout.on('data', function (data) {
  //   console.log('Pipe data from python script ...');
  //   console.log(`Node JS got Data ${data}`);
  //   console.log(`Type is : ${typeof data}`);

  //   // convert data to String
  //   results = data.toString();
  //   data_str = data.toString();
  //   console.log(`Data To String: ${data_str}`);
  //   console.log(`Type is ${typeof data_str}`);

  //   // convert to JSON
  //   data_json = JSON.parse(data_str);
  //   dataToJSON = data_json
  //   console.log(`JSON is: ${data_json}`)
  //   console.log(`Data: ${data_json.data}`)
  //   console.log(`Type: ${typeof data_json.data}`)
  //   console.log(`1st element: ${data_json.data[0]}`)
  //   console.log(`2nd element: ${data_json.data[1]}`)

  //   // results[0] = "public/images/indexed/C1.png"



  //   dataToSend = data.toString();
  //   console.log(`Data to Send: ${dataToSend}`)
  //   process.send(dataToSend)
  // });
  // // in close event we are sure that stream from child process is closed
  // python.on('close', (code) => {
  //   console.log(`child process close all stdio with code ${code}`);
  // // send data to browser, if any.
  // });

  next();
}

function updateLocals(res, data) {
  res.locals.result = data;
}

module.exports = processImage;