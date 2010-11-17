var csv_chart = function(uri, options) {
  $.get(uri, function(data) {
    // Split the lines
    var lines = data.split('\n');
    
    // Iterate over the lines and add categories or series
    $.each(lines, function(lineNo, line) {
      // Ignore blank lines
      if(line == "") return;

      var items = line.split(',');
        
        // header line containes categories
        if (lineNo == 0) {
            $.each(items, function(itemNo, item) {
              if (itemNo > 0) options.xAxis.categories.push(item);});}
        
        
        // the rest of the lines contain data with their name in the
        // first position
        else {
            var series = {
              data: []}
          ;
            $.each(items, function(itemNo, item) {
                if (itemNo == 0) {
                  series.name = item;}
                    else {
                      series.data.push(parseFloat(item));}});
            
          options.series.push(series);}});
    
    // Create the chart
    var chart = new Highcharts.Chart(options);});

};

