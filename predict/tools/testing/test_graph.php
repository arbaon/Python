  <html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart1);
      google.charts.setOnLoadCallback(drawChart2);
      function drawChart1() {
        var data = new google.visualization.DataTable();
	data.addColumn('number', 'Games');
	data.addColumn('number', 'Results');
	data.addRows(
        <?php
	  $command = escapeshellcmd('/Users/bcorbett/MyGit/predict/testing/graph.py "Man United"');	  
	  $output = shell_exec($command);
	  echo $output;
	?>
        );
        var options = {
          title: 'Team Performance',
          curveType: 'function',
          legend: { position: 'top' }
	};
        var chart = new google.visualization.LineChart(document.getElementById('teama_chart'));
        chart.draw(data, options);
      }
      function drawChart2() {
        var data = new google.visualization.DataTable();
	data.addColumn('number', 'Games');
	data.addColumn('number', 'Results');
	data.addRows(
        <?php
	  $command = escapeshellcmd('/Users/bcorbett/MyGit/predict/testing/graph.py "Chelsea"');	  
	  $output = shell_exec($command);
	  echo $output;
	?>
        );
        var options = {
          title: 'Team Performance',
          curveType: 'function',
          legend: { position: 'top' }
	};
        var chart = new google.visualization.LineChart(document.getElementById('teamb_chart'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="teama_chart" style="width: 400px; height: 200px"></div>
    <div id="teamb_chart" style="width: 400px; height: 200px"></div>
  </body>
</html>

