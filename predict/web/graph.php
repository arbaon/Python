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
	  echo $teama_output;
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
	  echo $teamb_output;
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
