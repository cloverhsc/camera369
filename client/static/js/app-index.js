requirejs.config({
    paths: {
        "jquery": "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min",
        "rxjs": "https://unpkg.com/@reactivex/rxjs@5.5.6/dist/global/Rx"
    }
});

requirejs(["index"]);
