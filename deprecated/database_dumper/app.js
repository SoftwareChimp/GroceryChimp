function dump() {
    // CLEAR DUMP ELEMENT
    document.getElementById("dump").innerHTML = "";

    // GET TABLE INFORMATION
    $.post('database.php', {"dump_tables" : ""}, function (data) {
        let tables = data.split(', ');
        for (let table of tables) {
            // GET DATA FROM TABLE
            $.post('database.php', {"dump" : table}, function (data) {
                let dump = JSON.parse(data);
                let length = dump.length;
                let html = "<h3>TABLE: " + table + "</h3>";
                if (length > 0) {
                    // BUILD HTML TABLE IF ROW EXISTS
                    html += "<table><tr>";
                    let columns = [];
                    for (let col in dump[0]) {
                        if (isNaN(parseInt(col))) {
                            columns.push(col);
                            html += "<th>" + col + "</th>";
                        }
                    }

                    html += "</tr>";
                    for (let data of dump) {
                        html += "<tr>";
                        for (let col of columns) {
                            html += "<td>" + data[col] + "</td>";
                        }
                        html += "</tr>";
                    }
                    html += "</table>";
                    document.getElementById("dump").innerHTML += html;
                }
                else {
                    // DISPLAY SQL IF NO ROW IN TABLE EXISTS
                    $.post('database.php', {"dump_columns" : table}, function (data) {
                        html += "<span><i>Empty Table</i><br>" + data.replace("CREATE TABLE ", "") + "</span>";
                        document.getElementById("dump").innerHTML += html;
                    });
                }
            });
        }
    });
}
