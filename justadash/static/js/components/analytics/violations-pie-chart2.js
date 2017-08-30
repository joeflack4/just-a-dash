/**
 * Created by Joe Flack on 7/10/2016.
 */
	// global options variable
	var options = {
		responsive: true,
		scaleBeginAtZero: true,
        // you don't have to define this here, it exists inside the global defaults
		legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%>" +
        "<li><span style=\"background-color:<%=segments[i].fillColor%>\"></span>" +
        "<%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"
	};

		// PIE
		// PROPERTY TYPE DISTRIBUTION
		// context
		var ctxPTD = $("#property_types").get(0).getContext("2d");
		// data
		var dataPTD = [
			{
				label: "Single Family Residence",
				color: "#5093ce",
				highlight: "#78acd9",
				value: 52
			},
			{
				label: "Townhouse/Condo",
				color: "#c7ccd1",
				highlight: "#e3e6e8",
				value: 12
			},
			{
				label: "Land",
				color: "#7fc77f",
				highlight: "#a3d7a3",
				value: 6
			},
			{
				label: "Multifamily",
				color: "#fab657",
				highlight: "#fbcb88",
				value: 8
			},
			{
				label: "Farm/Ranch",
				color: "#eaaede",
				highlight: "#f5d6ef",
				value: 8
			},
			{
				label: "Commercial",
				color: "#dd6864",
				highlight: "#e6918e",
				value: 14
			}

		];

		// Property Type Distribution
		var propertyTypes = new Chart(ctxPTD).Pie(dataPTD, options);
			// pie chart legend
			$("#pie_legend").html(propertyTypes.generateLegend());
