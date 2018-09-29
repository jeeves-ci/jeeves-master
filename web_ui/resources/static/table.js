$( document ).ready(function() {

//    $(document).ajaxComplete(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
//      alert("Ajax request completed with response code " + xhr.status);
//    });
    var token = window.localStorage.getItem("access_token");
    if (token == null) {
        token = window.localStorage.getItem("access_token");
    }
    $.ajaxSetup({
        beforeSend: function (xhr)
        {
           xhr.setRequestHeader("Authorization","Bearer " + token);
        },
//        error: function (jqXHR, status, err) {
//            alert("Local error callback.");
//        },
    });


    const PAGE_SIZE = 25;
    var url = window.location.href;
    var arr_url = url.split("/");
    var webUiPublicIp = arr_url[2];
    var arrIp = webUiPublicIp.split(":");
    var restfulPublicIp = arrIp[0] + ":8080";

    $('#login').click(function(e)
    {
         var sidebar = $('.sidebar-container');
         sidebar.empty();
         var main = $('.main');
         main.empty().load('login');

    });

    function getTaskTableDiv(id, data){
        return "<div class='newTable'><table id='"+id+"'></table></div>";
    }

    function getMainTableDiv(){
        return `<div id="table-cont"><table id="table"></table></div>`;
    }
    $('.main').append(getMainTableDiv());

    function getNewSocketDiv(task_id){
        return "<pre id='socket_cont'><div id='content-" + task_id+ "'></div></pre>";
    }

    initMainTable();

function initNewTable(id, data){
    var workflowId = data.workflow_id;
    url = `http://${restfulPublicIp}/api/v1.0/workflow/${workflowId}/tasks`
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

    $('#'+id).on('click', 'tr', function () {

            // add new socket container
            var tr = $(this).closest('tr');
            var row = table.row( tr );


            if ( row.child.isShown() ) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            }
            else if (!tr.parent().is("thead")) {
                // Open this row
                row.child( getNewSocketDiv(row.data().task_id) ).show();
                tr.addClass('shown');
            }
            if (!tr.parent().is("thead")) {
                onTaskClick(row.data().task_id, row.data().workflow_id);
            }
    } );

    // Add highlight on hover
    $('#'+id).on( 'mouseenter', 'tr', function () {
            var tr = $(this).closest('tr');
            if (!tr.parent().is("thead")) {
                tr.addClass( 'highlight' ).siblings().removeClass('highlight');
                tr.css({"cursor":"pointer"})
            }
        } );

    $('#'+id).on( 'mouseleave', 'tr', function () {
            var tr = $(this).closest('tr');
            tr.removeClass( 'highlight' );
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
            { "data": "name", title:"Name", searchable:true },
            { "data": "workflow_id", title:"Workflow", orderable:false },
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
                if (element.column == 1) {
                    orderBy.push('name', element.dir);
                } else if (element.column == 3) {
                    orderBy.push('started_at', element.dir);
                } else if (element.column == 4){
                    orderBy.push('ended_at', element.dir);
                } else if (element.column == 5){
                     orderBy.push('status', element.dir);
                 }
              })
              d.order_by = orderBy.toString();
              if (d.search) {
                d.pattern = d.search.value;
              }
              delete d.columns;
              delete d.draw;
              delete d.length;
              delete d.start;
              delete d.search;
              delete d.order;
          },
        },
        "serverSide": true,
        "processing": true
    } );
    // Remove any sockets that may remain after pagination
    $('#table').on( 'page.dt', function () {
        for (var key in activeSockets) {
            activeSockets[key].close();
            delete activeSockets[key];
        }
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
            var id = row.data().workflow_id;
            row.child( getTaskTableDiv(id, row.data()) ).show();
            initNewTable(id, row.data());
            tr.addClass('shown');
        }
        // Remove any sockets belonging to the workflow
        for (var key in activeSockets) {
            if (activeSockets[key].workflowID == row.data().workflow_id) {
                activeSockets[key].close();
                delete activeSockets[key];
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
        delete activeSockets[taskID];
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
