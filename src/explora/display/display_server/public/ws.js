function writeToScreen(val){
	console.log(val)
}

function ws_handler(com){
  writeToScreen("WS msg recvd:" + JSON.stringify(com))
}

function start_ws(handler = ws_handler){

    const url = new URL(location.href)

    let websocket = new WebSocket("ws://" + url.host);
    document.websocket = websocket
    websocket.binaryType = "arraybuffer";
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };


    function onOpen(evt){
      writeToScreen("Client: connected");
      websocket.send("Explora's JS client connected")
    }

    function onClose(evt){
      if (evt.code == 1000){
        writeToScreen("Client: Disconnected");
      } else {
        writeToScreen("Client: Disconnected with error " + evt.code );
        writeToScreen(evt)
      }
    }

    function onMessage(evt){
       try{
          var com =  JSON.parse(evt.data);
          handler(com);
          
        } catch (e) {
        	
        	if (e instanceof SyntaxError){
	            writeToScreen("*** Received malformed msg ***");
	            writeToScreen(evt.data)
          	} else {
	            writeToScreen("*** Unknown error ***");
	            console.error(e);
          	}
        }
    	}
      
    function onError(evt){
      var msg = (evt.data)? evt.data : "<no data attached>";
      writeToScreen('Error: ' + msg);
      websocket.close();
      
    }
}