var getBlocklyScreenshot = function (divName = "blocklyDiv") {
    blocklyDiv = document.getElementById(divName)
    rect = blocklyDiv.getBoundingClientRect();
    scrollX = rect.left;
    scrollY = rect.top;
    width = rect.width;
    height = rect.height;
    return html2canvas(blocklyDiv, {
        foreignObjectRendering: true,
        scrollX: scrollX,
        scrollY: scrollY,
        width: width,
        height: height
    }).then(function (canvas) {
        var img = new Image();
        img.src = canvas.toDataURL();
        return img;
    });
};
