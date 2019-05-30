<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Sonda z czujnikiem DS18B20</title>


  <link href="css/styles.css" rel="stylesheet" />

  <style>
    #chart {
      max-width: 650px;
      margin: 35px auto;
    }

  </style>
</head>

<body>
  <div id="chart">

    <select id="days" onchange="new_selection()"><option>none</option></select><br/><br/>
    <canvas id="myChart" width="800" height="600"></canvas>
  </div>


  <script src="scripts/Chart.bundle.min.js"></script>
  <script src="scripts/scripts.js"></script>
  <script>
    var ctx = document.getElementById('myChart');
    var scatterChart = new Chart(ctx, {
        type: 'scatter',
        options: {
            legend: {
                display: false,
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    position: 'bottom',
                    time: {
                        displayFormats: {
                            hour: 'HH:MM',
                        },
                        tooltipFormat: 'HH:mm',
                    },
                }],
                yAxes: [{
                    ticks: {
                        callback: function(val, idx, values) {
                            return val + '°C';
                        },
                        suggestedMin: 0,
                        suggestedMax: 10,
                    }
                }]
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var date = tooltipItem.xLabel;
                        var temp = Math.round(tooltipItem.yLabel * 10) / 10 + "°C";
                        
                        var label = temp + " godz." + date;
                        return label;
                    }
                }
            }
        }
    });
    refresh_days();
</script>
</body>

</html>
