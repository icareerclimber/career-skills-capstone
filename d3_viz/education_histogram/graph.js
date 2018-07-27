// Borrowed from http://bl.ocks.org/ChandrakantThakkarDigiCorp/2a9e6f11f2a27b6af0c28c4e5e524f10

// Load the salary json data
var allData = []
var rankedSubjects = []
d3.json("04_edu_data_bar_chart.json", function(error, json) {
    d3.csv("04_ranked_subjects.csv", function(error, data) {
        if (error) throw error;
        allData = json
        rankedSubjects = data

        updateGraph(allData, 'account executive')
})});

// Load unique job titles json data
d3.csv("04_unique_jobs.csv", function(error, data) {
    if (error) throw error;

    // Populate values in the job title dropdown using data from the json
    var options = jobDrop
        .selectAll('option')
        .data(data.map( function (d) {return d.cleaned_job_title} )).enter()
        .append('option')
        .text(function (d) { return d; });

});

// Attach the job title dropdown to the div
var jobDrop = d3.select("#jobDropdown")
    .append('select')
    .attr('class','select')
    .on('change', function() {
        jobValue = jobDrop.node().value;
        updateGraph(allData, jobValue)
    });

function updateGraph(data, jobValue) {

    var filteredData = data.filter(function(d) {
        return (d.cleaned_job_title == jobValue) });

    var group = rankedSubjects.filter(function(d) {
        return (d.cleaned_job_title == jobValue) }).map( function(d) {return d.subject_name });

    var layers = d3.stack()
        .keys(group)
        .offset(d3.stackOffsetDiverging)
        (filteredData);

    var svg = d3.select("svg"),
        margin = {
            top: 25,
            right: 100,
            bottom: 100,
            left: 175
        },
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var x = d3.scaleLinear()
        .rangeRound([margin.left, width - margin.right]);

    x.domain([d3.min(layers, stackMin), d3.max(layers, stackMax)]);

    var y = d3.scaleBand()
        .rangeRound([height - margin.bottom, margin.top])
        .padding(0.1);

    y.domain(filteredData.map(function(d) {
        return d.final_degree_category;
    }))

    function stackMin(layers) {
        return d3.min(layers, function(d) {
            return d[0];
        });
    }

    function stackMax(layers) {
        return d3.max(layers, function(d) {
            return d[1];
        });
    }

    var z = d3.scaleOrdinal(d3.schemeCategory10);

    var maing = svg.append("g")
        .selectAll("g")
        .data(layers);

    var g = maing.enter().append("g")
        .attr("fill", function(d) {
            return z(d.key);
        });

    svg.selectAll("rect").remove();
    svg.selectAll(".axis").remove();
    svg.selectAll(".x").remove();
    svg.selectAll(".y").remove();

    var tooltip = d3.select("body").append("div").attr("class", "toolTip");
    
    g.selectAll(".bar")
        .data(function(d) {
            d.forEach(function(d1) {
                d1.key = d.key;
                return d1;
            });
            return d;
        })
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("data", function(d) {
            var data = {};
            data["key"] = d.key;
            data["value"] = d.data[d.key];
            var total = 0;
            group.map(function(d1) {
                total = total + d.data[d1]
            });
            data["total"] = total;
            return JSON.stringify(data);
        })
        .attr("width", function(d) {
            return x(d[1]) - x(d[0]);
        })
        .attr("x", function(d) {
            return x(d[0]);
        })
        .attr("y", function(d) {
            return y(d.data.final_degree_category);
        })
        .attr("height", y.bandwidth)
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX + "px")
              .style("top", d3.event.pageY + "px")
              .style("display", "inline-block")
              .html('"' + (d.key) + '"' +
                    "</span><br><span>Total: " + (d[1]-d[0]));
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (height - margin.bottom) + ")")
        .call(d3.axisBottom(x))
        .append("text")
        .attr("x", width / 2)
        .attr("y", margin.bottom * 0.5)
        .text("Records");

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + margin.left + ",0)")
        .call(d3.axisLeft(y));
}
