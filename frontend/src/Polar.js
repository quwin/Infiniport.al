import React, { useEffect, useRef } from 'react';
import anychart from 'anychart';

const PolarChart = ({ skillData }) => {
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

    chart = anychart.polar();

    chart.container(chartContainer.current);

    chart.interactivity().hoverMode('by-x');

    chart.yScale()
      .minimum(0)
      .maximum(100);

    chart.xAxis().ticks().enabled(false);
    chart.yAxis().ticks().enabled(false);
    chart.yAxis().labels(false);
    chart.xAxis().labels().fontSize('.7rem');


    chart.xGrid().palette(["#090d0f 1", "#090d0f .90"]);
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
    chart.xAxis().stroke('#283139', '2%');
    chart.yAxis().stroke('transparent');
    chart.background().fill(['#18141a']);

    var labelFormattingLvl = function () {
      return 'Lvl ' + this.value;
    };
    var labelFormattingExp = function () {
      return Math.round(this.value * divisor / 100).toLocaleString('en-US') + " xp";
    };

    var polygonSeries1 = chart.polygon(data1);
    polygonSeries1.name('Level');
    polygonSeries1.tooltip().format(labelFormattingLvl);
    polygonSeries1.legendItem().iconFill('#ec424c').iconType('line').iconStroke('6 #ec424c');

    var polygonSeries2 = chart.polygon(data2);
    polygonSeries2.name('Exp (to lvl ' + target + ')');
    polygonSeries2.tooltip().format(labelFormattingExp);
    polygonSeries2.legendItem().iconFill('#42ece2').iconType('line').iconStroke('6 #42ece2');

    var legend = chart.legend();
    legend.enabled(true);
    legend.positionMode('outside');
    legend.itemsLayout('vertical');
    legend.position('bottom');
    legend.align('left');
    legend.margin().top(-30);
    legend.itemsSpacing(5);

    chart.xScale("ordinal");
    chart.sortPointsByX(true);

    chart.draw();

  }, []);

  return (
    <div ref={chartContainer} style={{ width: "100%", height: "100%", position: 'absolute'}}></div>
  );
};

export default PolarChart;