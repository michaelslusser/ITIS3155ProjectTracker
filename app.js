// import modules
const express = require("express");
const morgan = require("morgan");
const methodOverride = require("method-override");
// need imports for routes

// initialize application
const app = express();

// configure app
let port = 8080;
let host = "localhost";
app.set("view engine", "ejs"); // use .ejs files as views, no need to add .ejs at the end of file names

// middleware
app.use(express.static("public"));
app.use(express.urlencoded({extended: true}));
app.use(morgan("tiny"));
app.use(methodOverride("_method"));

// route setup
app.get("/", (req, res) => {
    res.render("index");
});

// in the future, need app.use() for each route 

// start server
app.listen(port, host, () => {
    console.log("Server running on port ", port);
});