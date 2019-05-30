function new_selection() {
    var select = document.getElementById('days');
    refresh_graph(select.value);    
}

function refresh_days() {
    query_all_days(function(data) {
        var select = document.getElementById('days');
        select.options.length = 0;
        var selected = '';
        for(i in data) {
            var val = data[i];
            if (val.includes('alerts')) {
              continue;
            } 
            var opt = document.createElement("option");
            opt.value = val;
            opt.innerHTML = val.replace('days/termo.', '').replace('.csv', '');
            if (selected === '') {
                selected = val;
            } else if (selected.localeCompare(val) < 0) {
                selected = val;
            }
            // then append it to the select element
            select.appendChild(opt);
        }
        select.value = selected;
        new_selection();
    });
}

function refresh_graph(day) {
	query_data(day, function(data) {
        while (scatterChart.data.labels.length > 0) {
            scatterChart.data.labels.pop();
        }
        while (scatterChart.data.datasets.length > 0) {
            scatterChart.data.datasets.pop();
        }
        
		scatterChart.data.datasets.push({
            label:"Historia temperatury", 
            data:data,
            borderColor: 'blue',
            borderWidth: 1,
            showLine: true,
            fill: false
            });
		scatterChart.update();
	});
}

function query_all_days(callback) {
    return ajax_get_json('data.php?cmd=f', callback);
}

function query_data(file, callback) {
    return ajax_get_json('data.php?cmd=c&d=' + file, function(data) {
        //fuck me
        var str = JSON.stringify(data);
        var d = JSON.parse(str, function(k, v) {
           if (k === "x") {
                return new Date(v);
           } else {
                return v;
           }               
        });
        callback(d);
    });
}

function ajax_get_json(url, success, error) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        var data = JSON.parse(request.responseText);
        success(data);
      } else {
        // We reached our target server, but it returned an error
            error(request);
      }
    };

    request.onerror = function() {
      // There was a connection error of some sort
      error(request);
    };

    request.send();
}

