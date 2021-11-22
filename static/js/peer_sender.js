// call_sender.js is a basic implementation of WebRTC in my project

let localConnection = new RTCPeerConnection()

localConnection.onicecandidate = (e) => console.log(JSON.stringify(localConnection.localDescription))

const sendChannel = localConnection.createDataChannel("sendChannel");
sendChannel.onmessage = e =>  console.log("messsage received!!!"  + e.data )
sendChannel.onopen = e => console.log("open!!!!");
sendChannel.onclose = e => console.log("closed!!!!!!");

localConnection.createOffer().then(o => localConnection.setLocalDescription(o))