

function drawGraph(data){

	console.log(data);
	var percentageChange = data;
	//var percentageChange = [data.Results.output1.value.Values[0][0], data.Results.output1.value.Values[1][0], data.Results.output1.value.Values[2][0]];
	
	// Num of set of data received is hardcoded
	//var percentageChange = [0.3, -0.431, 0.167];

	var data = {
	    labels: ["Percentage Change"],
	    datasets: [
	        {
	            label: "Oil Commodity",
	            backgroundColor: "rgba(228,26,28,0.3)",
	            borderColor: "rgba(228,26,28,0.3)",
	            borderWidth: 1,
	            data: [percentageChange[0]]
	        },
	        {
	            label: "AEX Exchange",
	            backgroundColor: "rgba(55,126,184,0.5)",
	            borderColor: "rgba(55,126,184,0.5)",
	            borderWidth: 1,
	            data: [percentageChange[1]]
	        },
	        {
	            label: "HangSeng Index",
	            backgroundColor: "rgba(77,175,74,0.5)",
	            borderColor: "rgba(77,175,74,0.5)",
	            borderWidth: 1,
	            data: [percentageChange[2]]
	        },

	    ]
	};		

	$("#myChart").remove();
	$(".data-graph").append("<canvas id='myChart'></canvas>");
	var ctx = document.getElementById("myChart");
	var chartInstance = new Chart(ctx, {
	    type: 'bar',
	    data: data,
	    options: {
	        responsive: false
	    }
	});

}

/* Colors that can be used 
#e41a1c
#377eb8
#4daf4a
#984ea3
#ff7f00
#ffff33
#a65628
#f781bf
*/

