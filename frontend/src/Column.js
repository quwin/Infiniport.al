import React, { useEffect, useRef } from 'react';
import anychart from 'anychart';

const ColumnChart = () => {
  const chartContainer = useRef(null);

  useEffect(() => {
    const topData = [
      ['greyheals | 90', 75,76,71,70,60,0,74,79,79,65],
      ['Grainbro', 83,80,71,72,50,0,79,80,79,74],
      ['Luuu | 90', 75,75,71,70,45,0,79,80,75,64],
    ];

    const SKILLS = [
      'Forestry',
      'Woodwork',
      'Farming',
      'Cooking',
      'Petcare',
      'Exploration',
      'Mining',
      'Stoneshaping',
      'Metalworking',
      'Business'
    ];

    var dataSet = anychart.data.set(topData);
    var series;

    var chart = anychart.column();
    chart.animation(true);
    chart.yScale().stackMode('value');


    SKILLS.map((skill, index) => {
      var seriesData = dataSet.mapAs({
        x: 0, 
        value: index + 1
      });
      series = chart.column(seriesData);

      series.name(skill);
      series.labels(true);
      series.labels().format("{%x}");
    });

    chart.yAxis().labels().format('{%Value}{groupsSeparator: }');

    chart.interactivity().hoverMode('by-x');
    chart.tooltip().valuePrefix('Lvl ').displayMode('union');

    chart.xAxis().ticks().enabled(false);
    chart.yAxis().ticks().enabled(false);
    chart.yAxis().labels(false);

    chart.yScale()
        .minimum(600)
        .maximum(700);

    chart.xGrid().palette(["#18141a"]);
    chart.interactivity().hoverMode('by-x');
    chart.xGrid().stroke({
         color: "transparent",
         thickness: '2%',
         opacity: 1
    });



    chart.yAxis().stroke('transparent');
    chart.background().fill(['transparent']);
    chart.barsPadding(0).barGroupsPadding(0.2);
    chart.container(chartContainer.current);

    chart.draw();
  }, []);

  return (
    <div ref={chartContainer} style={{ width: "100%", height: "25rem", position: 'relative'}}></div>
  );
};

export default ColumnChart;
