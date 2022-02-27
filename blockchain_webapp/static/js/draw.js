


var imgA;
var imgB;

function setup() {

    createCanvas(2080, 1024);
    background(255);

    imgA = createImage(2048, 2048);
    imgB = createImage(2048, 2048);

    imgA.loadPixels();
    imgB.loadPixels();

    var d = pixelDensity();


    for (var i = 0; i < 1024* 1024 * 4 * d; i += 4) {
    imgA.pixels[i] = 240;
    imgA.pixels[i + 1] = 245;
    imgA.pixels[i + 2] = 250;
    imgA.pixels[i + 3] = 255;
    imgA.pixels[i + 4] = 260;
    imgA.pixels[i + 5] = 265;
    imgA.pixels[i + 6] = 270;
}


    imgA.updatePixels();




}

function draw() {
    if (!keyIsDown(2)) {
        image(imgA, 0, 0);

    } else {
        image(imgB, 0, 0);

    }
}

function makeVector(x, y) {
    var vector = [x, y, 1];
    return vector;
}

function makeIdentity() {
    var matrix = [[1, 0, 0],[0, 1, 0],[0, 0, 1]
    ];
    return matrix;
}

function makeMove(tx, ty) {
    var matrix = [[1, 0, tx],[0, 1, ty],[0, 0, 1]
    ];
    return matrix;
}






function drawVector(img, vec) {
    img.set(vec[0], vec[1], color(25, 1, 1));
    img.updatePixels();
}

function mouseDragged() {
    var x = mouseX;
    var y = mouseY, vector = makeVector(mouseX, mouseY);
    drawVector(imgA, vector);
}
