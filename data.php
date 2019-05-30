<?php
function get_files() {
    return json_encode(glob('days/*.csv'), JSON_UNESCAPED_SLASHES);
    /*$result = array();
    foreach (glob('days/*.csv') as $str) {
        array_push($result, str_replace('days/', '', $str));
    }
    return json_encode($result);*/
}

function csv_to_json($file) {
    $csv= file_get_contents($file);
    $array = array_map("csv_parse", explode("\n", $csv));
    $json = json_encode(map_xy($array));
    return $json;
}

function csv_parse($input) {
    return str_getcsv($input, ';');
}

function map_xy($arr) {
    $result = array();
    foreach($arr as $item) {
        $line = array();
        $line['y'] = floatval($item[0]);
        $line['x'] = $item[1];
        if ($line['x'] === NULL || $line['y'] === NULL) continue;
        array_push($result, $line);
    }
    return $result;
}

$cmd = $_GET['cmd'];

if ($cmd == 'f') {
    echo get_files();
} else if ($cmd == 'c') {
    $f = $_GET['d'];
    echo csv_to_json($f);
} else {
    echo '["missing"]';
}


?>