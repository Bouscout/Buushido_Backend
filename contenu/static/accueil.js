var head ; 
var small_head ;
var elements;
jQuery.event.special.touchstart = {
    setup: function( _, ns, handle ) {
        this.addEventListener("touchstart", handle, { passive: !ns.includes("noPreventDefault") });
    }
};
jQuery.event.special.touchmove = {
    setup: function( _, ns, handle ) {
        this.addEventListener("touchmove", handle, { passive: !ns.includes("noPreventDefault") });
    }
};
$(document).ready(e=>{
    head = $('#la_tete')
    small_head = $('#big_bro')
    elements = document.getElementsByClassName('titre')
    function vitrine(){
        intro()
        setTimeout(vitrine, 8000)
    }setTimeout(vitrine, 4000) ;
})

function intro(){
    for (let i = 0; i < elements.length; i++){
        elements[i].style.transform = 'translateY(30px)'    
        elements[i].style.opacity = '0'    }
    head.css('transform', 'scale(0.98)')
    head.css('-webkit-filter', 'brightness(30%)')
    head.css('opacity', '0.3')
    setTimeout(e=>{
        scrollR()
        head.css('opacity', '1')
        head.css('-webkit-filter', 'brightness(100%)')
            head.css('transform', 'scale(1.0)')
            for (let i = 0; i < elements.length; i++){
                elements[i].style.transform = 'translateY(-30px)'    
                elements[i].style.opacity = '1'    }
    }, 200)
   
}
function scrollR(){
    let swipe = window.innerWidth
    const tete = document.getElementById('bigbro')
    if (tete.scrollLeft > swipe*2.8){
        tete.scrollLeft = 0 ;
        return
    }
    tete.scrollLeft += swipe ;
    console.log(tete.scrollLeft)
}
function reset(){
    const tete = document.getElementById('bigbro')
    head.css('transform', 'scale(1.05)')
    head.css('opacity', '0.1')
        setTimeout(e=>{
            tete.scrollLeft = 0 ;
            head.css('opacity', '1')
            head.css('transform', 'scale(1.0)')
}, 500)
}
var elem = document.getElementsByClassName('info') ;
document.onmousemove = function(event){
  let mouse = event.clientX ;
  if(mouse >= 1000)
    for (let i =0; i < elem.length; i++){
      elem[i].style.left = '-265px' ;
    }else{
      for (let i =0; i < elem.length; i++){
      elem[i].style.left = '108%' ;  
    }
  }
}
