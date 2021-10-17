makeSquare = function() {
  square = {};
  square.xSize = 200;
  square.ySize = 200;
  square.size = 1000;
  square.colors = ["#3300aa", "#770044", "#5500bb", "#cc0066"];
  
  square.prepare = function(data) {
    var x = 0;
    var y = 0;
    var colorIndex = 0;
    for (let record of data) {
      record.x = x;
      record.y = y;
      record.colorIndex = colorIndex;
      x = x + this.xSize;
      if (x > this.size) {
        x = 0;
        y = y + this.ySize;
      }
      colorIndex = (colorIndex + 1) % 4;
    }
    return data;
  }
  
  square.render = function(c, data) {
    for (let record of data) {
      var rect = new fabric.Rect({
        left: record.x,
        top: record.y,
        fill: this.colors[record.colorIndex],
        width: this.xSize,
        height: this.ySize,
      });
      c.add(rect);

      let leftOffset = this.xSize / 10;
      let yOffset = this.ySize / 2;
      var text = new fabric.Text(record.label, {
        left: record.x + leftOffset,
        top: record.y + yOffset,
        fill: '#ffffff',
        fontSize: 20
      });
      c.add(text);
    }
  }
  return square;
}

makeTriangle = function () {
  triangle = {};
  triangle.xSize = 200;
  triangle.ySize = 200;
  triangle.size = 1000;
  triangle.images = ["images/1.jpg", "images/2.jpg", "images/3.jpg"];
  
  triangle.prepare = function(data) {
    var x = 0;
    var y = 0;
    var angle = 0;
    var imageIndex = 0;
    for (let record of data) {
      record.x = x;
      record.y = y;
      record.angle = angle;
      record.imageIndex = imageIndex;
      if (angle === 0) {
        x = x + this.xSize / 2;
        angle = 180;
      } else if (angle === 180) {
        x = x + this.xSize / 2;
        angle = 0
      }
      if (x + (this.xSize) > this.size) {
        x = 0;
        angle = 0;
        y = y + this.ySize;
      }
      imageIndex = (imageIndex + 1) % 3;
    }
    return data;
  }
  
  triangle.render = function(c, data) {
    for (let record of data) {
      let triangleClipPath = new fabric.Triangle({
        originX: 'center',
        originY: 'center',
        width: this.xSize,
        height: this.ySize,
        angle: record.angle,
        selectable: false,
      });
      let imagePath = triangle.images[record.imageIndex];
      fabric.Image.fromURL(imagePath, function(img) {
        img.left = record.x - (img.width / 2) + (triangle.xSize / 2);
        img.top = record.y - (img.height / 2) + triangle.ySize / 2;
        img.selectable = false;
        img.clipPath = triangleClipPath;
        img.on('mousedown', function(event) {
          console.log(record.title);
        });
        c.add(img);
      });
    }
  }
  return triangle;
}

// pick a tessellations, then ..
tess = makeTriangle(); 
fetch('vinyl.json')
  .then(response => response.json())
  .then(data => {
      var canvas = new fabric.Canvas('vinylCanvas');
      tess.render(canvas, tess.prepare(data))
  });
