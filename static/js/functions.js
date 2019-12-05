function makeCurrentChart(containerString, titleString, iCI, iCO, xPoints, num){
    var inputIn = generate(xPoints, iCI, num, "darkturquoise");
    var inputOut = generate(xPoints, iCO, num, "mediumorchid");
    var chart = new CanvasJS.Chart(containerString,
        {
            title:{
                text: titleString,
                fontFamily: "tahoma"
            },
            axisY: {
                title: "Current (A)"
            },
            axisX: {
                title: "Data Point #"
            },
            data: [
                {
                    type: "line",
                    showInLegend: true,
                    name: "series1",
                    legendText: "Charge Current",
                    dataPoints: inputIn
                },
                {
                    type: "line",
                    showInLegend: true,
                    name: "series2",
                    legendText: "Discharge Current",
                    dataPoints: inputOut
                },
            ]
        });

    chart.render();
}

function makeChart(containerString, titleString, yString, yPoints, xPoints, num){
    var points = generate(xPoints, yPoints, num, "darkturquoise");
    var chart = new CanvasJS.Chart(containerString,
        {
            title:{
                text: titleString,
                fontFamily: "tahoma"
            },
            axisY: {
                title: yString
            },
            axisX: {
                title: "Data Point #"
            },
            data: [
                {
                    type: "line",
                    dataPoints: points
                }
            ]
        });

    chart.render();
}

function generate(xp, yp, num, colorString){
    var arr = [];
    for(i=0; i < num; i++){
        arr.push({
            x: xp[i],
            y: yp[i],
            color: colorString,
            lineColor: colorString
        });
    }
    return arr;
}

