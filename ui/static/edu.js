// Extension of Chandrakant Thakkar's work from http://bl.ocks.org/ChandrakantThakkarDigiCorp/2a9e6f11f2a27b6af0c28c4e5e524f10
// Original work uses MIT license

// Load the salary json data
var eduData = []
var rankedSubjects = []
d3v4.json("04_edu_data_bar_chart.json", function(error, json) {
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
      eduData.push({cleaned_job_title: d.cleaned_job_title, final_degree_category: d.final_degree_category, total: t, bars: bars})
    });

});

d3v4.csv("04_ranked_subjects.csv", function(error, data) {
    if (error) throw error;
    rankedSubjects = data

})

d3v4.select("#edugraph")
    .append("svg")
    .attr("width", 800)
    .attr("height", 700)

function updateEduGraph(data, jobValue) {

    var filteredData = data.filter(function(d) {
        return (d.cleaned_job_title == jobValue) });

    var group = rankedSubjects.filter(function(d) {
        return (d.cleaned_job_title == jobValue) }).map( function(d) {return d.subject_name });


    var gvs = d3v4.select("#edugraph svg"),
        margin = {
            top: 25,
            right: 100,
            bottom: 100,
            left: 180
        },
        width = +gvs.attr("width"),
        height = +gvs.attr("height");

    var xxx = d3v4.scaleLinear()
        .rangeRound([margin.left, width - margin.right]);

    xxx.domain([d3v4.min(filteredData, stackMin), d3v4.max(filteredData, stackMax)]);

    var yyy = d3v4.scaleBand()
        .rangeRound([height - margin.bottom, margin.top])
        .padding(0.1);

    yyy.domain(filteredData.map(function(d) {
        return d.final_degree_category;
    }))

    function stackMin(layers) {
        return d3v4.min(layers.bars, function(d) {
            return d.y0;
        });
    }

    function stackMax(d) {
        return d.total;
    }

    var z = d3v4.scaleOrdinal(d3v4.schemeCategory10);
    z.domain(group)

    var maing = gvs.append("g")
        .selectAll("g")
        .data(filteredData);

    var g = maing.enter().append("g")
        // .attr("fill", function(d) {
        //     return z(d.key);
        // });

    gvs.selectAll("rect").remove();
    gvs.selectAll(".axis").remove();
    gvs.selectAll(".x").remove();
    gvs.selectAll(".y").remove();

    var tooltip = d3v4.select("#education").append("div").attr("class", "toolTip");

    g.selectAll("rect")
        .data(function(d) {
            return d.bars;
        })
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("width", function(d) {
            return xxx(d.y1) - xxx(d.y0);
        })
        .attr("x", function(d) {
            return xxx(d.y0);
        })
        .attr("y", function(d) {
            return yyy(d.final_degree_category);
        })
        .attr("height", yyy.bandwidth)
        .style("fill", function(d) {
          return z(d.name)
        })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3v4.event.pageX + "px")
              .style("top", d3v4.event.pageY + "px")
              .style("display", "inline-block")
              .style("opacity", 1)
              .html('Degree Subject: "' + (d.name) + '"' +
                    "</span><br><span>Total Records: " + (d.value));
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});

    gvs.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (height - margin.bottom) + ")")
        .call(d3v4.axisBottom(xxx));

    // text label for the x axis
    gvs.append("g")
        .append("text")
        .attr("class","labels")
        .attr("transform",
            "translate(" + ((width)/2 - 20) + " ," + (height - margin.bottom + 50) + ")")
        .style("text-anchor", "center")
        .text("Total Records");

    gvs.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + margin.left + ",0)")
        .call(d3v4.axisLeft(yyy));

    // text label for the y axis
    gvs.append("text")
        .attr("class","labels")
        .attr("transform", "rotate(-90)")
        .attr("y", 0)
        .attr("x", -(height-margin.bottom)/2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Degree Type");
}
