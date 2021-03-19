<?php
    $db_name = "master";
    $db = new PDO('sqlite:' . $db_name . '.db');

    // FUNCTION HANDLER
    if (isset($_POST['dump_tables'])) {
        $sql = 'SELECT name FROM sqlite_master WHERE type="table"';
        $str = "";
        foreach($db->query($sql) as $row) {
            if ($row['name'] !== "sqlite_sequence") {
                $str .= $row['name'] . ", ";
            }
        }
        $str = rtrim($str, ", ");
        echo $str;
    }
    else if (isset($_POST['dump'])) {
        $json = "[";
        foreach($db->query('SELECT * from ' . $_POST['dump']) as $row) {
            $json .= json_encode($row) . ", ";
        }
        $json = rtrim($json, ", ") . "]";
        echo $json;
    }
    else if (isset($_POST['dump_columns'])) {
        $sql = 'SELECT sql FROM sqlite_master WHERE type="table" AND tbl_name = "' . $_POST['dump_columns'] . '"';
        foreach($db->query($sql) as $row) {
            echo $row[0];
        }
    }

    $db = null;
?>
