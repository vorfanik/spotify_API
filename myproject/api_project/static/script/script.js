"use strict"

let defaultOpn = document.getElementById("defaultOpen");
if (defaultOpn != null) {
    defaultOpn.click();
}


function openElement(evt, search) {
    let tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (var i of tabcontent) {
        i.style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (var i of tablinks) {
        i.className = i.className.replace(" active", "");
    }
    document.getElementById(search).style.display = "block";
    evt.currentTarget.className += " active";
}



