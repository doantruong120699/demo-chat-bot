const express = require("express");
const path = require("path");
const fs = require("fs");

const apiRouter = express.Router();

apiRouter.get("*", (req, res) => {
  fs.readFile(path.join(__dirname, "../build/index.html"), (err, data) => {
    if (err) {
      res.status(200).json({
        error: err.message,
      });
      return;
    }

    res.writeHead(200, { "Content-Type": "text/html" });
    res.write(data);
    return res.end();
  });
});
module.exports = apiRouter;
