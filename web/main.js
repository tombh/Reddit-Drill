var labelType, useGradients, nativeTextSupport, animate;

window.onload = function(){ init() };

(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem) 
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};

function init(){
    
    var infovis = document.getElementById('infovis');
    //var w = infovis.offsetWidth - 50, h = infovis.offsetHeight - 50;
    
    //init Hypertree
    var ht = new $jit.RGraph({
      //id of the visualization container
      injectInto: 'infovis',      
      levelDistance: 30,
      orientation: 'top',
      //canvas width and height
      //width: w,
      //height: h,
      Navigation: {  
        enable: true,  
        type: 'auto',  
        panning: true, //true, 'avoid nodes'  
        zooming: 50 
      },
      //Change node and edge styles such as
      //color, width and dimensions.
      Node: {
        overridable: true,
        dim: 3,
        color: "#7BA591"
      },
      NodeStyles: {  
        enable: true,  
        type: 'Native',  
        stylesHover: {
          color: '#374C53'  
        },  
        duration: 100
      },
      Events: {  
        enable: true,
        type: 'auto',  
        onClick: function(node, eventInfo, e) {  
          console.log(node);
          console.log(eventInfo);
          console.log(e);
        } 
      },
      Tips: {  
        enable: true,  
        type: 'Native',  
        //offsetX: 10,  
        //offsetY: 10,  
        onShow: function(tip, node) {  
         tip.innerHTML = node.data.body;  
        }  
      },
      Edge: {
          lineWidth: 1,
          color: "#D8DCBD"
      },
      onBeforeCompute: function(node){
          Log.write("centering");
      },      
      //Change node styles when labels are placed
      //or moved.
      onBeforePlotNode: function(node) {  
          if(node.data.rating == 1) {  
              node.setData('color', '#000');  
          } else if(node.data.rating == 2) {  
              node.setData('color', '#333');  
          } else if(node.data.rating == 3) {  
              node.setData('color', '#555');  
          } else if(node.data.rating == 4) {  
              node.setData('color', '#aaa');  
          } else if(node.data.rating > 4) {  
              node.setData('color', '#ddd');  
          }
      },
      onComplete: function(){
          Log.write("done"); 
      }
    });
    //load JSON data.
    ht.loadJSON(json);
    //compute positions and plot.
    ht.refresh();
    //end      
        
    //ht.loadJSON(json);  
    //compute node positions and layout  
    //ht.compute();  
    //emulate a click on the root node.  
    //ht.onClick(ht.root);  
}