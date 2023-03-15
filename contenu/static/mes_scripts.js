

function menu() {
    $('#myDropdown').addClass('show');
    // $('#myDropdown').slideDown("slow");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(e) {
    if (!e.target.matches('.dropbtn')) {
      // $('#myDropdown').slideUp("slow")
      $('#myDropdown').removeClass('show')
    
    }
  }

  function menu2() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
    tempo = x.className
    x.className += " slideleft" ;
    console.log('alors le nom est :', x.className);
    x.className = tempo ;
    
  }

function text(){
  var point = document.getElementById('points')  ;
  var text = document.getElementById('more') ;
  if( point.innerHTML == 'show more...'){
    point.innerHTML = 'show less' ;
    text.style.display = 'block' ;
  }else{
    point.innerHTML = 'show more...' ;
    text.style.display = 'none' ;
  }
}
/*  

const head = document.getElementById("the_head") ;
  var xDown = null, yDown = null, xUp = null, yUp = null;
  document.addEventListener('touchstart', touchstart, false);        
  document.addEventListener('touchmove', touchmove, false);
  document.addEventListener('touchend', touchend, false);
function touchstart(evt) { const firstTouch = (evt.touches || evt.originalEvent.touches)[0]; xDown = firstTouch.clientX; yDown = firstTouch.clientY; }
function touchmove(evt) { if (!xDown || !yDown ) return; xUp = evt.touches[0].clientX; yUp = evt.touches[0].clientY; }
function touchend(evt) { 
    var xDiff = xUp - xDown, yDiff = yUp - yDown;
    if ((Math.abs(xDiff) > Math.abs(yDiff)) && (Math.abs(xDiff) > 0.33 * document.body.clientWidth)) { 
        if (xDiff < 0) {
        la_vitrine(2);
      }else{
        la_vitrine(1);
        }
    } 
    xDown = null, yDown = null;
}
*/


document.addEventListener('DOMContentLoaded', e =>{
  if (window.innerWidth > 1000){
    var vette = document.getElementById("gallerie2") ;
    var b = 1000 ;
   }else{
    $('#pc_view').css('display', 'none') ; 
    $('#mob_view').css('display', 'grid') ; 
    var vette = document.getElementById("gallerie") ;
    var b = 250
    }
   function moving(){
     vette.scrollLeft += b;
     console.log(vette.scrollLeft)
     if (vette.scrollLeft >= b*3){
       vette.scrollLeft -= b*4 ;
     }
   }
    function auto(){
      moving();
      setTimeout(auto, 5000) ;
    }
    setTimeout(auto(), 5000) ;
  })

  document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('fr2').addEventListener('submit', function (e) {
        e.preventDefault();
        form = this;
        // Make a new timeout set to go off in 1000ms (1 second)
        $('body').addClass('travel') ;
        $('#boite').fadeOut() ;
        setTimeout(function () {
            // submit form after timeout
            form.submit();
        }, 7000);
    });
  });


 document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('fr1').addEventListener('submit', function (e) {
      e.preventDefault();
      form = this;
      // Make a new timeout set to go off in 1000ms (1 second)
      $('body').addClass('travel') ;
      $('#boite').fadeOut() ;
      setTimeout(function () {
          // submit form after timeout
          form.submit();
      }, 7000);
  });
});
