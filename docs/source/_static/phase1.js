

var phase1_main = function() {
  // Load the rps data
  jQuery("#phase1-rps-chart").each(function() {
    var options = {
      chart: {
        renderTo: 'phase1-rps-chart',
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
    csv_chart("_static/data/phase1/rps.csv", options);}
                                  );

  jQuery("#phase1-tpr-chart").each(function() {
    var options = {
      chart: {
        renderTo: 'phase1-tpr-chart',
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
    csv_chart("_static/data/phase1/tpr.csv", options);}
                                  );
}


jQuery(phase1_main);
