/**************************************************
modello: <cassetto id=id_cassetto>
           <titolo id=id_titolo />
           <contenuto id=id_cont />
         </cassetto>
**************************************************/


function cassetto(id_cassetto, id_titolo, id_cont) {
    var i = 0;
    while (document.getElementById('_toggle' + i)) { i++ }
    id_toggle = '_toggle' + i;

    eval("func_toggle = function(e) { if (document.getElementById('" + id_cont + "').style.display == 'none') { document.getElementById('" + id_cont + "').style.display = 'block'; document.getElementById('" + id_toggle + "').childNodes[0].data = 'nascondi'; } else { document.getElementById('" + id_cont + "').style.display = 'none'; document.getElementById('" + id_toggle + "').childNodes[0].data = 'mostra'; } if (e && e.preventDefault) {e.preventDefault();} else {return false;} }");
    var Testo = document.createTextNode('mostra');
    var Ancora = document.createElement('a');
    Ancora.id = id_toggle;
    Ancora.href = '#';
    if (Ancora.addEventListener) {
        Ancora.addEventListener('click', func_toggle, false);  // DOM v2
    } else if (Ancora.attachEvent) {
        Ancora.attachEvent('onclick', func_toggle);            // IE 5+
    } else {
        Ancora.onclick = func_toggle;                           // resto del mondo
    }
    Ancora.className = 'toggle';
    document.getElementById(id_cassetto).insertBefore(Ancora, document.getElementById(id_titolo));
    document.getElementById(id_cont).style.display = 'none';
    document.getElementById(id_toggle).appendChild(Testo);
}
