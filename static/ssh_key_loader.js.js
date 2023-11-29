// console.log(steg.encode('Hello How Are You?' , 'data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7'  ));

// console.log(steg.decode('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABv0lEQVQ4T2NkYGD4ysDAwMgAAf+hNBOUDaL/QsVAFBuU/QsmBtL4E2rAHyQD2J64y8A0gmnhtqUMnMb2ICbI0H/IBmBzATYDWDiN7UEuZIFaCjYD5AKQASBBkAtggOmJuwzIFrhtUBeA1IO8AXI13IBfn7cs/s/rEwtyKiwMGJ64y4B4jAyMEDHhtqUgF8As/f314GYGbntfBsavBzf/ed+W+Y+Rm+8Pp53Pf3ZDW5AEyAXMUL/CwgBkAPOHOS1/vh/e9vfvi0cMPKEZDIxvmtP+/ziyDcn1DAyM3HyQKPn6CS7OLCHHANKEDEDqGJ+4y8CdjSJLJIfxVXnE/18XjhCpHFUZq4oOOBbALgAFyu/bFxl+nj/C8PvOFawGgrzBbmjDwKqiy8DrEwuPBRQvvJtQxvBt+zKsBoBsFJ+6AzUckKPu85bFDB8nV+L1DpdnFINQQRdcDdwL388eZHhbFY2iGWQjq6oehot4EysZ+COyUb3wNEgLJdpAsjI7n4AVPY+3wohC/tx2cDjAXfCqPIIBOTaQbUF3HSgwJRcewwzEjyumMnxZNZWBRVIOI7A+zGlh+LJ6Bjj1CaTUwL0KAG58pxl1mhXcAAAAAElFTkSuQmCC'));

//@Samuel Zeleke
/*
SSH provides secure authentication and encrypted communication between client and server, 
it does not involve steganography directly
 used to load SSH keys in web applications.
*/
var imgdatauri;

  // Perform necessary operations to read the URL
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      document.querySelector("#image1").src = e.target.result;
      imgdatauri = e.target.result;
    };
  }
  reader.readAsDataURL(input.files[0]);
}

//To transform the encoded or encrypted data into its original form, making it readable or usable within the messaging app
//To transferring and storing messages, ensuring that only authorized recipients can understand the content.
function decode(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function(e) {
          console.log(steg.decode(e.target.result));
        
        document.querySelector('#decoded').innerText = steg.decode(e.target.result);
      };
    }
    reader.readAsDataURL(input.files[0]); 
  }

 // protecting sensitive data, including text messages, is crucial to ensuring user privacy and data security.
function hideText() {
  document.querySelector("#image2").src = steg.encode(document.querySelector('#text').value, imgdatauri);
}
