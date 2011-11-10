var labelType, useGradients, nativeTextSupport, animate, ht, info;
var comment_conext = false;

var Log = {
  write: function(text){
    $("#message").html(text);
  }
};

$().ready(function(){
    init();
    display('13k.json');
    $("#load").bind('click', function(){
        $("#more").fadeIn();
    });
    $("#more a").bind('click', function(){
        display(this.rel);
    });
});

function display(filename){
    $("#more").fadeOut();
    Log.write("Loading data via AJAX");
    $.getJSON('/ore/' + filename, function(json) {
        info = json.info;
        //load JSON data.
        $("#title").html(info.title);
        Log.write("Data loaded, computing the visualisation");
        ht.loadJSON(json.data);
        ht.refresh();
    });
}

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



function init(){
    
    var infovis = document.getElementById('infovis');
    var w = infovis.offsetWidth - 50, h = infovis.offsetHeight - 50;
        
    //init Hypertree
    ht = new $jit.RGraph({
      //id of the visualization container
      injectInto: 'infovis',      
      levelDistance: 3,
      orientation: 'top',
      Navigation: {  
        enable: true,  
        type: 'auto',  
        panning: true, //true, 'avoid nodes'  
        zooming: 200 
      },
      //Change node and edge styles such as
      //color, width and dimensions.
      Node: {
        overridable: true,
        dim: 0.75,
        color: "#000"
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
        onRightClick: function(node, eventInfo, e) {  
          console.log(comment_context);
          //console.log(eventInfo);
          //console.log(e);
          if(comment_context !== false) window.open(comment_context, '_blank');
        } 
      },
      Tips: {  
        enable: true,  
        type: 'Native',  
        //offsetX: 10,  
        //offsetY: 10,  
        onShow: function(tip, node) {
            comment_context = 'http://reddit.com/' + info.permalink + '/' + node.data.id;
            var depth = node.data.depth;
            var rating = "(" + node.data.rating + ") ";
            if(node.data.depth == undefined){
                depth = '';
                rating = "* ";
            }
            tip.innerHTML = '<div class="rd_tip"><span>' + depth + rating + node.data.author + " &uarr;" + node.data.ups + " &darr;" + node.data.downs + "</span><br />" + node.data.body_html + '</div>';  
        },
        onHide: function(){
            comment_context = false;
        } 
      },
      Edge: {
        lineWidth: 0.2,
        color: "#D8DCBD"
      },
      //Change node styles when labels are placed
      //or moved.
      onBeforePlotNode: function(node) {
          if(node.data.depth == undefined){
              node.setData('dim', 2);
              first = false;
          }
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
          Log.write("Complete!");
          $("#message").fadeOut(5000); 
      }
    });
}