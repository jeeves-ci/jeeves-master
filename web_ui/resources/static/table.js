const PAGE_SIZE = 25;
var url = window.location.href;
var arr_url = url.split("/");
var webUiPublicIp = arr_url[2];
var arrIp = webUiPublicIp.split(":");
var restfulPublicIp = arrIp[0] + ":8080";

$( document ).ready(function() {
    initMainTable();

function getNewTableDiv(id, data){
    return "<div class='newTable'><table id='"+id+"'></table></div>";
}

function getNewSocketDiv(task_id){
    return "<pre id='socket_cont'><div id='content-" + task_id+ "'></div></pre>";
}


function initNewTable(id, data){
    var workflowId = data.workflow_id;
    url = `http://${restfulPublicIp}/api/v1.0/tasks?workflow_id=${workflowId}`
    $.ajax({
      url: url,
      success: onWorkflowTasksReceive.bind(this, id)
    });
}

function onWorkflowTasksReceive(id, data){
    var table = $('#'+id).DataTable( {
        "columns": [
            { "data": "task_name", title:"Name" },
            { "data": "minion_ip", title:"Minion" },
            { "data": "started_at", title:"Started At" },
            { "data": "date_done", title:"Ended At" },
            { "data": "status", title:"Status" }
        ],
        "order": [[0, 'asc']],
        data:data.tasks,
        paging: false,
        info: false,
        "searching": false
    } );
//    table.setAttribute("class", "table-hover");

    $('#'+id).on('click', 'tr', function () {

            // add new socket container
            var tr = $(this).closest('tr');
            var row = table.row( tr );


            if ( row.child.isShown() ) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            }
            else {
                // Open this row
                console.log(row.data());
                var id = row.data().workflow_id;
                row.child( getNewSocketDiv(row.data().task_id) ).show();
                tr.addClass('shown');
            }
            onTaskClick(row.data().task_id, row.data().workflow_id);
    } );
}


function initMainTable(){
    var table = $('#table').DataTable( {
        "columns": [
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { "data": "workflow_id", title:"Workflow", orderable:false, searchable:true },
            { "data": "started_at", title:"Started At" },
            { "data": "ended_at", title:"Ended At" },
            { "data": "status", title:"Status" }
        ],
        pageLength: 10,
        "order": [[2, 'desc']],
        destroy: true,
        ajax: {
            url: `http://${restfulPublicIp}/api/v1.0/workflows`,
            // Modify response to fit datatable expected vals
            dataFilter: function(res, type){
              var data = JSON.parse(res);

              data.recordsTotal = data.total;
              data.recordsFiltered = data.total;
              data.length = data.total;
              data.data = data.workflows;

              return JSON.stringify(data);
          },
          data: function(d){
              d.page = d.start;
              d.size = d.length;
              orderBy = [];
              d.order.forEach(function(element){
                if (element.column == 2) {
                    orderBy.push('started_at', element.dir);
                } else if (element.column == 3){
                    orderBy.push('ended_at', element.dir);
                } else if (element.column == 4){
                     orderBy.push('status', element.dir);
                 }
              })
              d.order_by = orderBy.toString();
              if (d.search) {
                d.pattern = d.search.value;
              }
          },
        },
        "serverSide": true,
        "processing": true
    } );

    // Add event listener for opening and closing workflows
    $('#table tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            console.log(row.data());
            var id = row.data().workflow_id;
            row.child( getNewTableDiv(id, row.data()) ).show();
            initNewTable(id, row.data());
            tr.addClass('shown');
        }
        // Remove any sockets belonging to the workflow
        for (var key in activeSockets) {
            if (activeSockets[key].workflowID == row.data().workflow_id) {
                activeSockets[key].close();
            }
        }
    } );
}

var activeSockets = {};
function onTaskClick(taskID, workflowID) {
    // Socket will be closed upon closing a task
    activeSocket = activeSockets[taskID];
    if (activeSocket && activeSocket.isActive(taskID)) {
        // remove existing socket container and close socket
        var socketContainer = $('#content-'+taskID);
        socketContainer.remove();
        activeSocket.close();
    } else {
        activeSockets[taskID] = openSocket(taskID, workflowID);
    }
}

function socketDetails(socket, taskID, workflowID) {
        this.socket = socket;
        this.taskID = taskID;
        this.workflowID = workflowID;
        this.isActive = function (taskID) {
            return this.socket && this.taskID == taskID;
        };
        this.close = function () {
            if (this.socket) {
                this.socket.close();
                this.socket = undefined;
                this.taskID = undefined;
                this.workflowID = undefined;
            }
        };
    }

function openSocket(taskId, workflowId) {
    var ws = new WebSocket(`ws://${webUiPublicIp}/tail/${taskId}`);
    var $message = $('#message');
    var $content = $('#content-' + taskId);
    $content.html('');
    ws.onopen = function(){
        $message.attr("class", 'label label-success');
        $message.text('open');
    };
    ws.onmessage = function(ev){
        $message.attr("class", 'label label-info');
        $message.hide();
        $message.fadeIn("fast");
        $message.text('received message');
        $content.append(ev.data);
    };
    ws.onclose = function(ev){
        $message.attr("class", 'label label-important');
        $message.text('closed');
    };
    ws.onerror = function(ev){
        $message.attr("class", 'label label-warning');
        $message.text('error occurred');
    };
    return new socketDetails(ws, taskId, workflowId);
}

});
