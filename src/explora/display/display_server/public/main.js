let current_state = "system";

const source_screens = [
	{ type: "img", source : "sample_img.jpg", state : "ST1", show : true  },
	{ type: "video", source : "sample_video.mp4", state : "ST2"  }

]

function show_screen(com){
	if (com.state == "system"){
		console.log("WS system msg:" + com.msg);
		return;
	}
	
	let time = (current_state != com.state)? 100: 0; 
	current_state = com.state;

	$("#transition").fadeIn( time, ()=> {
		$("#transition").fadeOut(time*2);
		// Show the screen with id=screen_{comm.state} when the div#transition 
		// is fully shown 

		let screens = $(".backplate")

		let current_screen = $("#screen_" + com.state);
		if (current_screen.length){
			screens.addClass("hidden");
			current_screen.removeClass("hidden")
			if (typeof current_screen[0].play == "function"){
				current_screen[0].play()
			}
		} else {
			writeToScreen(" *** Not valid state "+ com.state +" ***")
		}

    if (com.state == 'FINAL'){
      $("#over p").addClass("final");      
    } else {
      $("#over p").removeClass("final");
    }

		$("#over p").text(com.count? com.count : "");
	});
}


$( document ).ready(function() {
    console.log( "ready!" );
    $("#transition").fadeOut(500);
    $("#over p").text("");

    source_screens.forEach( (item) => {
    	let el = document.createElement( item["type"] );
    	if (item["type"] == "video"){
    		el.src = item["source"];
			el.muted = true; // This allows for autoplay without restrictions
			el.preload = true;

    	} else if  ((item["type"] == "img")) {
	    	el.setAttribute("src", item["source"]);
    	} else {
    		console.log("not allowed item type" + item["type"]);
    		return;
    	}
		console.log(`Appended element type:${item["type"]}, file: ${item["source"]}`)

    	el.id = "screen_" + item["state"];
    	el.classList.add("backplate");
    	if (!item["show"]) {
	    	el.classList.add("hidden");
    	}
    	$("body").append(el);
    });
    
  	start_ws(show_screen);

});