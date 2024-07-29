import React, { useEffect, useRef } from 'react';
import anychart from 'anychart';

const RadarChart = ({ skillData }) => {
  const chartContainer = useRef(null);
  var link;
  var chart;

  useEffect(() => {
    const base = 1.06;
    // lvl breakpoints
    const lvl85 = 51550086;
    const lvl80 = 31233985;
    const lvl75 = 18914480;
    const lvl70 = 11442925;
    const lvl65 = 6913694;
    const lvl60 = 4168553;
    const iconLink = 'https://d31ss916pli4td.cloudfront.net/game/ui/skills/skills_icon_'


    const levelCap = Math.max(...skillData.map(item => item[1]));
    let divisor;
    let target;
    if (levelCap > 79) {
      divisor = lvl85;
      target = '85';
    } else if (levelCap > 69) {
      divisor = lvl80;
      target = '80';
    } else if (levelCap > 59) {
      divisor = lvl70;
      target = '70';
    } else {
      divisor = lvl60;
      target = '60';
    }

    function logBaseTransform(data) {
      return data.map(item => [
        item[0],
        item[1],
        (item[2] / Math.pow(base, Math.min(levelCap, item[1]))) / (divisor / Math.pow(base, levelCap)) * 100,
      ]);
    }
    var transformedData = logBaseTransform(skillData);
    var dataSet = anychart.data.set(transformedData);

    var data1 = dataSet.mapAs({ 'x': 0, 'value': 1 });
    var data2 = dataSet.mapAs({ 'x': 0, 'value': 2 });
    chart = anychart.radar();

    chart.container(chartContainer.current);
    chart.yScale()
      .minimum(0)
      .maximum(100);

    chart.xAxis().ticks().enabled(false);
    chart.yAxis().ticks().enabled(false);
    chart.yAxis().labels(false);
    chart.xAxis().labels()
      .padding('1rem')
      .fontSize('.5rem');
      
    chart.xGrid().palette(["#090d0f 1", "#090d0f .95"]);
    chart.palette(["#ec424c", "#42ece2"]);
    chart.xGrid().stroke({
        color: "#283139",
        thickness: '2%',
        opacity: 1
    });
    chart.yGrid().stroke({
        color: "#283139",
        thickness: '.7%',
        opacity: 1
    });
    chart.interactivity().hoverMode('by-x');
    chart.xAxis().stroke('#283139', '2%');
    chart.yAxis().stroke('transparent');
    chart.background().fill(['transparent']);
      
    var legend = chart.legend();
    legend.enabled(true);
    legend.positionMode('outside');
    legend.itemsLayout('vertical');
    legend.position('bottom');
    legend.align('left');
    legend.margin().top(-30);
    legend.itemsSpacing(5);

    var labelFormattingLvl = function () {
      return 'Lvl ' + this.value;
    };
    var labelFormattingExp = function () {
      return Math.round(this.value * divisor / 100).toLocaleString('en-US') + " xp";
    };

    var series1 = chart.area(data1).name('Level');
    series1.tooltip().format(labelFormattingLvl);
    var series2 = chart.area(data2).name(`Exp (to lvl ${target})`);
    series2.tooltip().format(labelFormattingExp);

    chart.draw();

    chart.shareAsPng(function (response) {
          link = response;
    });
  }, []);

  return (
    <div ref={chartContainer} style={{ width: "100%", height: "100%", position: 'absolute'}}></div>
  );
};

export default RadarChart;
