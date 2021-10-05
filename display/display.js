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

square.render = function(ctx, data) {
  ctx.font = "20px Arial";
  for (let record of data) {
    ctx.fillStyle = this.colors[record.colorIndex];
    ctx.fillRect(record.x, record.y, record.x + this.xSize, record.y + this.ySize);
    ctx.fillStyle = "#ffffff";
    let leftOffset = this.xSize / 10;
    let rightOffset = this.xSize / 5;
    let yOffset = this.ySize / 2;

    ctx.fillText(record.title,
        record.x + leftOffset,
        record.y + yOffset,
        this.xSize - rightOffset
    );
  }
}

fetch('vinyl.json')
  .then(response => response.json())
  .then(data => {
      // pick a tessellations, then ..
      var canvas = document.getElementById("vinylCanvas");
      var ctx = canvas.getContext("2d");

      let preparedData = square.prepare(data);
      square.render(ctx, data)
  });
