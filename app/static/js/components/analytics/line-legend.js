// Data From - https://www.glassdoor.com/Reviews/The-Zimmerman-Agency-Reviews-E224188_P6.htm

// DEBUGGING
//   var glassdoor_data = require('./zimmerman_agency_glassdoor_reviews.json');

// var glassdoor_data = [];
// $.getJSON("zimmerman_agency_glassdoor_reviews.json", function(json) {
//     glassdoor_data = json;
// });

// var glassdoor_data = (function () {
//     var json = null;
//     $.ajax({
//         'async': false,
//         'global': false,
//         'url': 'zimmerman_agency_glassdoor_reviews.json',
//         'dataType': "json",
//         'success': function (data) {
//             json = data;
//         }
//     });
//     return json;
// })();

// console.log(glassdoor_data[0]['recommends']);
// DEBUGGING


// CUSTOM
var glassdoor_datapoints = [
 {
   "month":2,
   "year":2009,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":1,
   "year":2010,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":6,
   "year":2010,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":6,
   "year":2010,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":8,
   "year":2010,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":9,
   "year":2010,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":2,
   "year":2011,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":2,
   "year":2011,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":6,
   "year":2011,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":7,
   "year":2011,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":9,
   "year":2011,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":10,
   "year":2011,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":11,
   "year":2011,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":2,
   "year":2013,
   "recommends":1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":3,
   "year":2013,
   "recommends":1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":6,
   "year":2013,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":7,
   "year":2013,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":7,
   "year":2013,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":7,
   "year":2013,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":8,
   "year":2013,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":9,
   "year":2013,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":11,
   "year":2013,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":11,
   "year":2013,
   "recommends":1,
   "outlook":1,
   "ceo_approval":0
 },
 {
   "month":12,
   "year":2013,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":2,
   "year":2014,
   "recommends":0,
   "outlook":1,
   "ceo_approval":0
 },
 {
   "month":4,
   "year":2014,
   "recommends":0,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":5,
   "year":2014,
   "recommends":1,
   "outlook":1,
   "ceo_approval":0
 },
 {
   "month":5,
   "year":2014,
   "recommends":1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":5,
   "year":2014,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":-1
 },
 {
   "month":6,
   "year":2014,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":8,
   "year":2014,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":8,
   "year":2014,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":10,
   "year":2014,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":3,
   "year":2015,
   "recommends":1,
   "outlook":1,
   "ceo_approval":0
 },
 {
   "month":4,
   "year":2015,
   "recommends":1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":5,
   "year":2015,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":6,
   "year":2015,
   "recommends":-1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":7,
   "year":2015,
   "recommends":1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":8,
   "year":2015,
   "recommends":0,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":8,
   "year":2015,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":9,
   "year":2015,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":9,
   "year":2015,
   "recommends":1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":9,
   "year":2015,
   "recommends":0,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":10,
   "year":2015,
   "recommends":0,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":10,
   "year":2015,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":11,
   "year":2015,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":2,
   "year":2016,
   "recommends":0,
   "outlook":1,
   "ceo_approval":0
 },
 {
   "month":2,
   "year":2016,
   "recommends":1,
   "outlook":0,
   "ceo_approval":0
 },
 {
   "month":3,
   "year":2016,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":3,
   "year":2016,
   "recommends":1,
   "outlook":0,
   "ceo_approval":1
 },
 {
   "month":3,
   "year":2016,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":3,
   "year":2016,
   "recommends":-1,
   "outlook":-1,
   "ceo_approval":-1
 },
 {
   "month":4,
   "year":2016,
   "recommends":1,
   "outlook":1,
   "ceo_approval":1
 },
 {
   "month":4,
   "year":2016,
   "recommends":1,
   "outlook":1,
   "ceo_approval":0
 }
];

// var glassdoor_data_by_quarter = {};
var glassdoor_data_by_quarter= {
    "2009 Q1": {},
    "2009 Q2": {},
    "2009 Q3": {},
    "2009 Q4": {},
    "2010 Q1": {},
    "2010 Q2": {},
    "2010 Q3": {},
    "2010 Q4": {},
    "2011 Q1": {},
    "2011 Q2": {},
    "2011 Q3": {},
    "2011 Q4": {},
    "2012 Q1": {},
    "2012 Q2": {},
    "2012 Q3": {},
    "2012 Q4": {},
    "2013 Q1": {},
    "2013 Q2": {},
    "2013 Q3": {},
    "2013 Q4": {},
    "2014 Q1": {},
    "2014 Q2": {},
    "2014 Q3": {},
    "2014 Q4": {},
    "2015 Q1": {},
    "2015 Q2": {},
    "2015 Q3": {},
    "2015 Q4": {},
    "2016 Q1": {},
    "2016 Q2": {}
    // "2016 Q3": {},
    // "2016 Q4": {}
};

var add_quarterly_data = function(year_quarter, data, i) {
    // fields = ["recommends", "outlook", "ceo_approval"];
    // if (typeof glassdoor_data_by_quarter[year_quarter] == "undefined") {
    //     glassdoor_data_by_quarter[year_quarter] = {};
    // }
    if (typeof glassdoor_data_by_quarter[year_quarter]["recommends"] == "undefined") {
        glassdoor_data_by_quarter[year_quarter]["recommends"] = 0;
    }
    if (typeof glassdoor_data_by_quarter[year_quarter]["outlook"] == "undefined") {
        glassdoor_data_by_quarter[year_quarter]["outlook"] = 0;
    }
    if (typeof glassdoor_data_by_quarter[year_quarter]["ceo_approval"] == "undefined") {
        glassdoor_data_by_quarter[year_quarter]["ceo_approval"] = 0;
    }
    if (typeof glassdoor_data_by_quarter[year_quarter]["n"] == "undefined") {
        glassdoor_data_by_quarter[year_quarter]["n"] = 0;
    }
    // for (var field in fields) {
    //     glassdoor_data_by_quarter[year_quarter][field] += data[field];
    // }
    // glassdoor_data_by_quarter[year_quarter]["recommends"] += data["recommends"];
    // glassdoor_data_by_quarter[year_quarter]["outlook"] += data["outlook"];
    // glassdoor_data_by_quarter[year_quarter]["ceo_approval"] += data["ceo_approval"];
    glassdoor_data_by_quarter[year_quarter]["recommends"] += glassdoor_datapoints[i]["recommends"];
    glassdoor_data_by_quarter[year_quarter]["outlook"] += glassdoor_datapoints[i]["outlook"];
    glassdoor_data_by_quarter[year_quarter]["ceo_approval"] += glassdoor_datapoints[i]["ceo_approval"];
    glassdoor_data_by_quarter[year_quarter]["n"] += 1;

    // Debugging
    // console.log(glassdoor_data_by_quarter[year_quarter]);
    // Debugging
};

for (var i = 0; i < glassdoor_datapoints.length; i++) {
    data = glassdoor_datapoints[i];
    year_quarter = String(data["year"]) + " ";
        if (data["month"] >= 1 && data["month"] <= 3) {
            year_quarter += "Q1"
    }
        else if (data["month"] >= 4 && data["month"] <= 6) {
            year_quarter += "Q2"
    }
        else if (data["month"] >= 7 && data["month"] <= 9) {
            year_quarter += "Q3"
    }
        else if (data["month"] >= 10 && data["month"] <= 12) {
            year_quarter += "Q4"
    }

    add_quarterly_data(year_quarter, data, i);
}

var running_avgs_over_time = function(data_class) {
    n_over_time = 0;
    sum_over_time = 0;
    avgs_over_time = [];

    // for (var i = 0; i < glassdoor_datapoints.length; i++) {
    // for (var i = 0; i < glassdoor_data_by_quarter.length; i++) {
    for (var quarter in glassdoor_data_by_quarter) {
        // recommendation = glassdoor_data_by_quarter[quarter]["recommends"];
        recommendation = glassdoor_data_by_quarter[quarter][data_class];
        data_points_in_quarter = glassdoor_data_by_quarter[quarter]["n"];

        if (typeof recommendation == "undefined") {
            recommendation = avgs_over_time.slice(-1)[0];
        }
        else {
            sum_over_time += recommendation;
            n_over_time += data_points_in_quarter;
        }

        // sum_over_time += recommendation;

        // Debugging
        // console.log(recommendation);
        // Debugging
        // recommendation = glassdoor_datapoints[i]["recommends"];

        running_avg = sum_over_time / n_over_time;
        avgs_over_time.push(running_avg);

        // Debugging
        console.log(avgs_over_time.length + '. Sum over time ' + ': ' + sum_over_time);
        console.log(avgs_over_time.length + '. N over time ' + ': ' + n_over_time);
        console.log(avgs_over_time.length + '. avg over time ' + ': ' + running_avg);
        // Debugging

    }
    return avgs_over_time;
};
// CUSTOM


// Debugging
console.log(glassdoor_data_by_quarter);
// console.log(running_recommendation_avgs_over_time());
// Debugging


var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

var randomScalingFactor = function() {
    return Math.round(Math.random() * 100 * (Math.random() > 0.5 ? -1 : 1));
};
var randomColorFactor = function() {
    return Math.round(Math.random() * 255);
};
var randomColor = function(opacity) {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
};

var config = {
    type: 'line',
    // CUSTOM
    data: {
        // labels: ["January", "February", "March", "April", "May", "June", "July"],
        labels: ["2009 Q1", "2009 Q2", "2009 Q3", "2009 Q4", "2010 Q1", "2010 Q2", "2010 Q3", "2010 Q4",
            "2011 Q1", "2011 Q2", "2011 Q3", "2011 Q4", "2012 Q1", "2012 Q2", "2012 Q3", "2012 Q4",
            "2013 Q1", "2013 Q2", "2013 Q3", "2013 Q4", "2014 Q1", "2014 Q2", "2014 Q3", "2014 Q4",
            "2015 Q1", "2015 Q2", "2015 Q3", "2015 Q4", "2016 Q1", "2016 Q2"
            // , "2016 Q3", "2016 Q4"
        ],
        datasets: [{
            label: "% Employee Recommends",
            // data: testy(),
            // data: running_avgs_over_time,
            // data: running_avgs_over_time(),
            // data: running_recommendation_avgs_over_time(),
            data: running_avgs_over_time('recommends'),
            fill: false,
            borderDash: [5, 5]
        }, {
            label: "% Positive Outlook",
            data: running_avgs_over_time('outlook'),
            fill: false,
            borderDash: [5, 5]
        }, {
            label: "% CEO Approval",
            data: running_avgs_over_time('ceo_approval'),
            // data: [randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor(), randomScalingFactor()],
            fill: false
        }]
    },
    // CUSTOM
    options: {
        responsive: true,
        legend: {
            position: 'bottom'
        },
        hover: {
            mode: 'label'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Year/Quarter'
                }
            }],
            yAxes: [{
                // type: 'percentScale',
                display: true,
                // scaleLabel : "<%= value + ' + two = ' + (Number(value) + 2)   %>"
                scaleLabel: {
                    display: true,
                    labelString: 'Positive Sentiment'
                },
                //CUSTOM
                // labels: {
                //     // show: true,
                //     template: "<%=value%>"
                    // fontSize: 10,
                    // fontStyle: "normal",
                    // fontColor: "rgba(255, 255, 255, 1)",
                    // fontFamily: "Helvetica Neue"
		        // }
                ticks: {
                    min: -1,
                    max: 1
                }
                // CUSTOM
            }]
        },
        title: {
            display: true,
            text: 'Joviality of Zimmerman Employees (Avg to Date / Time)'
        }
    }
};

//CUSTOM
// var percentScale = Chart.Scale.extend({
//     convertTicksToLabels: function() {}
// });

// Chart.scaleService.registerScaleType('percentScale', percentScale, defaultConfigObject);
//CUSTOM



$.each(config.data.datasets, function(i, dataset) {
    var background = randomColor(0.5);
    dataset.borderColor = background;
    dataset.backgroundColor = background;
    dataset.pointBorderColor = background;
    dataset.pointBackgroundColor = background;
    dataset.pointBorderWidth = 1;
});

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
};

$('#randomizeData').click(function() {
    $.each(config.data.datasets, function(i, dataset) {
        dataset.data = dataset.data.map(function() {
            return randomScalingFactor();
        });

    });

    window.myLine.update();
});

$('#addDataset').click(function() {
    var background = randomColor(0.5);
    var newDataset = {
        label: 'Dataset ' + config.data.datasets.length,
        borderColor: background,
        backgroundColor: background,
        pointBorderColor: background,
        pointBackgroundColor: background,
        pointBorderWidth: 1,
        fill: false,
        data: []
    };

    for (var index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomScalingFactor());
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
});

$('#addData').click(function() {
    if (config.data.datasets.length > 0) {
        var month = MONTHS[config.data.labels.length % MONTHS.length];
        config.data.labels.push(month);

        $.each(config.data.datasets, function(i, dataset) {
            dataset.data.push(randomScalingFactor());
        });

        window.myLine.update();
    }
});

$('#removeDataset').click(function() {
    config.data.datasets.splice(0, 1);
    window.myLine.update();
});

$('#removeData').click(function() {
    config.data.labels.splice(-1, 1); // remove the label first

    config.data.datasets.forEach(function(dataset, datasetIndex) {
        dataset.data.pop();
    });

    window.myLine.update();
});
