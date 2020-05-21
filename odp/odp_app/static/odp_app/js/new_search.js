$(document).foundation();
$('#data_della_sentenza').fdatepicker({
    format: 'yyyy-mm-dd'
});
$('#data_del_deposito').fdatepicker({
    format: 'yyyy-mm-dd'
});
for (var year = (new Date()).getFullYear(); year >= 1983; year--) {
    $('#anno_del_deposito').append($('<option>', {
        value: year,
        text: year
    }));
}
$('#mostra_altre_opzioni').click(function () {
    $('#altre_opzioni').show();
    $('#mostra_altre_opzioni').remove();
    return false;
});

$('#danno_non_patrimoniale').change(function () {
    if (this.checked) {
        $('#dettagli_danno_non_patrimoniale').show();
        $('#tipo_danno_patrimoniale').attr('name', "danno_p");
    } else {
        $('#dettagli_danno_non_patrimoniale').hide();
        $('#tipo_danno_patrimoniale').removeAttr('name');
    }
});

$('#danno_morale').change(function () {
    if (this.checked) {
        $('#dettagli_danno_morale').show();
        $('#tipo_danno_morale').attr('name', "metodo_dm");
    } else {
        $('#dettagli_danno_morale').hide();
        $('#tipo_danno_morale').removeAttr('name');
    }
});


$('#search_form').submit(function () {
    $('#search_form').find('input, select').each(function () {
        var input = $(this);
        if (!input.val()) {
            input.prop('disabled', true);
        }
    });
});

$(window).on('pageshow', function () {
    $('#search_form').find('input, select').each(function () {
        var input = $(this);
        input.prop('disabled', false);
    });
    $('#dettagli_danno_morale').hide()
    $('#dettagli_danno_non_patrimoniale').hide()
});