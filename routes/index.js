var express = require("express");
var router = express.Router();
var path = require("path");
var { getSimilarImages } = require("../middleware/processImage");
const fs = require("fs");
const data = require("../public/data/data.json");
const morgan = require("morgan");
const multer = require("multer");
const process = require("process");
const { spawnSync } = require("child_process");
const processImage = require("../middleware/processImage");
const {
  allowInsecurePrototypeAccess
} = require("@handlebars/allow-prototype-access");

/* Setup uploaded image storage (db) */
const storage = multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, "public/images/uploads");
  },
  filename: function (req, file, callback) {
    callback(
      null,
      Date.now() +
        file.originalname.substring(0, 2) +
        path.extname(file.originalname)
    );
  }
});
const upload = multer({ storage: storage });

/* GET home page. */
router.get(["/", "/back"], function (req, res, next) {
  res.render("index", {
    title: "CSC 664",
    style: "../../public/stylesheets/indexStyle.css",
    script: "../../public/javascripts/runPyScript.js"
  });
});

/* GET data db */
router.get("/data", (req, res, next) => {
  res.json(data);
});

/* POST search results page */
router.post("/search", upload.single("image_file"), (req, res, next) => {
  // Run the python script to process the image.
  // const python = spawnSync(
  //   "python",
  //   [
  //     "bin/processImages.py",
  //     req.file.path,
  //     "public/images/indexed",
  //     req.body.method
  //   ],
  //   { encoding: "utf-8" }
  // );
  // var result = JSON.parse(python.stdout);

  const method_header = getMethodString(req.body.method);

  res.render("searchResults", {
    title: "CSC 664",
    style: "../../public/stylesheets/indexStyle.css",
    script: "../../public/javascripts/searchResults.js",
    input: req.file.path,
    method: req.body.method
  });
});

function getMethodString(method) {
  str = "";
  if ("cosine" === method) {
    str += "Cosine Distance Value";
  } else if ("intersection" === method) {
    str += "Histogram Intersection Value";
  }

  return str;
}

function basename(str, sep) {
  return str.substr(str.lastIndexOf(sep) + 1);
}

module.exports = router;
