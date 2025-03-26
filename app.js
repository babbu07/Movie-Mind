const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const axios = require("axios");

// https://api.themoviedb.org/4cR3hImKd78dSs652PAkSAyJ5Cx.jpg
// https://image.tmdb.org/t/p/w500/4cR3hImKd78dSs652PAkSAyJ5Cx.jpg
// [7450, 11551, 440, 602, 80274]
// https://api.themoviedb.org/3/movie/movieId?api_key=60fbf2f8a8f8d69fd6983b53ceed9fad

const apiKey = "60fbf2f8a8f8d69fd6983b53ceed9fad";
const url = "https://api.themoviedb.org/3/movie/popular?api_key="+apiKey;

const app = express();

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static("public"));
app.use(cors());

app.set('view engine', 'ejs');

let movieIds = [];

app.get("/",async function(req, res){

    // fetching the data from tmdb
    try{
        const response = await fetch(url);
        const data = await response.json();
        let moviesDetails = [];
        for(let i=0;i<12;i++){
            moviesDetails.push({name: data.results[i].title, imageUrl: "https://image.tmdb.org/t/p/w500/"+data.results[i].poster_path});
        }
        res.render("home", {posters: moviesDetails, posterStyle: ["top-movies", "poster-card", "poster-name"]});
    }catch(error){
        console.log("/: "+error);
    }
});

app.post("/submit", function(req, res){
    let movieName = req.body.movieName;
    res.redirect("/"+movieName);
});

app.get("/:movieName", async function(req, res) {
    try {
        let movieName = req.params.movieName;

        // Ensure getPrediction completes before accessing movieIds
        await getPrediction(movieName);

        if (movieIds.length > 0) {
            let recommendedMoviesDetails = [];

            for (const element of movieIds) {
                let movieUrl = `https://api.themoviedb.org/3/movie/${element}?api_key=${apiKey}`;

                try {
                    const response = await fetch(movieUrl);
                    const data = await response.json();

                    recommendedMoviesDetails.push({
                        name: data.title,
                        imageUrl: `https://image.tmdb.org/t/p/w500/${data.poster_path}`
                    });

                } catch (error) {
                    console.error("Error fetching movie details: ", error);
                }
            }

            // Send the data to the frontend
            res.render("home", { posters: recommendedMoviesDetails, posterStyle: ["recommended-top-movies", "recommended-poster-card", "recommended-poster-name"]});
        } else {
            res.status(404).send("No recommended movies found.");
        }

    } catch (error) {
        console.error("Error in route handler: ", error);
        res.status(500).send("Internal Server Error");
    }
});


async function getPrediction(input) {
    try{
        const response = await axios.post("http://localhost:5000/predict", {input});
        movieIds = response.data.result;
    } catch(error) {
        console.error("getPridiction: ",error);
    }
    
}

app.listen(3000, function(){
    console.log("Port 3000 is active");
})