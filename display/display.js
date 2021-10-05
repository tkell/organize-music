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
        width: record.x + this.xSize,
        height: record.y + this.ySize,
      });
      c.add(rect);

      let leftOffset = this.xSize / 10;
      let rightOffset = this.xSize / 5;
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

// pick a tessellations, then ..
sq = makeSquare();
fetch('vinyl.json')
  .then(response => response.json())
  .then(data => {
      var canvas = new fabric.StaticCanvas('vinylCanvas');

      let preparedData = sq.prepare(data);
      sq.render(canvas, data)
  });
