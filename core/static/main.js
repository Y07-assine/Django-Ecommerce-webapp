const navOpen=document.querySelector(".nav__hamburger");
const navClose=document.querySelector(".close__toggle");
const menu=document.querySelector(".nav__menu2");
const navContainer=document.querySelector(".nav__menu2");


navOpen.addEventListener("click",()=>{
    menu.classList.add("open");
    document.body.classList.add("active");
    navContainer.style.left="0";
    navContainer.style.width="30rem";

});
navClose.addEventListener("click",()=>{
    menu.classList.remove("open");
    document.body.classList.remove("active");
    navContainer.style.left="-30rem";
    navContainer.style.width="0";

});

//============
//header_top
//============
$(function(){
    const menu=document.querySelector(".nav__menu2");
    var data=$(".header__top").html();
    $(window).ready(function(){
        if(window.innerWidth > 1200 ){
            $(".header__top").html(data);
            menu.classList.add("collapse");
            menu.classList.add("navbar-collapse");

        }
    });

    $(window).resize(function(){

        if(window.innerWidth < 1200 ){
            $(".header__top").empty();

            menu.classList.remove("collapse");
            menu.classList.remove("navbar-collapse");
        }
    });
    $(window).resize(function(){

        if(window.innerWidth>1200){
            ;
            menu.classList.add("collapse");
            menu.classList.add("navbar-collapse");

        }
    });

});
//==============
//end_header_top
//==============

$('.slider-one')
    .not(".slick-initialized")
    .slick({
        autoplay:true,
        autoplaySpeed:3000,
        dots:true,
        prevArrow: ".site-slider .slider-btn .prev",
        nextArrow: ".site-slider .slider-btn .next"
    });

$("#top-sale .owl-carousel , #pack .owl-carousel, #produit .owl-carousel").owlCarousel({
    loop:true,
    nav:true,
    dots:false,
    responsive:{
        0:{
            items:2
        },
        600:{
            items:3
        },
        1000:{
            items:4
        }
    }
});

//=============
//nbr_article
//=============
$(".article .owl-carousel").owlCarousel({
    loop:true,
    nav:true,
    dots:false,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:3
        }
    }
});
//===============
//end_nbr_article
//===============

//=========
//quantité
//=========

let $qty_up = $(".augmente_qt");
let $qty_down=$(".diminue_qt");

$qty_up.click(function(e){
    let $input =$(`#quantite[data-id='${$(this).data("id")}']`);
    if($input.val()>=1 && $input.val()<=9){
        $input.val(function(i,oldval){
            return ++oldval;
        });
    }

});
$qty_down.click(function(e){
    let $input =$(`#quantite[data-id='${$(this).data("id")}']`);
    if($input.val()>1 && $input.val()<=10){
        $input.val(function(i,oldval){
            return --oldval;
        });
    }

});



//============
//end_quantité
//============


function dropdown(button) {
    var x=button.id;
    switch (x) {
        case 'drop1':
            document.getElementById("myDropdown1").classList.toggle("show_content");break;
        case 'drop2':
            document.getElementById("myDropdown2").classList.toggle("show_content");break;
        case 'drop3':
            document.getElementById("myDropdown3").classList.toggle("show_content");break;
        case 'drop4':
            document.getElementById("myDropdown4").classList.toggle("show_content");break;
        case 'drop5':
            document.getElementById("myDropdown5").classList.toggle("show_content");break;
    }

}

window.onclick=(event)=>{
    if(!event.target.matches('.dropbtn')){
        var dropdowns =document.getElementsByTagName("dropdown-content");
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show_content')) {
                openDropdown.classList.remove('show_content');
            }
        }
    }
}

$(document).ready(()=>{
    var xhttp= new XMLHttpRequest();
    xhttp.onreadystatechange=()=>{
        if (xhttp.readyState==4 && xhttp.status==200){
            var produit=JSON.parse(xhttp.responseText).Produits;
            var details=produit.filter()
        }


    }
})

var brand = $('input[name=brand]:checked').val();
console.log(brand);
$price = $(".js-range-slider")
$price.ionRangeSlider({
type: "double",
grid: true,
min: 200,
max: 30000,
from: 5000,
to: 25000,
prefix: "Dhs"
});