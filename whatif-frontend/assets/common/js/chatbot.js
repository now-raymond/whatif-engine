/*
 *	AJAX - Handle chatbot events
 *	1. Hide and Show chatbot by passing(posting) "message" to its parent
 *	2. Send button click event - take user input and do a GET/POST request
 */

 $(document).ready(function(){
 	$("#hide-btn").click(function(e){
 		e.preventDefault();
 		window.top.postMessage("hide-chatbot", "*");
 	});

  	$("#close-btn").click(function(e){
 		e.preventDefault();
 		window.top.postMessage("close-chatbot", "*");
 	});	

  	$("#send-btn").click(function(){
  		makeRequest();
 	});	

  	// Handle Enter key, pressing Enter key is equivalent to pressing send button
  	$('#text-input').keypress(function (e) {
       var key = e.which;
		if(key == 13){
			makeRequest();
		}
      });         

 });


/*
 * THE FOLLOWING URL & REQUEST BODY HAVE TO BE CHANGED.
 *
 * --- Parsing is not required here because data returned is automatically parsed into object
 */

 function makeRequest(){
	var userInput = $("#text-input").val();
	var baseurl = "https://ussouthcentral.services.azureml.net/workspaces/dba1511d9f144eaea1a28f057929adc9/services/c3b0ba881f2c431da28a0f8dc7fbf820/execute?api-version=2.0&details=true";
	
	if(userInput == "") return;
	appendSentMessage(userInput);
	//console.log("HI");

	$.ajax({
	    url: baseurl,
	    headers: {
	    	// API Key is removed for security purposes
	        'Authorization':' ',
	        'Content-Type':'application/json'
	    },
	    method: 'POST',
	    dataType: 'json',
	    data: JSON.stringify(
	    {
		  "Inputs": {
		    "input1": {
		      "ColumnNames": [
		        "date",
		        "weightage",
		        "percentage_change",
		        "Column 3",
		        "Column 4",
		        "Column 5",
		        "Column 6",
		        "Column 7",
		        "Column 8",
		        "Column 9",
		        "Column 10",
		        "Column 11",
		        "Column 12"
		      ],
		      "Values": [
		        [
		          "2017-03-12",
		          "0",
		          "0",
		          userInput,
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0"
		        ],
		        [
		          "2017-03-12",
		          "0",
		          "0",
		          userInput,
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0",
		          "0"
		        ]
		      ]
		    }
		  },
		  "GlobalParameters": {
		    "Split tokens on special characters": "True",
		    "Split tokens on special characters1": "",
		    "Split tokens on special characters2": ""
		  }
		}),

        success: function(responseData, status, xhr) {
	    	var percentageChange = [responseData.Results.output1.value.Values[0][0], responseData.Results.output1.value.Values[1][0], responseData.Results.output1.value.Values[2][0]];
	    	window.parent.drawGraph(percentageChange);   	
        },
        error: function(request, status, error) {
            //console.log(error);
        }
	});


	
	// Clear input field

	$("#text-input").val('');
 }

/*
 *  
 */
 function appendSentMessage(str){
 	$(".conversation-container").append(
 			"<div><div class='message message-sent float-right'>" + str + "</div></div>"
 		);
 }







