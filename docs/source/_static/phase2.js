

var phase2_main = function() {
  // Load the rps data
  jQuery("#phase2-rps-chart").each(function() {
    var options = {
      chart: {
        renderTo: 'phase2-rps-chart',
        defaultSeriesType: 'line'}
      ,
      title: {
        text: 'Request Per Second (more is better)'}
      ,
      xAxis: {
        categories: [],
        title: { text: 'Concurrency'}}
      ,
      yAxis: {
        title: {
          text: 'RPS'}}
      ,
      series: []
    };
    csv_chart("_static/data/phase2/rps.csv", options);}
                                  );

  jQuery("#phase2-tpr-chart").each(function() {
    var options = {
      chart: {
        renderTo: 'phase2-tpr-chart',
        defaultSeriesType: 'line'}
      ,
      title: {
        text: 'Time(ms) per Request (less is better)'}
      ,
      xAxis: {
        categories: [],
        title: { text: 'Concurrency'}}
      ,
      yAxis: {
        title: {
          text: 'TPR (ms)'}}
      ,
      series: []
    };
    csv_chart("_static/data/phase2/tpr.csv", options);}
                                  );
}


jQuery(phase2_main);
