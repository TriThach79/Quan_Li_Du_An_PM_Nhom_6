var rangeSlider = $(".price-range"),
minamount = $("#minamount"),
maxamount = $("#maxamount"),
minPrice = rangeSlider.data('min'),
maxPrice = rangeSlider.data('max');
rangeSlider.slider({
range: true,
min: minPrice,
max: maxPrice,
values: [minPrice, maxPrice],
slide: function (event, ui) {
    minamount.val('$' + ui.values[0]);
    maxamount.val('$' + ui.values[1]);
}
});
minamount.val('$' + rangeSlider.slider("values", 0));
maxamount.val('$' + rangeSlider.slider("values", 1));