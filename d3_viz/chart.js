// Set the margins
var margin = {top: 100, right: 100, bottom: 100, left: 100},
  width = 850 - margin.left - margin.right,
  height = 600 - margin.top - margin.bottom;

// Create SVG
var svg = d3.select("#graph")
        .append("svg")
        .style("width", 1000 + "px")
        .style("height", 1000 + "px")
        .attr("width", 1000)
        .attr("height", 1000)
        .append("g")
        .attr("class", "svg");

// Create tooltip
var tooltip = d3.select("body").append("div").attr("class", "toolTip");

// Set x and y axis range
var x = d3.scaleLinear().range([0, width]);
var y = d3.scaleBand().range([height, 0]);

// Set location for graph
var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
// Load the salary json data
d3.json("salary_data.json", function(error, data) {
    if (error) throw error;

    jobs = data.data.cleaned_job_title

    var unique = [...new Set(data.data.map(item => item.Group))];
  
    // Group the data by name and experience level
    var dataGrouped = d3.nest()
      .key(function(d) { return d.experiences; })
      .rollup(function(v) { return {
            min: d3.min(v, function(d) { return d.salary; }),
            median: d3.median(v, function(d) { return d.salary; }),
            max: d3.max(v, function(d) { return d.salary; }),
            count: v.length
      }; })
      .sortKeys(d3.descending)
      .entries(data.data);

    // Set domain for x and y axis
    x.domain([0, d3.max(data.data, function(d) { return d.salary; })]);
    y.domain(dataGrouped.map(function(d) { return d.key; })).padding(0.1);

    // Create x-axis ticks and lines
    g.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(15).tickFormat(function(d) { return "$" + parseInt(d / 1000) + "k"; }).tickSizeInner([-height]));

    // Create y-axis ticks and lines
    g.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y));

    // Number formatter
    var formatSuffix = d3.format(".2s"),
        formatMoney = function(d) { return "$" + formatSuffix(d); }

    // Create bars for graph and create tooltip
    g.selectAll(".bar")
        .data(dataGrouped)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.value.min); })
        .attr("height", y.bandwidth())
        .attr("y", function(d) { return y(d.key); })
        .attr("width", function(d) { return x(d.value.max) - x(d.value.min); })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 90 + "px")
              .style("display", "inline-block")
              .html("Experience: " + (d.key) + "<br><span>Min: " + 
                    formatMoney(d.value.min) + "</span><br><span> Median: " + 
                    formatMoney(d.value.median) + "</span><br><span> Max: " + 
                    formatMoney(d.value.max) + "</span><br><span> Count: " + 
                    (d.value.count) + "</span>"
                    );
        })
        .on("mouseout", function(d){ tooltip.style("display", "none");});
});

var selector = d3.select("#drop")
    .append("select")
    .attr("id","dropdown")
    .on("change", function(d){
        console.log("changed")
        // selection = document.getElementById("dropdown");

        // y.domain([0, d3.max(data, function(d){
        //     return +d[selection.value];})]);

        // yAxis.scale(y);

        // d3.selectAll(".rectangle")
        //     .transition()
        //     .attr("height", function(d){
        //         return height - y(+d[selection.value]);
        //     })
        //     .attr("x", function(d, i){
        //         return (width / data.length) * i ;
        //     })
        //     .attr("y", function(d){
        //         return y(+d[selection.value]);
        //     })
        //     .ease("linear")
        //     .select("title")
        //     .text(function(d){
        //         return d.State + " : " + d[selection.value];
        //     });
  
        // d3.selectAll("g.y.axis")
        //     .transition()
        //     .call(yAxis);

     });

selector.selectAll("option")
  .data(elements)
  .enter().append("option")
  .attr("value", function(d){
    return d;
  })
  .text(function(d){
    return d;
  })
