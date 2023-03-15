var tete; 
var tete2 ;
var fait = false
var page ;
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
document.addEventListener('DOMContentLoaded', e =>{
    window.scrollTo(0, -5)
    page = document.getElementById('page')
    tete = document.getElementById('intro')
    tete2 = document.getElementById('tete')
})
//to manage the cool animation effect
document.addEventListener('scroll' ,e=>{
    if(fait == false){
    let pos = tete.getBoundingClientRect()  
    // console.log(pos.top)
        if (pos.top < 1){
            // tete.style.opacity = '0.3'
            // tete.style.visibility = 'hidden'
            tete.style.top = '0'
            setTimeout(e=>{
                tete.style.backdropFilter = 'blur(8px) contrast(88%)' ;
                tete.style['-webkit-backdrop-filter'] = 'blur(8px) contrast(88%)' ;
                // tete.style.visibility = 'visible'
                // tete.style.opacity = '1'
            }, 500)
            tete2.style.position = 'absolute'
            // document.getElementsByTagName('html').style.sc
            window.scrollTo({
                top: 0, 
                left: 0, 
                behavior: 'instant'
              });
            // window.scrollTo(1, 0)
            fait = true
        }
    }
})
//to manage the scrolling of the different pages
function scrolling(x){
    let elem1 = document.getElementById('det')
    let elem2 = document.getElementById('epis')
    let elem3 = document.getElementById('com')
    if(x == 0){
        elem1.style.borderColor = '#8b03cf'
        elem2.style.borderColor = 'white'
        elem3.style.borderColor = 'white'
        page.scrollLeft = -100 ;
    }else if(x == 1){
        elem1.style.borderColor = 'white'
        elem2.style.borderColor = '#8b03cf'
        elem3.style.borderColor = 'white'
        page.scrollLeft = window.innerWidth ;
    }else if(x == 2){
        alert("Desole cette section n'est pas encore finie")
        return
        elem1.style.borderColor = 'white'
        elem2.style.borderColor = 'white'
        elem3.style.borderColor = '#8b03cf'
        page.scrollLeft = window.innerWidth*2 ;
    }  
}
function showmenu(){
    let menu = document.getElementById('menu_saison')
    menu.style.display = 'flex';
}
window.onclick = function(e) {
    if (!e.target.matches('#sauce')) {
        setTimeout(e=>{
        document.getElementById('menu_saison').style.display = 'none'
        }, 5000)
    }
    
  }
// In order to select the saison old method
// used to englobe the filtrage
  function selection(){
    var input ;
    input = document.getElementById('my_option') ;
    choix = input.options[input.selectedIndex].text
  }
// in order to filter the episodes displayed
    function filtrage(choix){
        var epi = document.getElementsByClassName('epi') ;   
        var sais = document.getElementsByClassName('saison')  ;
        if(choix == '0'){
            for(i = 0 ; i < epi.length ; i++){
                epi[i].style.display = 'flex' ;
            }
        return ;
    }
    for(i = 0 ; i < epi.length ; i++){
        epi[i].style.display = 'none' ;
    }
    
    for(i = 0 ; i < sais.length ; i++){
        if(sais[i].textContent == choix ){
            epi[i].style.display = 'flex' ;
        }
    }
   
    return ;    
}

function regarde(){
    let pos = page.getBoundingClientRect()
    scrolling(1)
    window.scrollTo(0, pos.top)
}

// to add an anime to the user watchlist
function watch(){
let text = $('#watch')
let icon = $('#icon')
console.log('la lettre est :', text.text()[0])
$.ajax({
    url : 'http://buushido.ml/addwatch/' , 
    type : 'get' ,
    enctype: 'multipart/form-data',
    cache: false,
    headers: { "cache-control": "no-cache" },
    data :{
        text : $('#ref_id').text()
    },
    success : function(response){
        let resultat = document.getElementById('msg')
        resultat.innerHTML = response.message
        resultat.style.display = 'block'
        setTimeout(e=>{
            resultat.style.display = 'none'
        }, 5000)
    },
    error : function(xhr){     
        console.log('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
        let resultat = document.getElementById('msg')
        resultat.innerHTML = ':( sad face...'
        resultat.style.display = 'block'
        setTimeout(e=>{
            resultat.style.display = 'none'
        }, 5000)

    }
})
if (icon.attr('class')=='fa-regular fa-circle-check '){
    // text.text('Retirer de votre liste')
    icon.attr('class', 'fa-solid fa-circle-check ')
}else {
    // text.text(' Ajouter à votre liste')
    icon.attr('class', 'fa-regular fa-circle-check ')
}
}


// setting up the status of the watchlist icon
$(document).ready(e=>{
let ref = $('#ref') ;
// if (window.innerWidth < 1000){
    //     $('#watch').css('display', 'none') ;
    // }
if (ref.text() == 'n'){
    // $('#watch').text(' Ajouter à votre liste')
    $('#icon').attr('class', 'fa-regular fa-circle-check ')
}else{
    // $('#watch').text('Retirer de votre liste')
    $('#icon').attr('class', 'fa-solid fa-circle-check ')
}

})