// Borrowed from http://bl.ocks.org/ChandrakantThakkarDigiCorp/2a9e6f11f2a27b6af0c28c4e5e524f10

// Load the salary json data
var allData = []
var rankedSubjects = []
d3.json("04_edu_data_bar_chart.json", function(error, json) {
    if (error) throw error;
    json.forEach(function(d) {
      var t = 0
      var bars = []
      Object.keys(d).forEach(function(key, index) {
        if (key != 'cleaned_job_title' && key != 'final_degree_category') {
          bars.push({name: key, value: d[key], y0: t, y1: t + d[key], final_degree_category: d.final_degree_category})
          t += d[key]
        }
      });
      d.total = t
      allData.push({cleaned_job_title: d.cleaned_job_title, final_degree_category: d.final_degree_category, total: t, bars: bars})
    });

});

d3.csv("04_ranked_subjects.csv", function(error, data) {
    if (error) throw error;
    rankedSubjects = data

    updateGraph(allData, 'account executive')
})

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

    x.domain([d3.min(filteredData, stackMin), d3.max(filteredData, stackMax)]);

    var y = d3.scaleBand()
        .rangeRound([height - margin.bottom, margin.top])
        .padding(0.1);

    y.domain(filteredData.map(function(d) {
        return d.final_degree_category;
    }))

    function stackMin(layers) {
        return d3.min(layers.bars, function(d) {
            return d.y0;
        });
    }

    function stackMax(d) {
        return d.total;
    }

    var z = d3.scaleOrdinal(d3.schemeCategory10);
    z.domain(group)

    var maing = svg.append("g")
        .selectAll("g")
        .data(filteredData);

    var g = maing.enter().append("g")
        // .attr("fill", function(d) {
        //     return z(d.key);
        // });

    svg.selectAll("rect").remove();
    svg.selectAll(".axis").remove();
    svg.selectAll(".x").remove();
    svg.selectAll(".y").remove();

    var tooltip = d3.select("body").append("div").attr("class", "toolTip");

    g.selectAll("rect")
        .data(function(d) {
            return d.bars;
        })
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("width", function(d) {
            return x(d.y1) - x(d.y0);
        })
        .attr("x", function(d) {
            return x(d.y0);
        })
        .attr("y", function(d) {
            return y(d.final_degree_category);
        })
        .attr("height", y.bandwidth)
        .style("fill", function(d) {
          return z(d.name)
        })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX + "px")
              .style("top", d3.event.pageY + "px")
              .style("display", "inline-block")
              .html('"' + (d.name) + '"' +
                    "</span><br><span>Total: " + (d.value));
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
